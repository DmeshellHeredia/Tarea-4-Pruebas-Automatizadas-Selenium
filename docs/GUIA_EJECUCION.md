# Guía de ejecución — Tarea 4

Pasos reproducibles para instalar, configurar y ejecutar el proyecto y su
suite de pruebas Selenium desde cero.

## 1. Preparación de Python

1. Instala Python 3.10 o superior.
2. Verifica la versión:
   ```
   python --version
   ```
3. Clona el repositorio y entra a la carpeta del proyecto:
   ```
   git clone https://github.com/DmeshellHeredia/Tarea-4-Pruebas-Automatizadas-Selenium.git
   cd Tarea-4-Pruebas-Automatizadas-Selenium
   ```
4. Crea y activa un entorno virtual:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

## 2. Instalación de `requirements.txt`

```
pip install -r requirements.txt
```

Esto instala Flask, mysql-connector-python, python-dotenv, Selenium, pytest y
pytest-html en las versiones fijadas en el archivo.

## 3. Creación de las bases de datos

Con MySQL 8 en ejecución, ejecuta ambos scripts con tu cliente preferido
(MySQL Workbench, `mysql` CLI, etc.):

```
database/schema.sql        -- crea tarea4_selenium
database/schema_test.sql   -- crea tarea4_selenium_test
```

Ambas bases son independientes y contienen las tablas `productos` y
`usuarios`.

## 4. Configuración de variables de entorno

```
copy .env.example .env
copy .env.test.example .env.test
```

Edita ambos archivos con tus propios valores locales (host, puerto, usuario y
contraseña de MySQL, navegador, modo headless, credenciales del usuario de
pruebas). **Nunca** coloques una contraseña real en `.env.example` ni en
`.env.test.example` — esos archivos son solo plantillas y sí se versionan.

## 5. Preparación del usuario de pruebas

Con `.env` apuntando a la base sobre la que quieras crear el usuario (normal
o de pruebas, según lo que necesites probar manualmente):

```
python scripts/crear_usuario_prueba.py
```

El script toma `TEST_LOGIN_USER` y `TEST_LOGIN_PASSWORD` del entorno activo,
genera el hash con `generate_password_hash()` y lo guarda en la tabla
`usuarios`. Es seguro ejecutarlo varias veces (actualiza el hash existente).

## 6. Inicio manual de la aplicación

```
python app.py
```

Abre `http://127.0.0.1:5000/login` e inicia sesión con el usuario que
preparaste en el paso anterior.

## 7. Ejecución completa de pytest

```
pytest -v --html=reports/report.html --self-contained-html
```

Esto ejecuta las 16 pruebas (15 funcionales + 1 de infraestructura), levanta
un servidor Flask controlado en el puerto 5001 contra `tarea4_selenium_test`,
genera capturas en `reports/screenshots/` y produce `reports/report.html`.

## 8. Ejecución headless

En tu `.env.test`:
```
SELENIUM_HEADLESS=true
```

Útil para correr la suite sin ventanas visibles (por ejemplo, en un entorno
sin pantalla).

## 9. Ejecución visible

En tu `.env.test`:
```
SELENIUM_HEADLESS=false
```

Necesario para grabar el video demostrativo, ya que el navegador debe verse
en pantalla durante la ejecución.

## 10. Selección entre Chrome y Edge

En tu `.env.test`:
```
SELENIUM_BROWSER=chrome
```
o
```
SELENIUM_BROWSER=edge
```

Selenium Manager descarga y gestiona el driver correspondiente
automáticamente; no se necesita configurar ninguna ruta manual.

## 11. Generación y apertura del reporte

El comando del paso 7 ya genera `reports/report.html`. Ábrelo haciendo doble
clic o con:
```
start reports/report.html
```
Es autocontenido: funciona sin conexión a internet y las capturas están
embebidas directamente en el archivo.

## 12. Solución de problemas básicos

- **"No se pudo conectar a la base de datos"**: confirma que el servicio de
  MySQL esté activo y que `.env`/`.env.test` tengan la contraseña correcta.
- **El navegador no abre / falla el driver**: confirma que Chrome o Edge esté
  instalado y que `SELENIUM_BROWSER` coincida con el navegador disponible.
- **Puerto 5001 ocupado**: verifica que no haya una ejecución anterior de
  pytest colgada; cierra procesos `python`/`chromedriver` residuales.
- **Las pruebas fallan por elementos no encontrados**: revisa que la
  aplicación no haya cambiado los `id`/`data-testid` esperados por los Page
  Objects en `pages/`.
- **El reporte no muestra capturas**: confirma que `reports/screenshots/`
  exista y tenga permisos de escritura; el hook de `tests/conftest.py` las
  crea automáticamente si la carpeta está disponible.
