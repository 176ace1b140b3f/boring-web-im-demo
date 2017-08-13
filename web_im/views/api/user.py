import sqlalchemy.exc
from flask import Blueprint, session, jsonify, request
from web_im.models.user import User, ContactRelation

bp = Blueprint("user", __name__, url_prefix="/api/user")


@bp.route("/register", methods=['POST'])
def register():
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


@bp.route("/login", methods=['POST'])
def login():
    username = request.values.get("username")
    password = request.values.get("password")
    uid = User.login_challenge(username, password)
    if uid is None:
        session.pop("user_id", None)
        return jsonify({"error": 1002, "error_msg": "failed"})
    else:
        session["user_id"] = uid
        return jsonify({"error": 0})


@bp.route("/logout", methods=['POST'])
def logout():
    session.pop("user_id", None)
    return jsonify({"error": 0})


@bp.route("/connect", methods=['POST'])
def connect():
    username = request.values.get("username")

    if "user_id" not in session:
        return jsonify({"error": 1003, "error_msg": "login first"})

    target_user = User.get_by_name(username)
    if target_user is None:
        return jsonify({"error": 1004, "error_msg": "user not found"})

    ContactRelation.connect(session["user_id"], target_user.id)
    return jsonify({"error": 0})


@bp.route("/disconnect", methods=['POST'])
def disconnect():
    user_id = request.values.get("user_id")

    if "user_id" not in session:
        return jsonify({"error": 1003, "error_msg": "login first"})

    target_user = User.get(user_id)
    if target_user is None:
        return jsonify({"error": 1004, "error_msg": "user not found"})

    ContactRelation.disconnect(session["user_id"], target_user.id)
    return jsonify({"error": 0})
