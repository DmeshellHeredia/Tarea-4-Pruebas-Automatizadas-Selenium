import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.mark.selenium
@pytest.mark.smoke
def test_humo_infraestructura_selenium(live_server, driver):
    """Valida servidor de pruebas, navegador Selenium, esperas explicitas y login end-to-end."""
    driver.get(f"{live_server}/login")

    campo_usuario = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "login-usuario"))
    )
    campo_password = driver.find_element(By.ID, "login-password")

    campo_usuario.send_keys(os.environ["TEST_LOGIN_USER"])
    campo_password.send_keys(os.environ["TEST_LOGIN_PASSWORD"])
    driver.find_element(By.ID, "btn-login").click()

    WebDriverWait(driver, 10).until(EC.url_contains("/productos"))

    assert "/productos" in driver.current_url
