USE pyfungivisum;
DROP TABLE IF EXISTS `predictions`;
DROP TABLE IF EXISTS `users`;

CREATE TABLE `users`(
`id` int(11) NOT NULL AUTO_INCREMENT,
`username` varchar(50) NOT NULL,
`firstname` varchar(50) NOT NULL,
`lastname` varchar(50) NOT NULL,
`email` varchar(200) NOT NULL,
`hashedpassword` varchar(200) NOT NULL,
PRIMARY KEY (`id`)
)engine=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE `predictions`(
`id` int(11) NOT NULL AUTO_INCREMENT,
`imagename` varchar(50) NOT NULL,
`confidence` float NOT NULL,
`predictedspecy` varchar(50) NOT NULL,
`presumedspecy` varchar(50) DEFAULT NULL,
`userid` int(11) NOT NULL,
 PRIMARY KEY(`id`),
 FOREIGN KEY(`userid`) REFERENCES users(`id`)
)engine=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;





