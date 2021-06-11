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
    
@app.route("/<string:player>")
def show(player):
    sql = "SELECT * FROM matches"
    result = db.session.execute(sql)
    matches = result.fetchall()
    sql2 = "SELECT * FROM matchguesses WHERE player =:player"
    result2 = db.session.execute(sql2, {"player":player})
    matchguesses = result2.fetchall()
    
    sql3 = "SELECT * FROM finishguesses WHERE player = :player ORDER BY group_id, groupfinish"
    result3 = db.session.execute(sql3, {"player":player})
    groupguesses = result3.fetchall()
    
    sql4 = "SELECT * FROM finishguesses WHERE player = :player AND finalfinish IS NOT NULL ORDER BY finalfinish"
    result4 = db.session.execute(sql4, {"player":player})
    finishguesses = result4.fetchall()
    
    sql5 = "SELECT * FROM topplayers WHERE player = :player"
    result5 = db.session.execute(sql5, {"player":player})
    topplayers = result5.fetchall()
    
    return ("player.html", matches=matches, matchguesses=matchguesses, groupguesses = groupguesses, finishguesses = finishguesses, topplayers = topplayers)
    
    
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
    
    first = request.form["1"]
    second = request.form["2"]
    third = request.form["3to4"]
    fifth = request.form["5to8"]
    ninth = request.form["9to16"]
    
    actions.setfinish(player,1,first)
    actions.setfinish(player,2,second)
    actions.setfinish(player,3,third)
    actions.setfinish(player,5,fifth)
    actions.setfinish(player,9,ninth)
    
    scorer = request.form["topscorer"]
    assister = request.form["topassister"]
    actions.settopplayers(player, scorer, assister)
    return redirect("/")
