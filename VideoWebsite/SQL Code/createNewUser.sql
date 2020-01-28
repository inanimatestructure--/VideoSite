DELIMITER //
DROP PROCEDURE IF EXISTS createNewUser //

CREATE PROCEDURE createNewUser(IN username varchar(50), IN handleName varchar(50))
BEGIN
  INSERT INTO users(userName, handle) VALUES (username, handleName);
END //
DELIMITER ;
