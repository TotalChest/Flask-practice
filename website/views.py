from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json


views = Blueprint('views', __name__)


@views.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        note = request.form.get('note')
        new_note = Note(user_id=current_user.id, data=note)
        db.session.add(new_note)
        db.session.commit()
    return render_template("home.html", user=current_user)


@views.route("/delete-note", methods=["POST"])
def delete_note():
    note_id = json.loads(request.data)['noteId']
    note = Note.query.get(note_id)
    if note and current_user.is_authenticated:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonfy({})