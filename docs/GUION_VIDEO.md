# Guion del video demostrativo — Tarea 4

Duración objetivo: 6 a 10 minutos. Grabar con el navegador visible
(`SELENIUM_HEADLESS=false`). Publicar en YouTube o OneDrive (no Google
Drive), con acceso público o abierto para el profesor y el monitor.

## 0. Preparación previa (no grabada)

- Limpiar datos de prueba manuales si los hubiera.
- Confirmar `.env`/`.env.test` configurados localmente (sin mostrarlos en
  pantalla durante la grabación).
- Confirmar `SELENIUM_HEADLESS=false` y el navegador deseado en
  `SELENIUM_BROWSER`.
- Tener abiertas de antemano las pestañas: repositorio de GitHub, tablero de
  Jira, y la terminal en la carpeta del proyecto.

## 1. Presentación breve (30-45 s)

"Hola, soy Michael Heredia. Esta es la Tarea 4 de Programación III: pruebas
automatizadas con Selenium sobre un CRUD de productos con Flask y MySQL,
incluyendo inicio de sesión."

## 2. Repositorio público (30-45 s)

- Mostrar la URL del repositorio en GitHub.
- Recorrer brevemente la estructura de carpetas: `app.py`, `pages/`,
  `tests/`, `reports/`, `docs/`.

## 3. Organización del código (45-60 s)

- Mostrar `pages/login_page.py`, `pages/products_page.py`,
  `pages/product_form_page.py`: explicar que son el Page Object Model.
- Mostrar `tests/conftest.py`: servidor controlado, base de pruebas
  independiente, limpieza automática, fixture de sesión.

## 4. Proyecto de Jira (45-60 s)

- Abrir el tablero de Jira del proyecto.
- Mostrar las 5 historias (HU-01 a HU-05) y su estado.

## 5. Las cinco historias y sus criterios (60-90 s)

- Abrir al menos una historia (por ejemplo HU-02) y mostrar:
  - Criterios de aceptación.
  - Criterios de rechazo.
  - Los tres escenarios (feliz, negativo, límite) documentados.

## 6. Infraestructura Selenium (30-45 s)

- Mostrar `pytest.ini` (marcadores) y explicar brevemente
  `SELENIUM_BROWSER`/`SELENIUM_HEADLESS` en `.env.test`.

## 7. Ejecución visible de las pruebas (2-3 min)

- Ejecutar en terminal:
  ```
  pytest -v --html=reports/report.html --self-contained-html
  ```
- Dejar visible el navegador mientras corre al menos:
  - Un camino feliz (por ejemplo, login válido o crear producto válido).
  - Una prueba negativa (por ejemplo, credenciales inválidas o precio
    negativo).
  - Una prueba de límites (por ejemplo, valores máximos de producto).
- Narrar qué está pasando en cada una mientras el navegador actúa.

## 8. Resultado final en terminal (15-20 s)

- Mostrar la línea final: `16 passed`.

## 9. Reporte HTML (45-60 s)

- Abrir `reports/report.html` en el navegador.
- Mostrar la tabla de resultados con las 16 filas en "Passed".
- Expandir una fila para mostrar la captura embebida.

## 10. Capturas (20-30 s)

- Mostrar la carpeta `reports/screenshots/` con los 16 archivos PNG.

## 11. Cierre (15-20 s)

"Con esto se completan las 5 historias de usuario, las 15 pruebas
funcionales más la prueba de infraestructura, con reporte HTML y capturas
automáticas. Gracias."

---

**Nota:** este documento es únicamente el guion. La grabación y publicación
del video las realiza el estudiante personalmente; el video debe subirse a
YouTube (público) o a OneDrive (acceso abierto), nunca a Google Drive.
