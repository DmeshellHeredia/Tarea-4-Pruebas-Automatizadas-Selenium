# Tarea 4 - Pruebas Automatizadas con Selenium

## Objetivo

Proyecto individual de la asignatura Programación III que consiste en aplicar pruebas
automatizadas con Selenium WebDriver sobre una aplicación web propia con operaciones
CRUD e inicio de sesión.

## Aplicación CRUD base

Este repositorio parte del CRUD de productos desarrollado previamente en la Tarea 3
(Uso de Git y Git Flow), adaptado para esta nueva tarea. En esta etapa la aplicación
permite:

- Listar productos.
- Registrar productos.
- Editar productos.
- Eliminar productos mediante una solicitud POST con confirmación previa.
- Validar nombre, precio, cantidad y categoría.

La automatización con Selenium, el inicio de sesión y el resto de la infraestructura
de pruebas se agregarán en fases posteriores del proyecto; todavía no están
implementados en este punto.

## Tecnologías actuales

- Python
- Flask
- MySQL 8
- mysql-connector-python
- python-dotenv
- HTML y CSS

## Requisitos previos

- Python 3.10 o superior instalado.
- MySQL 8 instalado y en ejecución.
- Un cliente de MySQL (por ejemplo, MySQL Workbench).

## Instalación

1. Clonar el repositorio:

   ```
   git clone https://github.com/DmeshellHeredia/Tarea-4-Pruebas-Automatizadas-Selenium.git
   ```

2. Crear un entorno virtual:

   ```
   python -m venv venv
   ```

3. Activar el entorno virtual:

   En Windows:
   ```
   venv\Scripts\activate
   ```

   En Linux o Mac:
   ```
   source venv/bin/activate
   ```

4. Instalar las dependencias:

   ```
   pip install -r requirements.txt
   ```

## Configuración de MySQL y variables de entorno

1. Copiar el archivo de referencia para la base normal:

   ```
   copy .env.example .env
   ```

2. Editar `.env` y colocar la contraseña real de MySQL en `MYSQL_PASSWORD`.

3. Copiar el archivo de referencia para la base de pruebas:

   ```
   copy .env.test.example .env.test
   ```

4. Editar `.env.test` con los valores locales correspondientes.

Los archivos `.env` y `.env.test` no deben subirse al repositorio.

## Preparación de las dos bases de datos

Este proyecto utiliza dos bases de datos completamente independientes:

- `tarea4_selenium`: base normal para ejecución manual de la aplicación.
- `tarea4_selenium_test`: base exclusiva para pruebas automatizadas (se preparará en
  una fase posterior del proyecto).

Para crear la base normal:

1. Abrir MySQL Workbench o el cliente de MySQL de preferencia.
2. Ejecutar el script `database/schema.sql`.
3. Verificar que aparezca la base de datos `tarea4_selenium` y la tabla `productos`.

Para crear la base de pruebas:

1. Ejecutar el script `database/schema_test.sql`.
2. Verificar que aparezca la base de datos `tarea4_selenium_test` y la tabla
   `productos`.

## Ejecución manual

```
python app.py
```

La aplicación estará disponible en:

```
http://127.0.0.1:5000
```
