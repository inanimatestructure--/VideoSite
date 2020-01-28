DELIMITER //
DROP PROCEDURE IF EXISTS deleteVideo //

CREATE PROCEDURE deleteVideo(IN id INT, IN vidId INT)
BEGIN
  DELETE
    FROM videos WHERE userId = id AND videoId = vidId;
END //
DELIMITER ;
