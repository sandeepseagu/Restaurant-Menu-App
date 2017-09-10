-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP VIEW IF EXISTS standings;
DROP View IF EXISTS count;
DROP VIEW IF EXISTS wins;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS players;

create table players(
    id SERIAL primary key,
    name text
);

create table matches(
    id SERIAL primary key,
    player int REFERENCES players(id),
    opponent int REFERENCES players(id),
    result int
);

create view wins as
    select players.id, count(matches.player) as n from players left join (select * from matches where result>0) as matches
    on players.id=matches.player group by players.id;

create view count as
    select players.id, count(matches.player) as p players left join matches on players.id=matches.player group by
    players.id;

create view standings as
    select players.id,players.name,wins.n,count.p from players,wins,count where players.id=wins.id and
    players.id=count.id;

