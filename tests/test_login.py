import os

import pytest

from pages.login_page import LoginPage


@pytest.mark.selenium
@pytest.mark.login
@pytest.mark.happy
def test_hu01_login_valido(live_server, driver, nombre_evidencia):
    """HU-01 camino feliz: credenciales validas inician sesion y redirigen a /productos."""
    nombre_evidencia["valor"] = "HU01_login_feliz"

    pagina_login = LoginPage(driver, live_server)
    pagina_login.iniciar_sesion(
        os.environ["TEST_LOGIN_USER"], os.environ["TEST_LOGIN_PASSWORD"]
    )
    pagina_login.esperar_redireccion_a_productos()

    assert "/productos" in driver.current_url
    assert driver.get_cookie("session") is not None

    boton_logout = pagina_login.esperar_boton_logout_visible()
    assert boton_logout.is_displayed()


@pytest.mark.selenium
@pytest.mark.login
@pytest.mark.negative
def test_hu01_login_credenciales_invalidas(live_server, driver, nombre_evidencia):
    """HU-01 prueba negativa: contrasena incorrecta no inicia sesion y muestra mensaje generico."""
    nombre_evidencia["valor"] = "HU01_login_negativo"

    pagina_login = LoginPage(driver, live_server)
    pagina_login.iniciar_sesion(
        os.environ["TEST_LOGIN_USER"], "contrasena_incorrecta_selenium_12345"
    )

    mensaje = pagina_login.obtener_mensaje_error()

    assert mensaje == "Usuario o contraseña incorrectos."
    assert "/login" in driver.current_url
    assert driver.get_cookie("session") is None


@pytest.mark.selenium
@pytest.mark.login
@pytest.mark.boundary
def test_hu01_login_campos_vacios(live_server, driver, nombre_evidencia):
    """HU-01 prueba de limites: usuario y contrasena vacios muestran mensajes obligatorios."""
    nombre_evidencia["valor"] = "HU01_login_limite"

    pagina_login = LoginPage(driver, live_server)
    pagina_login.iniciar_sesion("", "")

    assert pagina_login.obtener_error_usuario() == "El usuario es obligatorio."
    assert pagina_login.obtener_error_password() == "La contraseña es obligatoria."
    assert "/login" in driver.current_url
    assert driver.get_cookie("session") is None
