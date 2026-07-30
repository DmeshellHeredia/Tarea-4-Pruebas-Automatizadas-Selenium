from flask import Flask, flash, redirect, render_template, request, url_for

from config import Config
from database import (
    actualizar_producto,
    crear_producto,
    eliminar_producto,
    obtener_producto_por_id,
    obtener_productos,
    verificar_conexion,
)
from validators import validar_datos_producto

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY


@app.route("/")
def inicio():
    conexion_ok, mensaje_conexion = verificar_conexion()
    return render_template(
        "index.html", conexion_ok=conexion_ok, mensaje_conexion=mensaje_conexion
    )


@app.route("/productos", methods=["GET"])
def listar_productos():
    productos, error = obtener_productos()
    return render_template("productos.html", productos=productos, error=error)


@app.route("/productos/nuevo", methods=["GET", "POST"])
def registrar_producto():
    valores = {"nombre": "", "precio": "", "cantidad": "", "categoria": ""}
    errores = {}

    if request.method == "POST":
        valores["nombre"] = request.form.get("nombre", "")
        valores["precio"] = request.form.get("precio", "")
        valores["cantidad"] = request.form.get("cantidad", "")
        valores["categoria"] = request.form.get("categoria", "")

        datos_limpios, errores = validar_datos_producto(valores)

        if not errores:
            exito, error_creacion = crear_producto(
                datos_limpios["nombre"],
                datos_limpios["precio"],
                datos_limpios["cantidad"],
                datos_limpios["categoria"],
            )
            if exito:
                flash("Producto registrado correctamente.", "exito")
                return redirect(url_for("listar_productos"))

            flash(error_creacion, "error")

    return render_template("productos_nuevo.html", valores=valores, errores=errores)


@app.route("/productos/<int:producto_id>/editar", methods=["GET", "POST"])
def editar_producto(producto_id):
    producto, error = obtener_producto_por_id(producto_id)

    if error:
        flash(error, "error")
        return redirect(url_for("listar_productos"))

    if producto is None:
        flash("El producto solicitado no existe.", "error")
        return redirect(url_for("listar_productos"))

    valores = {
        "nombre": producto["nombre"],
        "precio": str(producto["precio"]),
        "cantidad": str(producto["cantidad"]),
        "categoria": producto["categoria"],
    }
    errores = {}

    if request.method == "POST":
        valores["nombre"] = request.form.get("nombre", "")
        valores["precio"] = request.form.get("precio", "")
        valores["cantidad"] = request.form.get("cantidad", "")
        valores["categoria"] = request.form.get("categoria", "")

        datos_limpios, errores = validar_datos_producto(valores)

        if not errores:
            exito, resultado = actualizar_producto(
                producto_id,
                datos_limpios["nombre"],
                datos_limpios["precio"],
                datos_limpios["cantidad"],
                datos_limpios["categoria"],
            )
            if exito:
                if resultado == "unchanged":
                    flash("No se realizaron cambios en el producto.", "exito")
                else:
                    flash("Producto actualizado correctamente.", "exito")
                return redirect(url_for("listar_productos"))

            if resultado == "not_found":
                flash("El producto solicitado no existe.", "error")
                return redirect(url_for("listar_productos"))

            flash(
                "No fue posible actualizar el producto. Revisa los datos ingresados.",
                "error",
            )

    return render_template(
        "productos_editar.html",
        valores=valores,
        producto_id=producto_id,
        errores=errores,
    )


@app.route("/productos/<int:producto_id>/eliminar", methods=["POST"])
def eliminar_producto_ruta(producto_id):
    exito, resultado = eliminar_producto(producto_id)

    if exito:
        flash("Producto eliminado correctamente.", "exito")
    elif resultado == "not_found":
        flash("El producto solicitado no existe.", "error")
    else:
        flash("No fue posible eliminar el producto.", "error")

    return redirect(url_for("listar_productos"))


@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def error_interno(error):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
