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

    def esta_listado_vacio(self):
        try:
            return self.driver.find_element(*self.LISTADO_VACIO).is_displayed()
        except NoSuchElementException:
            return False

    def buscar_fila_por_nombre(self, nombre):
        filas = self.driver.find_elements(*self.FILAS)
        for fila in filas:
            celda_nombre = fila.find_element(*self.CELDA_NOMBRE)
            if celda_nombre.text == nombre:
                return fila
        return None

    def esperar_fila_por_nombre(self, nombre):
        return self.espera.until(lambda driver: self.buscar_fila_por_nombre(nombre))

    def obtener_datos_fila(self, fila):
        return {
            "nombre": fila.find_element(*self.CELDA_NOMBRE).text,
            "precio": fila.find_element(*self.CELDA_PRECIO).text,
            "cantidad": fila.find_element(*self.CELDA_CANTIDAD).text,
            "categoria": fila.find_element(*self.CELDA_CATEGORIA).text,
        }
