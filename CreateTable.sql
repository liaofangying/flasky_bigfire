user flaskdata;

/*!40101 SET NAMES utf8 */;

CREATE TABLE `comments` (
  `commentId` int(11) NOT NULL AUTO_INCREMENT,
  `commentContent` varchar(500) NOT NULL,
  `userId` int(11) NOT NULL,
  `postId` int(11) NOT NULL,
  `inDate` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `lastEditDate` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (`commentId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `posts` (
  `postId` int(11) NOT NULL AUTO_INCREMENT,
  `postContent` varchar(500) NOT NULL,
  `inDate` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `userId` int(11) NOT NULL,
  PRIMARY KEY (`postId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `relations` (
  `relationId` int(10) NOT NULL AUTO_INCREMENT,
  `bloggerId` int(10) NOT NULL,
  `fansId` int(10) NOT NULL,
  PRIMARY KEY (`relationId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `roles` (
  `roleId` int(11) NOT NULL AUTO_INCREMENT,
  `roleName` varchar(100) NOT NULL,
  `defaultType` tinyint(1) NOT NULL DEFAULT '0',
  `permissions` varchar(10) NOT NULL,
  PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `users` (
  `userId` int(11) NOT NULL AUTO_INCREMENT,
  `userName` varchar(64) NOT NULL,
  `passWord` varchar(128) NOT NULL,
  `roleId` int(11) NOT NULL,
  `inDate` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `location` varchar(64) DEFAULT NULL,
  `aboutMe` varchar(225) DEFAULT NULL,
  `lastSeen` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `avatar` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
