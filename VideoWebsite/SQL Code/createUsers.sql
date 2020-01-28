DROP TABLE IF EXISTS users;
CREATE TABLE users (
 userId INT NOT NULL AUTO_INCREMENT,
 userName varchar(50) NOT NULL,
 handle varchar(50) unique NOT NULL,
 PRIMARY KEY (userId)
);
