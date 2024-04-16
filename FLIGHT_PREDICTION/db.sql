/*
SQLyog Community Edition- MySQL GUI v7.01 
MySQL - 5.0.27-community-nt : Database - androiddb
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`androiddb` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `androiddb`;

/*Table structure for table `userdetails` */

DROP TABLE IF EXISTS `userdetails`;

CREATE TABLE `userdetails` (
  `id` int(255) NOT NULL auto_increment,
  `username` varchar(255) default NULL,
  `email` varchar(255) default NULL,
  `mobile` varchar(255) default NULL,
  `password` varchar(255) default NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `userdetails` */

insert  into `userdetails`(`id`,`username`,`email`,`mobile`,`password`) values (1,'a','rmundekar2000@gmail.com','1236547898','d'),(2,'yask','rmundekar200@gmail.com','9561161391','b'),(3,'kj','rmun2000@gmail.com','2356898956','a'),(4,'015-Roshan Mundekar','f@gmail.com','1956116139','g'),(5,'Roshan ','rm@gmail.com','4567890987','g'),(6,'yash','sujay@gmail.com','8768658678','y'),(7,'admin','sujay@gmail.com','35456768899','e');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
