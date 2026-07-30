import base64
import os
import threading
from pathlib import Path
from urllib.parse import urlparse

import pytest
from dotenv import load_dotenv

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_CAPTURAS = RAIZ_PROYECTO / "reports" / "screenshots"
PATRON_NOMBRE_PRUEBA = "Producto Selenium%"

load_dotenv(RAIZ_PROYECTO / ".env.test", override=True)

_MAPEO_VARIABLES_BASE_DATOS = {
    "MYSQL_HOST": "TEST_MYSQL_HOST",
    "MYSQL_PORT": "TEST_MYSQL_PORT",
    "MYSQL_DATABASE": "TEST_MYSQL_DATABASE",
    "MYSQL_USER": "TEST_MYSQL_USER",
    "MYSQL_PASSWORD": "TEST_MYSQL_PASSWORD",
}

for variable_app, variable_test in _MAPEO_VARIABLES_BASE_DATOS.items():
    valor_prueba = os.environ.get(variable_test)
    if valor_prueba is not None:
        os.environ[variable_app] = valor_prueba


@pytest.fixture(scope="session", autouse=True)
def usuario_selenium_preparado():
    from scripts.crear_usuario_prueba import preparar_usuario

    usuario = os.environ["TEST_LOGIN_USER"]
    password = os.environ["TEST_LOGIN_PASSWORD"]

    assert preparar_usuario(
        usuario, password
    ), "No fue posible preparar el usuario de pruebas Selenium en la base de pruebas."


@pytest.fixture(scope="session")
def live_server():
    from werkzeug.serving import make_server

    from app import create_app

    base_url = os.environ.get("TEST_BASE_URL", "http://127.0.0.1:5001")
    partes = urlparse(base_url)
    host = partes.hostname or "127.0.0.1"
    puerto = partes.port or 5001

    flask_app = create_app()
    servidor = make_server(host, puerto, flask_app)
    hilo = threading.Thread(target=servidor.serve_forever, daemon=True)
    hilo.start()

    yield base_url

    servidor.shutdown()
    hilo.join(timeout=5)


@pytest.fixture
def driver():
    navegador = os.environ.get("SELENIUM_BROWSER", "chrome").lower()
    headless = os.environ.get("SELENIUM_HEADLESS", "false").lower() == "true"

    if navegador == "edge":
        from selenium.webdriver import Edge, EdgeOptions

        opciones = EdgeOptions()
        if headless:
            opciones.add_argument("--headless=new")
        conductor = Edge(options=opciones)
    else:
        from selenium.webdriver import Chrome, ChromeOptions

        opciones = ChromeOptions()
        if headless:
            opciones.add_argument("--headless=new")
        conductor = Chrome(options=opciones)

    conductor.set_window_size(1280, 800)

    yield conductor

    conductor.quit()


@pytest.fixture
def sesion_iniciada(live_server, driver):
    from pages.login_page import LoginPage

    LoginPage(driver, live_server).iniciar_sesion(
        os.environ["TEST_LOGIN_USER"], os.environ["TEST_LOGIN_PASSWORD"]
    ).esperar_redireccion_a_productos()

    return driver


@pytest.fixture
def nombre_evidencia():
    return {"valor": None}


def _eliminar_productos_prueba():
    from database import obtener_conexion

    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM productos WHERE nombre LIKE %s", (PATRON_NOMBRE_PRUEBA,)
        )
        conexion.commit()
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()


@pytest.fixture(autouse=True)
def limpiar_productos_prueba():
    _eliminar_productos_prueba()
    yield
    _eliminar_productos_prueba()


def _guardar_captura(conductor, nombre):
    CARPETA_CAPTURAS.mkdir(parents=True, exist_ok=True)
    nombre_archivo = "".join(
        caracter if caracter.isalnum() or caracter in ("_", "-") else "_"
        for caracter in nombre
    )
    ruta = CARPETA_CAPTURAS / f"{nombre_archivo}.png"
    try:
        conductor.save_screenshot(str(ruta))
    except Exception:
        pass
    return ruta


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    if call.when == "call":
        import pytest_html
        from pytest_html.fixtures import extras_stash_key

        conductor = item.funcargs.get("driver")
        if conductor is not None:
            evidencia = item.funcargs.get("nombre_evidencia")
            nombre = (
                evidencia["valor"]
                if evidencia and evidencia.get("valor")
                else item.name
            )
            ruta_captura = _guardar_captura(conductor, nombre)
            if ruta_captura.exists():
                contenido_base64 = base64.b64encode(
                    ruta_captura.read_bytes()
                ).decode("ascii")
                if extras_stash_key not in item.config.stash:
                    item.config.stash[extras_stash_key] = []
                item.config.stash[extras_stash_key].append(
                    pytest_html.extras.image(contenido_base64, name=nombre)
                )

    yield
