DELIMITER //
DROP PROCEDURE IF EXISTS uploadAVideo //

CREATE PROCEDURE uploadAVideo(IN newNameOfFile varchar(250), IN uid INT)
BEGIN
    INSERT INTO videos(fileName, userId) VALUES (newNameOfFile, uid);
END //
DELIMITER ;
