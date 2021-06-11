from app import app
from db import db
from flask import redirect, request, session, render_template
import users
import actions

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
        sql = "SELECT * FROM players"
        result = db.session.execute(sql)
        players = result.fetchall()
        return render_template ("adminmenu.html", players=players)
    return render_template ("error.html", message="Käyttäjä ei ole admin-käyttäjä")
    
@app.route("/adminmenu/<string:player>")
def set(player):
    return render_template("setplayer.html", player=player)

@app.route("/register324")
def register():
    return render_template("register.html")

@app.route("/commitregister", methods=["POST"])
def commitreg():
    username = request.form["username"]
    password = request.form["password"]
    users.register(username,password)
    return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username,password):
            return redirect("/adminmenu")
        else:
            return render_template("error.html",message="Väärä tunnus tai salasana")

@app.route("/newplayer", methods=["POST"])
def newplayer():
    name = request.form["name"]
    if (len(name)) < 2:
        return render_template("error.html",message="Nimen pitää sisältää vähintään kaksi merkkiä")
    actions.newplayer(name)
    return redirect(request.referrer)

@app.route("/commitguesses", methods=["POST"])
def commitguesses():
    player = request.form["pelaaja"]
    matchguesses = request.form["matches"]
    actions.setmatchguesses(player,matchguesses)
    
    agroup = request.form["A"]
    
    actions.setgroupguess(player,"A",agroup)
    bgroup = request.form["B"]
    actions.setgroupguess(player,"B",bgroup)
    cgroup = request.form["C"]
    actions.setgroupguess(player,"C",cgroup)
    dgroup = request.form["D"]
    actions.setgroupguess(player,"D",dgroup)
    egroup = request.form["E"]
    actions.setgroupguess(player,"E",egroup)
    fgroup = request.form["F"]
    actions.setgroupguess(player,"F",fgroup)
    
    return redirect("/")
