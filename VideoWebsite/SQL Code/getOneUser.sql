DELIMITER //
DROP PROCEDURE IF EXISTS getOneUser //

CREATE PROCEDURE getOneUser(IN name VARCHAR(50))
BEGIN
  SELECT *
    FROM users WHERE handle = name OR userName = name;
END //
DELIMITER ;
