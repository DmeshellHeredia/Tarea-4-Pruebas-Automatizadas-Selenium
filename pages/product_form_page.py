from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TIEMPO_ESPERA_POR_DEFECTO = 10


class ProductFormPage:
    NOMBRE = (By.ID, "nombre")
    PRECIO = (By.ID, "precio")
    CANTIDAD = (By.ID, "cantidad")
    CATEGORIA = (By.ID, "categoria")
    BOTON_GUARDAR = (By.ID, "btn-guardar-producto")
    BOTON_CANCELAR = (By.ID, "btn-cancelar-producto")
    ERROR_NOMBRE = (By.ID, "error-nombre")
    ERROR_PRECIO = (By.ID, "error-precio")
    ERROR_CANTIDAD = (By.ID, "error-cantidad")
    ERROR_CATEGORIA = (By.ID, "error-categoria")

    def __init__(self, driver):
        self.driver = driver
        self.espera = WebDriverWait(driver, TIEMPO_ESPERA_POR_DEFECTO)

    def esperar_formulario_visible(self):
        self.espera.until(EC.visibility_of_element_located(self.NOMBRE))
        return self

    def completar_nombre(self, valor):
        campo = self.espera.until(EC.visibility_of_element_located(self.NOMBRE))
        campo.clear()
        campo.send_keys(valor)
        return self

    def completar_precio(self, valor):
        campo = self.driver.find_element(*self.PRECIO)
        campo.clear()
        campo.send_keys(valor)
        return self

    def completar_cantidad(self, valor):
        campo = self.driver.find_element(*self.CANTIDAD)
        campo.clear()
        campo.send_keys(valor)
        return self

    def completar_categoria(self, valor):
        campo = self.driver.find_element(*self.CATEGORIA)
        campo.clear()
        campo.send_keys(valor)
        return self

    def completar_formulario(self, nombre, precio, cantidad, categoria):
        self.completar_nombre(nombre)
        self.completar_precio(precio)
        self.completar_cantidad(cantidad)
        self.completar_categoria(categoria)
        return self

    def guardar(self):
        self.driver.find_element(*self.BOTON_GUARDAR).click()
        return self

    def cancelar(self):
        self.driver.find_element(*self.BOTON_CANCELAR).click()
        return self

    def obtener_error_nombre(self):
        elemento = self.espera.until(
            EC.visibility_of_element_located(self.ERROR_NOMBRE)
        )
        return elemento.text

    def obtener_error_precio(self):
        elemento = self.espera.until(
            EC.visibility_of_element_located(self.ERROR_PRECIO)
        )
        return elemento.text

    def obtener_error_cantidad(self):
        elemento = self.espera.until(
            EC.visibility_of_element_located(self.ERROR_CANTIDAD)
        )
        return elemento.text

    def obtener_error_categoria(self):
        elemento = self.espera.until(
            EC.visibility_of_element_located(self.ERROR_CATEGORIA)
        )
        return elemento.text
