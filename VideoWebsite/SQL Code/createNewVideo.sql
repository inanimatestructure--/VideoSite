DELIMITER //
DROP PROCEDURE IF EXISTS createNewVideo //

CREATE PROCEDURE createNewVideo(IN videoTitle varchar(250), IN nameOfFile varchar(250), IN uID INT)
BEGIN
  INSERT INTO videos(title, fileName, userId) VALUES (videoTitle, nameOfFile, uID);
END //
DELIMITER ;
