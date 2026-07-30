from functools import wraps

from flask import redirect, session, url_for


def login_required(vista):
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if not session.get("usuario_id"):
            return redirect(url_for("login"))
        return vista(*args, **kwargs)

    return envoltura
