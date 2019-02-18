DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_email VARCHAR(20),
    IN p_password VARCHAR(20),
    IN p_no VARCHAR(20)
)
BEGIN
    if ( select exists (select 1 from users where email = p_email) ) THEN
     
        select 'Username Exists !!';
     
    ELSE
     
        insert into users
        (
            email,
            password,
            phoneno
        )
        values
        (
            p_email,
            p_password,
            p_no
        );
     
    END IF;
END$$
DELIMITER ;