from decimal import Decimal, InvalidOperation

LONGITUD_MAXIMA_NOMBRE = 100
LONGITUD_MAXIMA_CATEGORIA = 80
PRECIO_MAXIMO = Decimal("99999999.99")
CANTIDAD_MAXIMA = 2147483647


def _validar_nombre(valor):
    nombre = (valor or "").strip()
    if not nombre:
        return None, "El nombre es obligatorio."
    if len(nombre) > LONGITUD_MAXIMA_NOMBRE:
        return None, "El nombre no puede superar los 100 caracteres."
    return nombre, None


def _validar_categoria(valor):
    categoria = (valor or "").strip()
    if not categoria:
        return None, "La categoría es obligatoria."
    if len(categoria) > LONGITUD_MAXIMA_CATEGORIA:
        return None, "La categoría no puede superar los 80 caracteres."
    return categoria, None


def _validar_precio(valor):
    texto = (valor or "").strip()
    if not texto:
        return None, "El precio es obligatorio."

    try:
        precio = Decimal(texto)
    except InvalidOperation:
        return None, "El precio debe ser un número válido."

    if not precio.is_finite():
        return None, "El precio debe ser un número válido."

    if precio <= 0:
        return None, "El precio debe ser mayor que cero."

    exponente = precio.as_tuple().exponent
    if isinstance(exponente, int) and exponente < -2:
        return None, "El precio no puede tener más de dos decimales."

    if precio > PRECIO_MAXIMO:
        return None, "El precio no puede superar 99999999.99."

    return precio, None


def _validar_cantidad(valor):
    texto = (valor or "").strip()
    if not texto:
        return None, "La cantidad es obligatoria."

    try:
        cantidad = int(texto)
    except ValueError:
        return None, "La cantidad debe ser un número entero."

    if cantidad < 0:
        return None, "La cantidad no puede ser negativa."

    if cantidad > CANTIDAD_MAXIMA:
        return None, "La cantidad no puede superar 2147483647."

    return cantidad, None


def validar_datos_producto(datos):
    datos_limpios = {}
    errores = {}

    nombre, error_nombre = _validar_nombre(datos.get("nombre"))
    if error_nombre:
        errores["nombre"] = error_nombre
    else:
        datos_limpios["nombre"] = nombre

    precio, error_precio = _validar_precio(datos.get("precio"))
    if error_precio:
        errores["precio"] = error_precio
    else:
        datos_limpios["precio"] = precio

    cantidad, error_cantidad = _validar_cantidad(datos.get("cantidad"))
    if error_cantidad:
        errores["cantidad"] = error_cantidad
    else:
        datos_limpios["cantidad"] = cantidad

    categoria, error_categoria = _validar_categoria(datos.get("categoria"))
    if error_categoria:
        errores["categoria"] = error_categoria
    else:
        datos_limpios["categoria"] = categoria

    return datos_limpios, errores
