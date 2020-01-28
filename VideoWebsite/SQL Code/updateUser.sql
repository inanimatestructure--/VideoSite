DELIMITER //
DROP PROCEDURE IF EXISTS updateUser //

CREATE PROCEDURE updateUser(IN uID INT,IN name varchar(50))
BEGIN
  UPDATE users
  SET handle = name
  WHERE userId= uID;
END //
DELIMITER ;
