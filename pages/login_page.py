from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TIEMPO_ESPERA_POR_DEFECTO = 10


class LoginPage:
    USUARIO = (By.ID, "login-usuario")
    PASSWORD = (By.ID, "login-password")
    BOTON_LOGIN = (By.ID, "btn-login")
    MENSAJE_ERROR = (By.ID, "mensaje-login-error")
    ERROR_USUARIO = (By.ID, "error-login-usuario")
    ERROR_PASSWORD = (By.ID, "error-login-password")
    BOTON_LOGOUT = (By.ID, "btn-logout")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.espera = WebDriverWait(driver, TIEMPO_ESPERA_POR_DEFECTO)

    def abrir(self):
        self.driver.get(f"{self.base_url}/login")
        self.espera.until(EC.visibility_of_element_located(self.USUARIO))
        return self

    def ingresar_usuario(self, usuario):
        campo = self.espera.until(EC.visibility_of_element_located(self.USUARIO))
        campo.clear()
        campo.send_keys(usuario)
        return self

    def ingresar_password(self, password):
        campo = self.driver.find_element(*self.PASSWORD)
        campo.clear()
        campo.send_keys(password)
        return self

    def enviar(self):
        self.driver.find_element(*self.BOTON_LOGIN).click()
        return self

    def iniciar_sesion(self, usuario, password):
        self.abrir()
        self.ingresar_usuario(usuario)
        self.ingresar_password(password)
        self.enviar()
        return self

    def esperar_redireccion_a_productos(self):
        self.espera.until(EC.url_contains("/productos"))
        return self

    def obtener_mensaje_error(self):
        elemento = self.espera.until(
            EC.visibility_of_element_located(self.MENSAJE_ERROR)
        )
        return elemento.text

    def obtener_error_usuario(self):
        elemento = self.espera.until(
            EC.visibility_of_element_located(self.ERROR_USUARIO)
        )
        return elemento.text

    def obtener_error_password(self):
        elemento = self.espera.until(
            EC.visibility_of_element_located(self.ERROR_PASSWORD)
        )
        return elemento.text

    def esperar_boton_logout_visible(self):
        elemento = self.espera.until(
            EC.visibility_of_element_located(self.BOTON_LOGOUT)
        )
        return elemento
