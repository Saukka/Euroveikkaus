CREATE TABLE userseuro (
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
    awaygoals INTEGER,
    winner TEXT,
    date TEXT
);

CREATE TABLE TEAMS (
    id SERIAL PRIMARY KEY,
    team TEXT,
    Group_id TEXT,
    groupresult INTEGER,
    finalresult INTEGER
);

CREATE TABLE matchguesses (
    id SERIAL PRIMARY KEY,
    match_id INTEGER,
    player TEXT,
    homegoals INTEGER,
    awaygoals INTEGER,
    winner TEXT
); 
CREATE TABLE finishguesses (
    id SERIAL PRIMARY KEY,
    player TEXT,
    group_id TEXT,
    team TEXT,
    groupfinish INTEGER,
    finalfinish INTEGER
);
