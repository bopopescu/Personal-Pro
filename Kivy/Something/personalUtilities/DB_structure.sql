-- MySQL Version

USE be6v5hba1kumyfvusyeb;

CREATE TABLE IF NOT EXISTS `users` (
  `id_user` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `username` varchar(30) UNIQUE NOT NULL COMMENT 'cant be changed',
  `password` varchar(20) NOT NULL COMMENT 'it can be changed',
  `times` int NOT NULL
);

CREATE TABLE IF NOT EXISTS `tasks` (
  `id_task` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `task` varchar(18) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS `users_tasks` (
  `id_user` int NOT NULL,
  `id_task` int NOT NULL
);

ALTER TABLE `users_tasks` ADD FOREIGN KEY (`id_task`) REFERENCES `tasks` (`id_task`);

ALTER TABLE `users_tasks` ADD FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`);

INSERT INTO users VALUES (NULL, 'admin','admin', 0);


-- SQLITE Version

CREATE TABLE IF NOT EXISTS users(
  `id_user` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  `username` TEXT UNIQUE NOT NULL --COMMENT 'cant be changed',
  `password` TEXT NOT NULL --COMMENT 'it can be changed',
  `times` INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks(
  `id_task` INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `task` TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS users_tasks(
  `id_user` INTEGER NOT NULL,
  `id_task` INTEGER NOT NULL,
  FOREIGN KEY (id_task) REFERENCES tasks(id_task),
  FOREIGN KEY (id_user) REFERENCES users(id_user),
);