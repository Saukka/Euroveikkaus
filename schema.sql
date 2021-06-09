CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    player TEXT UNIQUE,
    points INTEGER
);

CREATE TABLE MATCHES (
    id SERIAL PRIMARY KEY,
    home TEXT,
    AWAY TEXT,
    homegoals INTEGER,
    awaygoals INTEGER
);

CREATE TABLE TEAMS (
    id SERIAL PRIMARY KEY,
    team TEXT,
    Group_id TEXT
    groupresult INTEGER
);

CREATE TABLE matchguesses (
    id SERIAL PRIMARY KEY,
    match_id SERIAL PRIMARY KEY,
    player TEXT,
    homegoals INTEGER,
    awaygoals INTEGER
    winner TEXT,
); 
CREATE TABLE matchresults (
    id SERIAL PRIMARY KEY,
    match_id INTEGER,
    homegoals INTEGER,
    awaygoals INTEGER,
    winner INTEGER
);
CREATE TABLE groupguesses (
    id SERIAL PRIMARY KEY,
    player TEXT,
    group_id
    team
    finish
);
