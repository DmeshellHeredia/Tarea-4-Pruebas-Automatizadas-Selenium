import mysql.connector
from mysql.connector import Error

from config import Config


def obtener_conexion():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE,
    )


def verificar_conexion():
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        return True, "Conexión con la base de datos exitosa."
    except Error:
        return False, (
            "No se pudo conectar a la base de datos. Verifica que MySQL "
            "esté disponible y que el archivo .env esté configurado correctamente."
        )
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()


def crear_producto(nombre, precio, cantidad, categoria):
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            """
            INSERT INTO productos (
                nombre,
                precio,
                cantidad,
                categoria
            )
            VALUES (%s, %s, %s, %s)
            """,
            (nombre, precio, cantidad, categoria),
        )
        conexion.commit()
        return True, None
    except Error:
        if conexion is not None:
            conexion.rollback()
        return False, (
            "No fue posible registrar el producto. Revisa los datos ingresados."
        )
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()


def obtener_productos():
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                id,
                nombre,
                precio,
                cantidad,
                categoria,
                created_at,
                updated_at
            FROM productos
            ORDER BY id ASC
            """
        )
        productos = cursor.fetchall()
        return productos, None
    except Error:
        return [], (
            "No se pudo obtener el listado de productos. Verifica que MySQL "
            "esté disponible e inténtalo nuevamente."
        )
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()


def obtener_producto_por_id(producto_id):
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                id,
                nombre,
                precio,
                cantidad,
                categoria,
                created_at,
                updated_at
            FROM productos
            WHERE id = %s
            """,
            (producto_id,),
        )
        producto = cursor.fetchone()
        return producto, None
    except Error:
        return None, "No fue posible obtener la información del producto."
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()


def actualizar_producto(producto_id, nombre, precio, cantidad, categoria):
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            """
            UPDATE productos
            SET
                nombre = %s,
                precio = %s,
                cantidad = %s,
                categoria = %s
            WHERE id = %s
            """,
            (nombre, precio, cantidad, categoria, producto_id),
        )
        if cursor.rowcount > 0:
            conexion.commit()
            return True, None

        cursor.execute(
            "SELECT id FROM productos WHERE id = %s",
            (producto_id,),
        )
        if cursor.fetchone() is not None:
            conexion.commit()
            return True, "unchanged"

        conexion.rollback()
        return False, "not_found"
    except Error:
        if conexion is not None:
            conexion.rollback()
        return False, "database_error"
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()


def eliminar_producto(producto_id):
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM productos WHERE id = %s",
            (producto_id,),
        )
        if cursor.rowcount > 0:
            conexion.commit()
            return True, None

        conexion.rollback()
        return False, "not_found"
    except Error:
        if conexion is not None:
            conexion.rollback()
        return False, "database_error"
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()


def obtener_usuario_por_nombre(usuario):
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, usuario, password_hash FROM usuarios WHERE usuario = %s",
            (usuario,),
        )
        return cursor.fetchone()
    except Error:
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()


def crear_usuario(usuario, password_hash):
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            """
            INSERT INTO usuarios (usuario, password_hash)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE password_hash = VALUES(password_hash)
            """,
            (usuario, password_hash),
        )
        conexion.commit()
        return True
    except Error:
        if conexion is not None:
            conexion.rollback()
        return False
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()
