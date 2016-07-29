DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id serial PRIMARY KEY,
  name varchar,
  email varchar,
  password varchar,
  username varchar
  #add follower property later
);


--Users Regan and Dave
insert into users values(default, 'Regan Co', 'regan@gmail.com', 'rpassword', 'rusername');
insert into users values(default, 'David Pham', 'dpham@gmail.com', 'dpassword', 'dusername');
insert into users values(default, 'Tony Stark', 'tstark@gmail.com', 'password', 'ironman');

insert into users values(default, 'Diana Prince', 'diane@gmail.com', '123', 'wonder');
insert into users values(default, 'Clark Kent', 'clark@gmail.com', '123', 'superman');
insert into users values(default, 'Bruce Wayne', 'batman@gmail.com', '123', 'batman');



DROP TABLE IF EXISTS tweet_table;
CREATE TABLE tweet_table (
  id serial PRIMARY KEY,
  user_id integer REFERENCES users (id),
  tweet_content varchar(141),
  timecreated timestamp,
  hearts boolean,
  hearts_amount integer

);
--Tweets
insert into tweet_table values(default, 1, 'I no use twitter', '2016-09-28 01:00:00', FALSE,  0);
insert into tweet_table values(default, 2, 'Getting a programming job', '2016-09-28 01:00:00', TRUE, 10);
insert into tweet_table values(default, 3, 'Gonna see Star Trek Beyond', '2005-09-28 01:00:00', TRUE, 5);
insert into tweet_table values(default, 1, 'I love sandwiches', '2016-09-28 01:00:00', FALSE,  0);
insert into tweet_table values(default, 1, 'I want to graduate', '2016-09-28 01:00:00', FALSE,  0);
insert into tweet_table values(default, 4, 'I love rock and roll musics', '2016-09-28 01:00:00', FALSE,  0);
insert into tweet_table values(default, 5, 'I want to go to Japan on vacation', '2016-09-28 01:00:00', FALSE,  0);
insert into tweet_table values(default, 5, 'I love cartoons', '2016-09-28 01:00:00', FALSE,  0);
insert into tweet_table values(default, 3, 'I want to build a robot', '2016-09-28 01:00:00', TRUE,  0);



DROP TABLE IF EXISTS followz;
CREATE TABLE followz (
person_following integer REFERENCES users (id),
is_following_id integer REFERENCES users (id)
);

--Follow inserts
insert into followz values(1, 2);
insert into followz values(2, 3);
insert into followz values(3, 2);
insert into followz values(4, 2);
insert into followz values(5, 2);
insert into followz values(6, 3);
insert into followz values(1, 4);
insert into followz values(2, 4);
insert into followz values(2, 5);
