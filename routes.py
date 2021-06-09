from app import app
from db import db
from flask import redirect, request, session, render_template

@app.route("/")
def index():
    sql = "SELECT * FROM players ORDER BY points DESC"
    result = db.session.execute(sql)
    players = result.fetchall()
    return render_template("index.html", players=players)
    
@app.route("/adminmenu")
def admin():
    if not session:
        return render_template ("login.html")
    elif session["user_id"] == 1:
        return render_template ("adminmenu.html")
    return render_template ("error.html", message="Käyttäjä ei ole admin-käyttäjä")

