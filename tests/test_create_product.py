import uuid

import pytest

from pages.product_form_page import ProductFormPage
from pages.products_page import ProductsPage


def _nombre_unico_hu02(etiqueta=""):
    identificador = uuid.uuid4().hex[:8]
    sufijo = f" {etiqueta}" if etiqueta else ""
    return f"Producto Selenium HU02{sufijo} {identificador}"


def _obtener_producto_bd(nombre):
    from database import obtener_conexion

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE nombre = %s", (nombre,))
    producto = cursor.fetchone()
    cursor.close()
    conexion.close()
    return producto


@pytest.mark.selenium
@pytest.mark.create
@pytest.mark.happy
def test_hu02_crear_producto_valido(live_server, sesion_iniciada, nombre_evidencia):
    """HU-02 camino feliz: datos validos registran el producto y lo muestran en el listado."""
    nombre_evidencia["valor"] = "HU02_crear_feliz"
    driver = sesion_iniciada
    nombre_producto = _nombre_unico_hu02()

    pagina_productos = ProductsPage(driver, live_server).abrir()
    pagina_productos.hacer_clic_agregar_producto()

    formulario = ProductFormPage(driver)
    formulario.completar_formulario(nombre_producto, "49.99", "10", "Electrónica")
    formulario.guardar()

    assert pagina_productos.esperar_mensaje_exito() == "Producto registrado correctamente."
    assert "/productos" in driver.current_url

    fila = pagina_productos.esperar_fila_por_nombre(nombre_producto)
    datos = pagina_productos.obtener_datos_fila(fila)
    assert datos["nombre"] == nombre_producto
    assert datos["precio"] == "49.99"
    assert datos["cantidad"] == "10"
    assert datos["categoria"] == "Electrónica"

    producto_bd = _obtener_producto_bd(nombre_producto)
    assert producto_bd is not None
    assert str(producto_bd["precio"]) == "49.99"
    assert producto_bd["cantidad"] == 10
    assert producto_bd["categoria"] == "Electrónica"


@pytest.mark.selenium
@pytest.mark.create
@pytest.mark.negative
def test_hu02_crear_producto_invalido(live_server, sesion_iniciada, nombre_evidencia):
    """HU-02 prueba negativa: precio y cantidad invalidos no registran el producto."""
    nombre_evidencia["valor"] = "HU02_crear_negativo"
    driver = sesion_iniciada
    nombre_producto = _nombre_unico_hu02("invalido")

    pagina_productos = ProductsPage(driver, live_server).abrir()
    pagina_productos.hacer_clic_agregar_producto()

    formulario = ProductFormPage(driver)
    formulario.completar_formulario(nombre_producto, "-5", "-1", "Electrónica")
    formulario.guardar()

    assert formulario.obtener_error_precio() == "El precio debe ser mayor que cero."
    assert formulario.obtener_error_cantidad() == "La cantidad no puede ser negativa."

    assert _obtener_producto_bd(nombre_producto) is None


@pytest.mark.selenium
@pytest.mark.create
@pytest.mark.boundary
def test_hu02_crear_producto_valores_limite(live_server, sesion_iniciada, nombre_evidencia):
    """HU-02 prueba de limites: valores maximos permitidos se guardan sin truncamiento."""
    nombre_evidencia["valor"] = "HU02_crear_limite"
    driver = sesion_iniciada

    prefijo = "Producto Selenium HU02 limite "
    identificador = uuid.uuid4().hex[:8]
    relleno = "X" * (100 - len(prefijo) - len(identificador))
    nombre_100 = f"{prefijo}{relleno}{identificador}"
    assert len(nombre_100) == 100

    categoria_80 = "C" * 80

    pagina_productos = ProductsPage(driver, live_server).abrir()
    pagina_productos.hacer_clic_agregar_producto()

    formulario = ProductFormPage(driver)
    formulario.completar_formulario(
        nombre_100, "99999999.99", "2147483647", categoria_80
    )
    formulario.guardar()

    assert pagina_productos.esperar_mensaje_exito() == "Producto registrado correctamente."

    fila = pagina_productos.esperar_fila_por_nombre(nombre_100)
    datos = pagina_productos.obtener_datos_fila(fila)
    assert datos["nombre"] == nombre_100
    assert datos["precio"] == "99999999.99"
    assert datos["cantidad"] == "2147483647"
    assert datos["categoria"] == categoria_80

    producto_bd = _obtener_producto_bd(nombre_100)
    assert producto_bd is not None
    assert str(producto_bd["precio"]) == "99999999.99"
    assert producto_bd["cantidad"] == 2147483647
    assert producto_bd["categoria"] == categoria_80
