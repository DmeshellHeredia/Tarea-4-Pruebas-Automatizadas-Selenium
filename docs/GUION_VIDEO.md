# Guion del video demostrativo — paso a paso literal

Sigue esto en orden exacto. No hay decisiones que tomar: cada paso indica
qué hacer y, cuando aplica, la frase exacta a decir. Duración estimada:
6 a 10 minutos. Publicar en YouTube (público) o OneDrive (acceso abierto)
— nunca Google Drive.

---

## Antes de darle "grabar"

### 1. Ubícate en la carpeta del proyecto

```
cd "C:\Users\micha\OneDrive\Desktop\basura\TAREA\P3\Unidad 6\Tarea-4-Pruebas-Automatizadas-Selenium\Tarea-4-Pruebas-Automatizadas-Selenium"
```

### 2. Activa el entorno virtual

```
venv\Scripts\activate
```

Confirma que aparece `(venv)` al inicio de la línea.

### 3. Confirma que MySQL está activo

Servicio `MySQL84` debe estar "En ejecución" (`services.msc`).

### 4. Configura el modo visible

Abre `.env.test`:
```
notepad .env.test
```
Busca la línea:
```
SELENIUM_HEADLESS=true
```
Cámbiala a:
```
SELENIUM_HEADLESS=false
```
Deja `SELENIUM_BROWSER=chrome` sin tocar (o `edge`, si prefieres grabar con
ese navegador). Guarda con `Ctrl+S` y cierra el Bloc de notas.

### 5. Confirma el usuario de pruebas

```
python scripts/crear_usuario_prueba.py
```
Debe imprimir: `Usuario de prueba 'selenium_user' preparado correctamente.`

### 6. Abre estas pestañas del navegador, en este orden, ANTES de grabar

1. `https://github.com/DmeshellHeredia/Tarea-4-Pruebas-Automatizadas-Selenium`
2. `https://michaelheredia60.atlassian.net/jira/software/projects/T4SEL/boards/34/backlog`
3. Una pestaña en blanco (para abrir `reports/report.html` más adelante).

### 7. Ten la terminal abierta

Ya ubicada en la carpeta del proyecto, con `(venv)` activo, lista para
escribir el siguiente comando (no lo ejecutes todavía).

---

## Grabación

### Escena 1 — Presentación (0:00 - 0:30)

**Haz:** cámara/pantalla en blanco o en el escritorio.

**Di exactamente:**
> "Hola, soy Michael Heredia. Esta es la Tarea 4 de Programación III: pruebas
> automatizadas con Selenium sobre un CRUD de productos con Flask y MySQL,
> incluyendo inicio de sesión."

### Escena 2 — Repositorio público (0:30 - 1:15)

**Haz:** cambia a la pestaña 1 (GitHub).

**Di:**
> "Este es el repositorio público del proyecto en GitHub."

Mueve el cursor (sin hacer clic) sobre `app.py`, la carpeta `pages/`, la
carpeta `tests/`, la carpeta `reports/` y la carpeta `docs/`.

### Escena 3 — Organización del código (1:15 - 2:15)

**Haz:** haz clic y abre `pages/login_page.py` (3-5 segundos), luego
`tests/conftest.py` (3-5 segundos).

**Di:**
> "En la carpeta `pages` está el Page Object Model: login, listado de
> productos y formulario de producto. En `tests` están las dieciséis
> pruebas automatizadas, incluyendo el servidor de pruebas controlado y la
> limpieza automática de datos."

### Escena 4 — Proyecto de Jira (2:15 - 3:00)

**Haz:** cambia a la pestaña 2 (Jira).

**Di:**
> "Aquí está el tablero de Jira con las cinco historias de usuario."

Muestra las 5 historias (HU-01 a HU-05) en la columna "Done".

### Escena 5 — Criterios de una historia (3:00 - 4:00)

**Haz:** haz clic en la historia HU-02 (Registrar producto) para abrirla.

**Di:**
> "Cada historia tiene sus criterios de aceptación, sus criterios de
> rechazo, y sus tres escenarios de prueba: camino feliz, prueba negativa y
> prueba de límites."

Desplázate dentro de la historia para mostrar esas tres secciones.

### Escena 6 — Preparar la ejecución (4:00 - 4:20)

**Haz:** cambia a la terminal.

**Di:**
> "Ahora voy a ejecutar las dieciséis pruebas con el navegador visible."

### Escena 7 — Ejecución en vivo (4:20 - 7:00)

**Haz:** escribe y ejecuta exactamente:
```
pytest -v --html=reports/report.html --self-contained-html
```

Deja que el navegador se vea actuando. Mientras corre, di brevemente (una
sola frase corta cada vez, sin detener la grabación):

- Cuando veas la pantalla de login: **di:** "Esto es el camino feliz de
  inicio de sesión."
- Cuando veas un mensaje de error en un formulario de producto: **di:**
  "Esta es una prueba negativa, con datos inválidos."
- Cuando veas un producto con valores muy grandes (nombre largo, precio
  99999999.99): **di:** "Y esta es una prueba de límites, con los valores
  máximos permitidos."

### Escena 8 — Resultado final (7:00 - 7:20)

**Haz:** señala con el cursor la última línea de la terminal.

**Di:**
> "Las dieciséis pruebas terminaron correctamente: dieciséis passed."

(La terminal mostrará literalmente `16 passed`.)

### Escena 9 — Reporte HTML (7:20 - 8:10)

**Haz:** cambia a la pestaña 3 y ejecuta:
```
start reports/report.html
```

**Di:**
> "Este es el reporte HTML autocontenido, con las dieciséis pruebas y sus
> capturas."

Haz clic en una fila del reporte para expandir su captura embebida.

### Escena 10 — Capturas (8:10 - 8:40)

**Haz:** abre el explorador de archivos:
```
explorer reports\screenshots
```

**Di:**
> "Y aquí están las dieciséis capturas automáticas, una por cada
> escenario."

### Escena 11 — Cierre (8:40 - 9:00)

**Di exactamente:**
> "Con esto se completan las cinco historias de usuario, las quince pruebas
> funcionales más la prueba de infraestructura, con reporte HTML y capturas
> automáticas. Gracias."

### 12. Detén la grabación.

---

## Después de grabar

1. Sube el archivo a YouTube (visibilidad **Público**) o a OneDrive
   (enlace **"Cualquier persona con el enlace"**). Nunca Google Drive.
2. Copia el enlace final.
3. Pruébalo en una ventana de incógnito antes de entregarlo.
4. Pega el enlace en el chat para que se incorpore a `README.md` y al texto
   de entrega.

**Nota:** la grabación y publicación del video las realiza el estudiante
personalmente.
