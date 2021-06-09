from app import app
from db import db
from flask import redirect, request, session, render_template, make_response

@app.route("/)
def index():
    sql = SELECT * FROM players ORDER BY points DESC"
    result = db.session.execute(sql)
    players = result.fetchall()
    return render_template("index.html", players=players)

