DELIMITER //
DROP PROCEDURE IF EXISTS updateVideo //

CREATE PROCEDURE updateVideo(IN vidId INT,IN videoTitle varchar(250))
BEGIN
  UPDATE videos
  SET title = videoTitle
  WHERE videoId = vidId;
END //
DELIMITER ;
