import uuid
from decimal import Decimal

import pytest

from pages.products_page import ProductsPage


def _nombre_unico_hu05(etiqueta=""):
    identificador = uuid.uuid4().hex[:8]
    sufijo = f" {etiqueta}" if etiqueta else ""
    return f"Producto Selenium HU05{sufijo} {identificador}"


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


def _existe_producto_bd(producto_id):
    from database import obtener_conexion

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM productos WHERE id = %s", (producto_id,))
    total = cursor.fetchone()[0]
    cursor.close()
    conexion.close()
    return total > 0


def _contar_productos_bd():
    from database import obtener_conexion

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM productos")
    total = cursor.fetchone()[0]
    cursor.close()
    conexion.close()
    return total


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
@pytest.mark.delete
@pytest.mark.happy
def test_hu05_eliminar_producto_confirmado(
    live_server, sesion_iniciada, nombre_evidencia
):
    """HU-05 camino feliz: confirmar la alerta elimina el producto correctamente."""
    nombre_evidencia["valor"] = "HU05_eliminar_feliz"
    driver = sesion_iniciada

    nombre_producto = _nombre_unico_hu05()
    producto_bd = _crear_producto_bd(nombre_producto, "25.00", 4, "Oficina")
    producto_id = producto_bd["id"]

    pagina_productos = ProductsPage(driver, live_server).abrir()
    pagina_productos.esperar_tabla_visible()
    pagina_productos.esperar_fila_por_nombre(nombre_producto)

    pagina_productos.hacer_clic_eliminar(producto_id)
    pagina_productos.esperar_alerta_presente()
    pagina_productos.aceptar_alerta_eliminacion()

    pagina_productos.esperar_fila_desaparece(producto_id)
    assert (
        pagina_productos.esperar_mensaje_exito()
        == "Producto eliminado correctamente."
    )
    assert not pagina_productos.fila_existe(producto_id)

    assert not _existe_producto_bd(producto_id)


@pytest.mark.selenium
@pytest.mark.delete
@pytest.mark.negative
def test_hu05_cancelar_eliminacion(live_server, sesion_iniciada, nombre_evidencia):
    """HU-05 prueba negativa: cancelar la alerta conserva el producto sin eliminar."""
    nombre_evidencia["valor"] = "HU05_eliminar_negativo"
    driver = sesion_iniciada

    nombre_producto = _nombre_unico_hu05("cancelar")
    producto_bd = _crear_producto_bd(nombre_producto, "18.00", 2, "Papeleria")
    producto_id = producto_bd["id"]

    pagina_productos = ProductsPage(driver, live_server).abrir()
    pagina_productos.esperar_tabla_visible()
    pagina_productos.esperar_fila_por_nombre(nombre_producto)

    pagina_productos.hacer_clic_eliminar(producto_id)
    pagina_productos.esperar_alerta_presente()
    pagina_productos.cancelar_alerta_eliminacion()

    assert pagina_productos.fila_existe(producto_id)
    assert pagina_productos.no_hay_mensaje_exito()

    assert _existe_producto_bd(producto_id)


@pytest.mark.selenium
@pytest.mark.delete
@pytest.mark.boundary
def test_hu05_eliminar_unico_producto(
    live_server, sesion_iniciada, nombre_evidencia, base_pruebas_vacia
):
    """HU-05 prueba de limites: eliminar el unico producto deja el listado vacio."""
    nombre_evidencia["valor"] = "HU05_eliminar_limite"
    driver = sesion_iniciada

    nombre_producto = _nombre_unico_hu05("unico")
    _crear_producto_bd(nombre_producto, "12.00", 1, "Unico")

    pagina_productos = ProductsPage(driver, live_server).abrir()
    pagina_productos.esperar_tabla_visible()
    assert pagina_productos.contar_filas() == 1

    fila = pagina_productos.esperar_fila_por_nombre(nombre_producto)
    producto_id = pagina_productos.obtener_id_fila(fila)

    pagina_productos.hacer_clic_eliminar(producto_id)
    pagina_productos.esperar_alerta_presente()
    pagina_productos.aceptar_alerta_eliminacion()

    pagina_productos.esperar_listado_vacio()
    assert pagina_productos.esta_listado_vacio()

    assert _contar_productos_bd() == 0
