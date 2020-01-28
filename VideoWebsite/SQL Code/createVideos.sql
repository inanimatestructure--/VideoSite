DROP TABLE IF EXISTS videos;
CREATE TABLE videos (
 videoId INT NOT NULL AUTO_INCREMENT,
 title varchar(250) DEFAULT 'Sandnes',
 fileName varchar(250) not null,
 userId INT,
 PRIMARY KEY (videoId),
 FOREIGN KEY (userId) REFERENCES users(userId)
  ON DELETE CASCADE
  ON UPDATE CASCADE
);
