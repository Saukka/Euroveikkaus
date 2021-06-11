from app import app
from db import db
from flask import redirect, request, session, render_template

def newplayer(name):
    if not session["user_id"] == 1:
        return False
    try:
        sql = "INSERT INTO players (player, points) VALUES (:name, 0)"
        db.session.execute(sql, {"name":name})
        db.session.commit()
        return True
    except:
        return False
    
def setmatchguesses(player,guesses):
    if not session["user_id"] == 1:
        return False
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
        return True
    except:
        return False

def setgroupguess(player,group,guess):
    if not session["user_id"] == 1:
        return False
    else:
        m = guess.splitlines()
        i = 0
        while i < 4:
            string = m[i]
            teamstring = string.split("\t")
            team = teamstring[0]
            finish = int(string[-1])
            sql = "INSERT INTO groupguesses (player, group_id, team, finish) VALUES (:player,:group,:team,:finish)"
            db.session.execute(sql, {"player":player, "group":group, "team":team, "finish":finish})
            db.session.commit()
            i += 1
        return True
