# Host: localhost  (Version: 5.7.26)
# Date: 2025-01-15 19:07:12
# Generator: MySQL-Front 5.3  (Build 4.234)

/*!40101 SET NAMES utf8 */;

#
# Structure for table "django_migrations"
#

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

#
# Data for table "django_migrations"
#

/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'role','0001_initial','2024-12-27 05:30:20.830446'),(2,'user','0001_initial','2024-12-27 05:30:20.853263'),(3,'food','0001_initial','2024-12-27 05:30:20.878355'),(4,'food','0002_alter_food_table','2024-12-27 05:30:20.886438'),(5,'order','0001_initial','2024-12-27 05:30:20.895446'),(6,'order','0002_alter_order_table','2024-12-27 05:30:20.899454'),(7,'role','0002_alter_role_table','2024-12-27 05:30:20.906447'),(8,'user','0002_alter_user_table','2024-12-27 05:30:20.910445');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;

#
# Structure for table "sys_food"
#

DROP TABLE IF EXISTS `sys_food`;
CREATE TABLE `sys_food` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  `foodname` varchar(50) NOT NULL,
  `foodicon` varchar(100) NOT NULL,
  `foodprocedure` longtext NOT NULL,
  `video` varchar(100) NOT NULL,
  `price` double NOT NULL,
  `remarks` longtext NOT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `food_food_user_id_fba7e822` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

#
# Data for table "sys_food"
#

/*!40000 ALTER TABLE `sys_food` DISABLE KEYS */;
INSERT INTO `sys_food` VALUES (1,'2025-01-07 03:39:30.702664','2025-01-07 03:39:30.702664',NULL,'鱼香肉丝','','<p>请输入做菜步骤</p>','',15,'备注',1);
/*!40000 ALTER TABLE `sys_food` ENABLE KEYS */;

#
# Structure for table "sys_order"
#

DROP TABLE IF EXISTS `sys_order`;
CREATE TABLE `sys_order` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  `user` varchar(50) NOT NULL,
  `food` varchar(50) NOT NULL,
  `num` int(11) NOT NULL,
  `remarks` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

#
# Data for table "sys_order"
#

/*!40000 ALTER TABLE `sys_order` DISABLE KEYS */;
INSERT INTO `sys_order` VALUES (1,'2025-01-15 10:23:27.607108','2025-01-15 10:23:27.607108',NULL,'admin','鱼香肉丝',1,'');
/*!40000 ALTER TABLE `sys_order` ENABLE KEYS */;

#
# Structure for table "sys_role"
#

DROP TABLE IF EXISTS `sys_role`;
CREATE TABLE `sys_role` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `level` int(11) NOT NULL,
  `remarks` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;

#
# Data for table "sys_role"
#

/*!40000 ALTER TABLE `sys_role` DISABLE KEYS */;
INSERT INTO `sys_role` VALUES (1,'2024-09-10 12:57:07.504000','2025-01-04 00:45:08.698509',NULL,'root',1,'aa'),(2,'2024-09-10 12:57:07.510000','2024-09-10 12:57:07.510000',NULL,'client',2,'ass');
/*!40000 ALTER TABLE `sys_role` ENABLE KEYS */;

#
# Structure for table "sys_user"
#

DROP TABLE IF EXISTS `sys_user`;
CREATE TABLE `sys_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(36) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `avatar` varchar(255) NOT NULL,
  `sex` varchar(20) NOT NULL,
  `email` varchar(20) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `remarks` longtext NOT NULL,
  `role_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_user_role_id_aee6bf52` (`role_id`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

#
# Data for table "sys_user"
#

/*!40000 ALTER TABLE `sys_user` DISABLE KEYS */;
INSERT INTO `sys_user` VALUES (1,'2024-09-10 12:57:07.507000','2024-09-10 12:57:07.507000',NULL,'admin','hJ58F_Qr96LW','18888888888','','男','1233@qq.com',1,'初始管理员',1),(2,'2024-09-10 12:57:07.512000','2024-09-10 12:57:07.512000',NULL,'dev','D19e534b_com','18888888887','','男','1232@qq.com',1,'运维管理员',1),(3,'2024-09-10 12:57:07.507000','2025-01-15 15:13:15.170000',NULL,'test','123456','18888888886','','男','1231@qq.com',1,'测试用户',2);
/*!40000 ALTER TABLE `sys_user` ENABLE KEYS */;
