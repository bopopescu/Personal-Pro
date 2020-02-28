DROP DATABASE IF EXISTS flaskcontact;
CREATE DATABASE flaskcontact;
USE flaskcontact;

CREATE TABLE IF NOT EXISTS  contacts(
	`contact_id` INTEGER UNSIGNED PRIMARY KEY AUTO_INCREMENT,
	`fullname` VARCHAR(255),
	`phone` VARCHAR(255),
	`email` VARCHAR(255)
);