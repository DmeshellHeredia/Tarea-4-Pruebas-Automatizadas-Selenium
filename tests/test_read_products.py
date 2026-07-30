import uuid
from decimal import Decimal

import pytest
from selenium.webdriver.common.by import By

from pages.products_page import ProductsPage


def _nombre_unico_hu03(etiqueta=""):
    identificador = uuid.uuid4().hex[:8]
    sufijo = f" {etiqueta}" if etiqueta else ""
    return f"Producto Selenium HU03{sufijo} {identificador}"


def _crear_producto_bd(nombre, precio, cantidad, categoria):
    from database import crear_producto, obtener_conexion

    exito, error = crear_producto(nombre, Decimal(precio), cantidad, categoria)
    assert exito, f"No se pudo preparar el producto de prueba: {error}"

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE nombre = %s", (nombre,))
    producto = cursor.fetchone()
    cursor.close()
    conexion.close()
    return producto


@pytest.fixture
def base_pruebas_vacia():
    """Vacia por completo productos en tarea4_selenium_test antes y despues de la prueba."""
    from database import obtener_conexion

    def _vaciar_productos():
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos")
        conexion.commit()
        cursor.close()
        conexion.close()

    _vaciar_productos()
    yield
    _vaciar_productos()


@pytest.mark.selenium
@pytest.mark.read
@pytest.mark.happy
def test_hu03_consultar_producto_existente(
    live_server, sesion_iniciada, nombre_evidencia
):
    """HU-03 camino feliz: un producto preparado en la base aparece correctamente en el listado."""
    nombre_evidencia["valor"] = "HU03_consultar_feliz"
    driver = sesion_iniciada

    nombre_producto = _nombre_unico_hu03()
    producto_bd = _crear_producto_bd(nombre_producto, "15.50", 3, "Hogar")

    pagina_productos = ProductsPage(driver, live_server).abrir()
    pagina_productos.esperar_tabla_visible()

    fila = pagina_productos.esperar_fila_por_nombre(nombre_producto)
    datos = pagina_productos.obtener_datos_fila(fila)

    assert datos["id"] == producto_bd["id"]
    assert datos["nombre"] == nombre_producto
    assert datos["precio"] == "15.50"
    assert datos["cantidad"] == "3"
    assert datos["categoria"] == "Hogar"

    assert str(producto_bd["precio"]) == "15.50"
    assert producto_bd["cantidad"] == 3
    assert producto_bd["categoria"] == "Hogar"


@pytest.mark.selenium
@pytest.mark.read
@pytest.mark.negative
def test_hu03_consultar_sin_autenticacion(live_server, driver, nombre_evidencia):
    """HU-03 prueba negativa: acceder a /productos sin sesion redirige al login sin mostrar inventario."""
    nombre_evidencia["valor"] = "HU03_consultar_negativo"

    pagina_productos = ProductsPage(driver, live_server).abrir()

    assert "/login" in driver.current_url
    assert pagina_productos.esta_tabla_visible() is False

    filas_inventario = driver.find_elements(
        By.CSS_SELECTOR, '[data-testid^="producto-nombre-"]'
    )
    assert filas_inventario == []


@pytest.mark.selenium
@pytest.mark.read
@pytest.mark.boundary
def test_hu03_consultar_unico_producto_con_valores_limite(
    live_server, sesion_iniciada, nombre_evidencia, base_pruebas_vacia
):
    """HU-03 prueba de limites: un unico producto con valores maximos se muestra sin truncar."""
    nombre_evidencia["valor"] = "HU03_consultar_limite"
    driver = sesion_iniciada

    prefijo = "Producto Selenium HU03 limite "
    identificador = uuid.uuid4().hex[:8]
    relleno = "X" * (100 - len(prefijo) - len(identificador))
    nombre_100 = f"{prefijo}{relleno}{identificador}"
    assert len(nombre_100) == 100

    categoria_80 = "C" * 80

    producto_bd = _crear_producto_bd(
        nombre_100, "99999999.99", 2147483647, categoria_80
    )

    pagina_productos = ProductsPage(driver, live_server).abrir()
    pagina_productos.esperar_tabla_visible()

    assert pagina_productos.contar_filas() == 1

    fila = pagina_productos.esperar_fila_por_nombre(nombre_100)
    datos = pagina_productos.obtener_datos_fila(fila)

    assert datos["id"] == producto_bd["id"]
    assert datos["nombre"] == nombre_100
    assert datos["precio"] == "99999999.99"
    assert datos["cantidad"] == "2147483647"
    assert datos["categoria"] == categoria_80

    assert str(producto_bd["precio"]) == "99999999.99"
    assert producto_bd["cantidad"] == 2147483647
    assert producto_bd["categoria"] == categoria_80
