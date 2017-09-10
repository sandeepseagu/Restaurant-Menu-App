SYNOPSIS

Tournament Database project is used to pair the players according to the rules of swiss- System(i.e pairing players who has same no of wins or close possible)


we use three files:
tournament.sql: The Database schema is created in it. Creation of players,matches table & wins,count,standings views

tournament.py:This file has which connects to the database and uses the database schema for pairing the players,reporting the match results and updating the database schema tables and views

tournament_test.py:Test Cases for tournament.py


tournament.sql:

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



Installation:
- You need to download fullstack-nanodegree-vm repositry
- Install virtual box and vagrant

- You have download Git Bash and log into repository files



creating the database:
Vagrant@vagrant:~ psql
vagrant=> CREATE DATABASE tournament;



Running Test
vagrant@vagrant:/vagrant/tournament$ python tournament$ python tournament_test.py
1.countPlayers() returns 0 after intial deletePlayers() execution
2.countPlayers() returns 1 after one player is registered.
3.countPlayers() returns 2 after two players are registered.
4.countPlayers() returns zero after registered players are deleted.
5.player records sucessfully deleted.
6.newly registered players appear in the standings with no matches.
7.After a match, players have updated standings
8 After a match deletion, player standings are properly reset
9 matches are properly deleted.
10 After one match, Players with one win are properly paired.
Success! All tests pass!

























