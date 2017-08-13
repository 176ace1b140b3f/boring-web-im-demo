import sqlalchemy.exc
from flask import Blueprint, session, jsonify, request
from web_im.models.user import User

bp = Blueprint("user", __name__, url_prefix="/api/user")


@bp.route("/register")
def register():
    # TODO: POST only
    username = request.values.get("username")
    password = request.values.get("password")

    try:
        user_id = User.create(username, password)
    except sqlalchemy.exc.IntegrityError:
        return jsonify({
            "error": 1001,
            "error_msg": "duplicated",
        })
    except BaseException:
        return jsonify({
            "error": 1000,
            "error_msg": "unknown",
        })

    return jsonify({"error": 0, "user_id": user_id})


@bp.route("/login")
def login():
    # TODO: POST only
    username = request.values.get("username")
    password = request.values.get("password")
    uid = User.login_challenge(username, password)
    if uid is None:
        session.pop("user_id", None)
        return jsonify({"error": 1002, "error_msg": "failed"})
    else:
        session["user_id"] = uid
        return jsonify({"error": 0})


@bp.route("/logout")
def logout():
    # TODO: csrf
    session.pop("user_id", None)
    return jsonify({"error": 0})
