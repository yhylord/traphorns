CREATE TABLE `links` ( `id` INTEGER PRIMARY KEY AUTOINCREMENT, `source` VARCHAR NOT NULL, `link` VARCHAR NOT NULL, `dead` BOOLEAN NOT NULL, `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP )