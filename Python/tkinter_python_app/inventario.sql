USE be6v5hba1kumyfvusyeb;

CREATE TABLE IF NOT EXISTS  inventario(
	`item_id` INTEGER UNSIGNED PRIMARY KEY AUTO_INCREMENT,
	`item` VARCHAR(255) NOT NULL,
	`precio` VARCHAR(255) NOT NULL
);

INSERT INTO inventario(`item`, `precio`) VALUES ('Audifonos','3000');
INSERT INTO inventario(`item`, `precio`) VALUES ('Mouse','4500');
INSERT INTO inventario(`item`, `precio`) VALUES ('Monitor','8850');