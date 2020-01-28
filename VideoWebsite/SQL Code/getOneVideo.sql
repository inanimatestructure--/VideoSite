DELIMITER //
DROP PROCEDURE IF EXISTS getOneVideo //

CREATE PROCEDURE getOneVideo(IN search VARCHAR(250), IN uid INT)
BEGIN
  SELECT *
    FROM videos WHERE title = search AND userId = uid;
END //
DELIMITER ;
