from app import app
from db import db
from flask import redirect, request, session, render_template

def newplayer(name):
    if not session["user_id"] == 1:
        return False;
    try:
        sql = "INSERT INTO players (player, points) VALUES (:name, 0)"
        db.session.execute(sql, {"name":name})
        db.session.commit()
        return True;
    except:
        return False;
    
def setmatchguesses(player,guesses):
    if not session["user_id"] == 1:
        return False;
    try:
        m = guesses.splitlines()
        i = 0
        print(m)
        while i < 36:
            string = m[i]
            hgoals = int(string[0])
            agoals = int(string[2])
            winner = string[-1]
            match_id = i + 1
            sql = "INSERT INTO matchguesses (match_id, player, homegoals, awaygoals, winner) VALUES (:match_id,:player,:hgoals,:agoals,:winner)"
            db.session.execute(sql, {"match_id":match_id, "player":player, "hgoals":hgoals, "agoals":agoals, "winner":winner})
            db.session.commit()
            i += 1
        return True;
    except:
        return False;

def setgroupguess(player,group,guess):
    if not session["user_id"] == 1:
        return False;
    else:
        m = guess.splitlines()
        i = 0
        while i < 4:
            string = m[i]
            teamstring = string.split("\t")
            team = teamstring[0]
            finish = int(string[-1])
            sql = "INSERT INTO finishguesses (player, group_id, team, groupfinish) VALUES (:player,:group,:team,:finish)"
            db.session.execute(sql, {"player":player, "group":group, "team":team, "finish":finish})
            db.session.commit()
            i += 1
        return True;

def setfinish(player, finish, guess):
    if not session["user_id"] == 1:
        return False;
    
    m = guess.splitlines()
    i = 0
    while i < len(m):
        string = m[i]
        if len(string.strip()) == 0:
            break;
        sql = "UPDATE finishguesses SET finalfinish = :finish WHERE player = :player AND team = :string"
        db.session.execute(sql, {"finish":finish, "player":player, "string":string})
        db.session.commit()
        i += 1
    return True;

def settopplayers(player, scorer, assister):
    if not session["user_id"] == 1:
        return False;
    sql = "INSERT INTO topplayers (player, scorerguess, assisterguess) VALUES (:player,:scorer,:assister)"
    db.session.execute(sql, {"player":player, "scorer":scorer, "assister":assister})
    db.session.commit()
    return True;

def updatematchpoints(i):
        sql1 = "UPDATE matchguesses SET POINTS = 0 WHERE match_id=:i"
        db.session.execute(sql1, {"i":i})
        db.session.commit()
        sql = "SELECT id, homegoals, awaygoals, winner FROM matches WHERE id=:i"
        result = db.session.execute(sql, {"i":i})
        info = result.fetchall()
        if not info:
            return False;
        if info[0][1] == -1:
            return False;
        homegoals = info[0][1]
        awaygoals = info[0][2]
        winner = info[0][3]
        
        sql2 = "UPDATE matchguesses SET points = 1 WHERE match_id=:i AND (homegoals=:homegoals OR awaygoals=:awaygoals)"
        db.session.execute(sql2, {"i":i, "homegoals":homegoals, "awaygoals":awaygoals})
        db.session.commit()
        
        sql3 = "UPDATE matchguesses SET points = 3 WHERE match_id=:i AND winner=:winner"
        db.session.execute(sql3, {"i":i, "winner":winner})
        db.session.commit()
        
        sql4 = "UPDATE matchguesses SET points = 5 WHERE match_id=:i AND winner=:winner AND (homegoals=:homegoals OR awaygoals=:awaygoals)"
        db.session.execute(sql4, {"i":i, "winner":winner, "homegoals":homegoals, "awaygoals":awaygoals})
        db.session.commit()
        
        sql5 = "UPDATE matchguesses SET points = 9 WHERE match_id=:i AND winner=:winner AND homegoals=:homegoals AND awaygoals=:awaygoals"
        db.session.execute(sql5, {"i":i, "winner":winner, "homegoals":homegoals, "awaygoals":awaygoals})
        db.session.commit()
        
        sql6 = "UPDATE players p SET points = (SELECT SUM(points) FROM matchguesses m WHERE m.player = p.player);"
        db.session.execute(sql6)
        db.session.commit()
        return True;
