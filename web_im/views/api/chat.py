import sqlalchemy.exc
from flask import Blueprint, session, jsonify, request
from web_im.exts import db
from web_im.models.user import ContactRelation
from web_im.models.chat import Message, UnreadMessageCount


bp = Blueprint("chat", __name__, url_prefix="/api/chat")


@bp.route("/send_message/<int:recipient_id>", methods=["POST"])
def send_message(recipient_id):
    # TODO: use errorhandler for "user not login"
    if "user_id" not in session:
        return jsonify({"error": 1003, "error_msg": "login first"})

    sender_id = session["user_id"]

    if not ContactRelation.is_contact(sender_id, recipient_id):
        return jsonify({"error": 1005, "error_msg": "join user first"})

    body = request.values.get("body")
    Message.create(
        sender_id,
        recipient_id,
        body,
    )
    UnreadMessageCount.add_unread(sender_id, recipient_id)
    # TODO update unread count
    return jsonify({"error": 0})


@bp.route("/delete_message", methods=["POST"])
def delete_message():
    # TODO: use errorhandler for "user not login"
    # TODO: buggy on unread count
    if "user_id" not in session:
        return jsonify({"error": 1003, "error_msg": "login first"})

    sender_id = session["user_id"]
    message_id = int(request.values.get("message_id"))
    Message.delete(sender_id, message_id)

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()

    return jsonify({"error": 0})
