from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TIEMPO_ESPERA_POR_DEFECTO = 10


class ProductsPage:
    BOTON_AGREGAR = (By.ID, "btn-agregar-producto")
    TABLA = (By.ID, "tabla-productos")
    LISTADO_VACIO = (By.ID, "listado-vacio")
    MENSAJE_EXITO = (By.ID, "mensaje-exito")
    FILAS = (By.CSS_SELECTOR, "#tabla-productos tbody tr")
    CELDA_NOMBRE = (By.CSS_SELECTOR, '[data-testid^="producto-nombre-"]')
    CELDA_PRECIO = (By.CSS_SELECTOR, '[data-testid^="producto-precio-"]')
    CELDA_CANTIDAD = (By.CSS_SELECTOR, '[data-testid^="producto-cantidad-"]')
    CELDA_CATEGORIA = (By.CSS_SELECTOR, '[data-testid^="producto-categoria-"]')

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.espera = WebDriverWait(driver, TIEMPO_ESPERA_POR_DEFECTO)

    def abrir(self):
        self.driver.get(f"{self.base_url}/productos")
        self.espera.until(
            lambda driver: driver.find_elements(*self.TABLA)
            or driver.find_elements(*self.LISTADO_VACIO)
            or "/login" in driver.current_url
        )
        return self

    def hacer_clic_agregar_producto(self):
        self.espera.until(EC.element_to_be_clickable(self.BOTON_AGREGAR)).click()
        return self

    def esperar_mensaje_exito(self):
        elemento = self.espera.until(
            EC.visibility_of_element_located(self.MENSAJE_EXITO)
        )
        return elemento.text

    def esperar_tabla_visible(self):
        self.espera.until(EC.visibility_of_element_located(self.TABLA))
        return self

    def esperar_listado_vacio(self):
        self.espera.until(EC.visibility_of_element_located(self.LISTADO_VACIO))
        return self

    def esta_tabla_visible(self):
        elementos = self.driver.find_elements(*self.TABLA)
        return bool(elementos) and elementos[0].is_displayed()

    def esta_listado_vacio(self):
        try:
            return self.driver.find_element(*self.LISTADO_VACIO).is_displayed()
        except NoSuchElementException:
            return False

    def contar_filas(self):
        return len(self.driver.find_elements(*self.FILAS))

    def buscar_fila_por_nombre(self, nombre):
        filas = self.driver.find_elements(*self.FILAS)
        for fila in filas:
            celda_nombre = fila.find_element(*self.CELDA_NOMBRE)
            if celda_nombre.text == nombre:
                return fila
        return None

    def esperar_fila_por_nombre(self, nombre):
        return self.espera.until(lambda driver: self.buscar_fila_por_nombre(nombre))

    def producto_existe(self, nombre):
        return self.buscar_fila_por_nombre(nombre) is not None

    def obtener_id_fila(self, fila):
        id_atributo = fila.get_attribute("id")
        return int(id_atributo.replace("fila-producto-", ""))

    def obtener_datos_fila(self, fila):
        return {
            "id": self.obtener_id_fila(fila),
            "nombre": fila.find_element(*self.CELDA_NOMBRE).text,
            "precio": fila.find_element(*self.CELDA_PRECIO).text,
            "cantidad": fila.find_element(*self.CELDA_CANTIDAD).text,
            "categoria": fila.find_element(*self.CELDA_CATEGORIA).text,
        }

    def hacer_clic_editar(self, producto_id):
        localizador = (By.CSS_SELECTOR, f'[data-testid="editar-producto-{producto_id}"]')
        self.espera.until(EC.element_to_be_clickable(localizador)).click()
        return self

    def obtener_fila_por_id(self, producto_id):
        return self.driver.find_element(By.ID, f"fila-producto-{producto_id}")

    def esperar_fila_con_datos(self, producto_id, **valores_esperados):
        def _condicion(driver):
            fila = driver.find_element(By.ID, f"fila-producto-{producto_id}")
            datos = self.obtener_datos_fila(fila)
            return all(
                datos.get(clave) == valor for clave, valor in valores_esperados.items()
            )

        return self.espera.until(_condicion)

    def hacer_clic_eliminar(self, producto_id):
        localizador = (
            By.CSS_SELECTOR,
            f'[data-testid="eliminar-producto-{producto_id}"]',
        )
        self.espera.until(EC.element_to_be_clickable(localizador)).click()
        return self

    def esperar_alerta_presente(self):
        self.espera.until(EC.alert_is_present())
        return self.driver.switch_to.alert

    def aceptar_alerta_eliminacion(self):
        self.esperar_alerta_presente().accept()
        return self

    def cancelar_alerta_eliminacion(self):
        self.esperar_alerta_presente().dismiss()
        return self

    def esperar_fila_desaparece(self, producto_id):
        localizador = (By.ID, f"fila-producto-{producto_id}")
        self.espera.until(EC.invisibility_of_element_located(localizador))
        return self

    def fila_existe(self, producto_id):
        return bool(self.driver.find_elements(By.ID, f"fila-producto-{producto_id}"))

    def no_hay_mensaje_exito(self):
        return not self.driver.find_elements(*self.MENSAJE_EXITO)
