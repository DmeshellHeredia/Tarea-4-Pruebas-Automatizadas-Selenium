import os
import sys

from werkzeug.security import generate_password_hash

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import crear_usuario  # noqa: E402


def preparar_usuario(usuario, password):
    password_hash = generate_password_hash(password)
    return crear_usuario(usuario, password_hash)


def main():
    usuario = os.getenv("TEST_LOGIN_USER")
    password = os.getenv("TEST_LOGIN_PASSWORD")

    if not usuario or not password:
        print(
            "Faltan las variables TEST_LOGIN_USER y/o TEST_LOGIN_PASSWORD "
            "en el entorno activo."
        )
        sys.exit(1)

    if preparar_usuario(usuario, password):
        print(f"Usuario de prueba '{usuario}' preparado correctamente.")
    else:
        print("No fue posible preparar el usuario de prueba.")
        sys.exit(1)


if __name__ == "__main__":
    main()
