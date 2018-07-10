CREATE TABLE IF NOT EXISTS `article`(
	`post_title` VARCHAR(100) NOT NULL,
	`create_time` DATETIME,
	`fav_nums` INT,
	`comment_nums` INT,
	`post_tag` VARCHAR(100),
	`post_content` LONGTEXT,
	`post_image` VARCHAR(100),
	`post_image_store_path` VARCHAR(100),
	`url_object_id` VARCHAR(100) NOT NULL,
	`post_url` VARCHAR(100) NOT NULL,
	PRIMARY KEY ( `url_object_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
