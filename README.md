# Tarea 4 - Pruebas Automatizadas con Selenium

## Descripción

Proyecto individual que automatiza, con Selenium WebDriver y pytest, el flujo de
inicio de sesión y las operaciones CRUD (crear, consultar, actualizar, eliminar)
de un catálogo de productos construido con Flask y MySQL.

## Objetivo académico

Aplicar pruebas automatizadas con Selenium sobre una aplicación web propia,
cubriendo camino feliz, prueba negativa y prueba de límites para cada historia
de usuario, con reporte HTML autocontenido y capturas automáticas por escenario,
como parte de la asignatura Programación III.

## Tecnologías utilizadas

- Python
- Flask
- MySQL 8
- mysql-connector-python
- python-dotenv
- Selenium WebDriver (Selenium Manager, sin drivers descargados manualmente)
- pytest
- pytest-html
- Werkzeug (hash de contraseñas)
- HTML y CSS

## Estructura principal del repositorio

```
Tarea-4-Pruebas-Automatizadas-Selenium/
├── app.py                     # Aplicacion Flask (rutas, create_app())
├── auth.py                    # Decorador login_required
├── config.py                  # Configuracion via variables de entorno
├── database.py                # Acceso a MySQL (productos, usuarios)
├── validators.py              # Validaciones de negocio de productos
├── requirements.txt
├── pytest.ini
├── .env.example / .env.test.example
├── database/
│   ├── schema.sql             # Base normal (tarea4_selenium)
│   └── schema_test.sql        # Base de pruebas (tarea4_selenium_test)
├── templates/                 # Vistas Jinja2 (login, productos, base, errores)
├── static/css/styles.css
├── scripts/
│   └── crear_usuario_prueba.py
├── pages/                     # Page Object Model
│   ├── login_page.py
│   ├── products_page.py
│   └── product_form_page.py
├── tests/                     # Suite Selenium + pytest
│   ├── conftest.py
│   ├── test_infraestructura_selenium.py
│   ├── test_login.py
│   ├── test_create_product.py
│   ├── test_read_products.py
│   ├── test_update_product.py
│   └── test_delete_product.py
├── reports/
│   ├── report.html
│   └── screenshots/
└── docs/
    ├── MATRIZ_TRAZABILIDAD.md
    ├── GUIA_EJECUCION.md
    └── GUION_VIDEO.md
```

## Requisitos previos

- Python 3.10 o superior.
- MySQL 8 instalado y en ejecución.
- Google Chrome o Microsoft Edge instalado (Selenium Manager resuelve el driver
  automáticamente, sin necesidad de descargarlo).

## Instalación

```
git clone https://github.com/DmeshellHeredia/Tarea-4-Pruebas-Automatizadas-Selenium.git
cd Tarea-4-Pruebas-Automatizadas-Selenium
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración de MySQL

Verifica que el servicio de MySQL 8 esté activo y que tengas un usuario con
permisos para crear bases de datos (por ejemplo `root`).

## Creación de `tarea4_selenium` (base normal)

1. Ejecuta el script `database/schema.sql` con tu cliente de MySQL preferido.
2. Verifica que exista la base `tarea4_selenium` con las tablas `productos` y
   `usuarios`.

## Creación de `tarea4_selenium_test` (base de pruebas)

1. Ejecuta el script `database/schema_test.sql`.
2. Verifica que exista la base `tarea4_selenium_test`, completamente
   independiente de la base normal, con las mismas tablas.

## Configuración de `.env`

```
copy .env.example .env
```

Edita `.env` y coloca tu contraseña real de MySQL en `MYSQL_PASSWORD`, además
de una clave propia en `FLASK_SECRET_KEY`. Este archivo nunca debe subirse al
repositorio (ya está en `.gitignore`).

## Configuración de `.env.test`

```
copy .env.test.example .env.test
```

Edita `.env.test` con los datos de conexión a `tarea4_selenium_test`, la URL
del servidor de pruebas (`TEST_BASE_URL=http://127.0.0.1:5001`), el navegador
(`SELENIUM_BROWSER=chrome` o `edge`), el modo (`SELENIUM_HEADLESS=true/false`) y
las credenciales del usuario Selenium (`TEST_LOGIN_USER`, `TEST_LOGIN_PASSWORD`).
Tampoco debe subirse al repositorio.

## Creación del usuario de pruebas

Con `.env` apuntando a la base deseada, ejecuta:

```
python scripts/crear_usuario_prueba.py
```

El script lee `TEST_LOGIN_USER`/`TEST_LOGIN_PASSWORD` del entorno activo y
crea (o actualiza) el usuario con la contraseña cifrada mediante
`generate_password_hash()`. Nunca imprime la contraseña en consola.

## Ejecución de la aplicación

```
python app.py
```

Disponible en `http://127.0.0.1:5000`. Todas las rutas de productos requieren
iniciar sesión primero en `/login`.

## Ejecución de todas las pruebas

```
pytest -v --html=reports/report.html --self-contained-html
```

## Ejecución por marcador

```
pytest -m login          # Solo HU-01
pytest -m create         # Solo HU-02
pytest -m read           # Solo HU-03
pytest -m update         # Solo HU-04
pytest -m delete         # Solo HU-05
pytest -m happy          # Solo caminos felices
pytest -m negative       # Solo pruebas negativas
pytest -m boundary       # Solo pruebas de limites
pytest -m smoke          # Solo la prueba de infraestructura
```

## Generación del reporte HTML

El comando de ejecución completa ya genera `reports/report.html` de forma
autocontenida (capturas embebidas en base64, abre sin conexión a internet).

## Ubicación de las capturas

`reports/screenshots/`, con un archivo por escenario (`HU01_login_feliz.png`,
`HU02_crear_negativo.png`, etc.), generado automáticamente por un hook de
pytest en cada ejecución, tanto si la prueba pasa como si falla.

## Arquitectura Page Object Model

- `pages/login_page.py`: interacciones con el formulario de login.
- `pages/products_page.py`: listado de productos, alertas de confirmación,
  lectura de filas por selectores dinámicos (`data-testid`).
- `pages/product_form_page.py`: formulario de creación/edición de productos.

Las pruebas (`tests/`) solo orquestan escenarios y aserciones; toda la
interacción con Selenium vive en los Page Objects.

## Separación entre la base normal y la base de pruebas

`tests/conftest.py` carga `.env.test` y remapea las variables `MYSQL_*` para
que la aplicación bajo prueba use exclusivamente `tarea4_selenium_test`,
corriendo en un servidor Flask controlado (puerto 5001) durante la sesión de
pytest. La aplicación ejecutada manualmente (`python app.py`, puerto 5000)
sigue usando `tarea4_selenium` a través del `.env` normal. Ambas bases nunca
se mezclan.

## Historias de usuario cubiertas

- HU-01: Inicio de sesión.
- HU-02: Registrar producto.
- HU-03: Consultar productos.
- HU-04: Actualizar producto.
- HU-05: Eliminar producto.

Documentadas con criterios de aceptación y rechazo en Jira (ver enlace abajo).

## Pruebas funcionales (15) + prueba técnica de humo (1)

Ver detalle completo, marcadores y capturas en
[`docs/MATRIZ_TRAZABILIDAD.md`](docs/MATRIZ_TRAZABILIDAD.md).

| # | Historia | Escenario | Prueba |
|---|---|---|---|
| 1 | HU-01 | Camino feliz | `test_hu01_login_valido` |
| 2 | HU-01 | Negativo | `test_hu01_login_credenciales_invalidas` |
| 3 | HU-01 | Límites | `test_hu01_login_campos_vacios` |
| 4 | HU-02 | Camino feliz | `test_hu02_crear_producto_valido` |
| 5 | HU-02 | Negativo | `test_hu02_crear_producto_invalido` |
| 6 | HU-02 | Límites | `test_hu02_crear_producto_valores_limite` |
| 7 | HU-03 | Camino feliz | `test_hu03_consultar_producto_existente` |
| 8 | HU-03 | Negativo | `test_hu03_consultar_sin_autenticacion` |
| 9 | HU-03 | Límites | `test_hu03_consultar_unico_producto_con_valores_limite` |
| 10 | HU-04 | Camino feliz | `test_hu04_actualizar_producto_valido` |
| 11 | HU-04 | Negativo | `test_hu04_actualizar_producto_invalido` |
| 12 | HU-04 | Límites | `test_hu04_actualizar_producto_valores_limite` |
| 13 | HU-05 | Camino feliz | `test_hu05_eliminar_producto_confirmado` |
| 14 | HU-05 | Negativo | `test_hu05_cancelar_eliminacion` |
| 15 | HU-05 | Límites | `test_hu05_eliminar_unico_producto` |

## Enlaces

- Repositorio: https://github.com/DmeshellHeredia/Tarea-4-Pruebas-Automatizadas-Selenium
- Historias de usuario (Jira): https://michaelheredia60.atlassian.net/jira/software/projects/T4SEL/boards/34/backlog
- Video demostrativo: PENDIENTE_ENLACE_VIDEO

## Consideraciones de seguridad

- Las contraseñas de MySQL y del usuario de pruebas se almacenan únicamente en
  `.env`/`.env.test`, ambos ignorados por Git y nunca versionados.
- Las contraseñas de aplicación se guardan siempre como hash
  (`generate_password_hash()`/`check_password_hash()`), nunca en texto plano.
- El reporte HTML y las capturas no contienen contraseñas, hashes ni rutas
  personales del equipo de desarrollo.
- Nunca publiques tu `.env` ni `.env.test` reales.

## Autor

Michael Heredia — matrícula: 2024-0063
