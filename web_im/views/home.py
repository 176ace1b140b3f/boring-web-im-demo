from flask import (
    Blueprint, session, render_template, redirect, url_for
)
from web_im.models.user import User
from web_im.models.chat import Message, UnreadMessageCount


bp = Blueprint("home", __name__)


@bp.route("/")
def home():
    user_id = session.get("user_id")
    if user_id is None:
        return render_template("login.jinja2")

    user = User.get(user_id)
    if user is None:
        session.pop("user_id")
        return render_template("login.jinja2")

    contacts = user.get_contacts()
    unread_counts = {
        contact_id: UnreadMessageCount.get_unread(contact_id, user_id)
        for contact_id, _ in contacts
    }
    return render_template(
        "index.jinja2",
        user=user,
        contacts=contacts,
        unread_counts=unread_counts,
    )


@bp.route("/chat/<int:contact_id>")
def chat(contact_id):
    # TODO xss check
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for(".home"))

    sender = User.get(user_id)
    recipient = User.get(contact_id)
    if recipient is None:
        return "Recipient not found"

    UnreadMessageCount.reset_unread(recipient.id, sender.id)
    messages = Message.get_many_by_user_pair(sender.id, recipient.id)

    name_dict = {
        sender.id: sender.name,
        recipient.id: recipient.name,
    }
    return render_template(
        "chat.jinja2",
        sender=sender,
        recipient=recipient,
        messages=messages,
        name_dict=name_dict,
    )
