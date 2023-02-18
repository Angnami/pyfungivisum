USE pyfungivisum;
DROP TABLE IF EXISTS `predictions`;
DROP TABLE IF EXISTS `users`;

CREATE TABLE `users`(
`id` varchar(100) NOT NULL,
`username` varchar(50) NOT NULL,
`firstname` varchar(50) NOT NULL,
`lastname` varchar(50) NOT NULL,
`email` varchar(200) NOT NULL,
`is_admin` varchar(5) DEFAULT 'false',
`hashedpassword` varchar(200) NOT NULL,
PRIMARY KEY (`id`)
)engine=InnoDB  DEFAULT CHARSET=latin1;

CREATE TABLE `predictions`(
`id` varchar(100) NOT NULL,
`imagename` varchar(50) NOT NULL,
`confidence` float NOT NULL,
`predictedspecy` varchar(50) NOT NULL,
`presumedspecy` varchar(50) DEFAULT NULL,
`userid` varchar(100) NOT NULL,
 PRIMARY KEY(`id`),
 FOREIGN KEY(`userid`) REFERENCES users(`id`)
 ON DELETE CASCADE ON UPDATE CASCADE
)engine=InnoDB  DEFAULT CHARSET=latin1;





