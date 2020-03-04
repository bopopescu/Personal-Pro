USE be6v5hba1kumyfvusyeb;

CREATE TABLE IF NOT EXISTS  usuarios(
	`user_id` INTEGER UNSIGNED PRIMARY KEY AUTO_INCREMENT,
	`ip` VARCHAR(255) NOT NULL,
	`port` VARCHAR(255) NOT NULL,
    `username` VARCHAR(255) NOT NULL,
    `password` VARCHAR(255) NOT NULL
);


INSERT INTO usuarios(`ip`, `port`,`username`, `password`) VALUES ('127.0.0.1','3600','drarn','1234');