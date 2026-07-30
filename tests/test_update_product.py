import uuid
from decimal import Decimal

import pytest

from pages.product_form_page import ProductFormPage
from pages.products_page import ProductsPage


def _nombre_unico_hu04(etiqueta=""):
    identificador = uuid.uuid4().hex[:8]
    sufijo = f" {etiqueta}" if etiqueta else ""
    return f"Producto Selenium HU04{sufijo} {identificador}"


def _crear_producto_bd(nombre, precio, cantidad, categoria):
    from database import crear_producto, obtener_conexion

    exito, error = crear_producto(nombre, Decimal(str(precio)), cantidad, categoria)
    assert exito, f"No se pudo preparar el producto de prueba: {error}"

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE nombre = %s", (nombre,))
    producto = cursor.fetchone()
    cursor.close()
    conexion.close()
    return producto


def _obtener_producto_bd_por_id(producto_id):
    from database import obtener_conexion

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id = %s", (producto_id,))
    producto = cursor.fetchone()
    cursor.close()
    conexion.close()
    return producto


@pytest.mark.selenium
@pytest.mark.update
@pytest.mark.happy
def test_hu04_actualizar_producto_valido(
    live_server, sesion_iniciada, nombre_evidencia
):
    """HU-04 camino feliz: precio y cantidad validos actualizan el producto correctamente."""
    nombre_evidencia["valor"] = "HU04_actualizar_feliz"
    driver = sesion_iniciada

    nombre_producto = _nombre_unico_hu04()
    producto_bd = _crear_producto_bd(nombre_producto, "10.00", 1, "Inicial")
    producto_id = producto_bd["id"]

    pagina_productos = ProductsPage(driver, live_server).abrir()
    pagina_productos.esperar_tabla_visible()
    pagina_productos.hacer_clic_editar(producto_id)

    formulario = ProductFormPage(driver).esperar_formulario_visible()
    valores_precargados = formulario.obtener_valores_actuales()
    assert valores_precargados["nombre"] == nombre_producto
    assert valores_precargados["precio"] == "10.00"
    assert valores_precargados["cantidad"] == "1"
    assert valores_precargados["categoria"] == "Inicial"

    formulario.completar_precio("29.90")
    formulario.completar_cantidad("7")
    formulario.guardar()

    assert (
        pagina_productos.esperar_mensaje_exito()
        == "Producto actualizado correctamente."
    )
    assert "/productos" in driver.current_url

    pagina_productos.esperar_fila_con_datos(producto_id, precio="29.90", cantidad="7")

    producto_actualizado = _obtener_producto_bd_por_id(producto_id)
    assert str(producto_actualizado["precio"]) == "29.90"
    assert producto_actualizado["cantidad"] == 7
    assert producto_actualizado["nombre"] == nombre_producto
    assert producto_actualizado["categoria"] == "Inicial"


@pytest.mark.selenium
@pytest.mark.update
@pytest.mark.negative
def test_hu04_actualizar_producto_invalido(
    live_server, sesion_iniciada, nombre_evidencia
):
    """HU-04 prueba negativa: precio y cantidad invalidos no modifican la base de datos."""
    nombre_evidencia["valor"] = "HU04_actualizar_negativo"
    driver = sesion_iniciada

    nombre_producto = _nombre_unico_hu04("invalido")
    producto_bd = _crear_producto_bd(nombre_producto, "15.00", 5, "Original")
    producto_id = producto_bd["id"]

    pagina_productos = ProductsPage(driver, live_server).abrir()
    pagina_productos.esperar_tabla_visible()
    pagina_productos.hacer_clic_editar(producto_id)

    formulario = ProductFormPage(driver).esperar_formulario_visible()
    formulario.completar_precio("0")
    formulario.completar_cantidad("-3")
    formulario.guardar()

    assert formulario.obtener_error_precio() == "El precio debe ser mayor que cero."
    assert (
        formulario.obtener_error_cantidad() == "La cantidad no puede ser negativa."
    )
    assert "/editar" in driver.current_url

    producto_sin_cambios = _obtener_producto_bd_por_id(producto_id)
    assert str(producto_sin_cambios["precio"]) == "15.00"
    assert producto_sin_cambios["cantidad"] == 5
    assert producto_sin_cambios["nombre"] == nombre_producto
    assert producto_sin_cambios["categoria"] == "Original"

    pagina_productos.abrir()
    pagina_productos.esperar_tabla_visible()
    pagina_productos.esperar_fila_con_datos(producto_id, precio="15.00", cantidad="5")


@pytest.mark.selenium
@pytest.mark.update
@pytest.mark.boundary
def test_hu04_actualizar_producto_valores_limite(
    live_server, sesion_iniciada, nombre_evidencia
):
    """HU-04 prueba de limites: valores maximos permitidos se guardan sin truncamiento."""
    nombre_evidencia["valor"] = "HU04_actualizar_limite"
    driver = sesion_iniciada

    nombre_producto = _nombre_unico_hu04("limite")
    producto_bd = _crear_producto_bd(nombre_producto, "5.00", 1, "Previo")
    producto_id = producto_bd["id"]

    prefijo = "Producto Selenium HU04 limite "
    identificador = uuid.uuid4().hex[:8]
    relleno = "X" * (100 - len(prefijo) - len(identificador))
    nombre_100 = f"{prefijo}{relleno}{identificador}"
    assert len(nombre_100) == 100

    categoria_80 = "C" * 80

    pagina_productos = ProductsPage(driver, live_server).abrir()
    pagina_productos.esperar_tabla_visible()
    pagina_productos.hacer_clic_editar(producto_id)

    formulario = ProductFormPage(driver).esperar_formulario_visible()
    formulario.completar_formulario(
        nombre_100, "99999999.99", "2147483647", categoria_80
    )
    formulario.guardar()

    assert (
        pagina_productos.esperar_mensaje_exito()
        == "Producto actualizado correctamente."
    )

    pagina_productos.esperar_fila_con_datos(
        producto_id,
        nombre=nombre_100,
        precio="99999999.99",
        cantidad="2147483647",
        categoria=categoria_80,
    )

    producto_actualizado = _obtener_producto_bd_por_id(producto_id)
    assert producto_actualizado["nombre"] == nombre_100
    assert str(producto_actualizado["precio"]) == "99999999.99"
    assert producto_actualizado["cantidad"] == 2147483647
    assert producto_actualizado["categoria"] == categoria_80
