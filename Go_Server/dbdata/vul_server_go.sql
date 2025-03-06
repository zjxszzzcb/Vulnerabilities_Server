# Host: localhost  (Version: 5.7.26)
# Date: 2025-01-15 15:15:22
# Generator: MySQL-Front 5.3  (Build 4.234)

/*!40101 SET NAMES utf8 */;

#
# Structure for table "sys_food"
#

DROP TABLE IF EXISTS `sys_food`;
CREATE TABLE `sys_food` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `created_at` datetime(3) DEFAULT NULL,
  `updated_at` datetime(3) DEFAULT NULL,
  `deleted_at` datetime(3) DEFAULT NULL,
  `foodname` varchar(50) DEFAULT NULL,
  `user_id` bigint(20) unsigned NOT NULL,
  `foodicon` varchar(100) DEFAULT NULL,
  `foodprocedure` longtext,
  `video` varchar(100) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `remarks` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_sys_food_deleted_at` (`deleted_at`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

#
# Data for table "sys_food"
#

/*!40000 ALTER TABLE `sys_food` DISABLE KEYS */;
INSERT INTO `sys_food` VALUES (1,'2024-09-10 13:04:53.502','2025-01-15 15:11:29.490',NULL,'鱼香肉丝',1,'','<p>请输入做菜步骤</p>','',15,''),(2,'2024-09-10 13:05:53.502','2025-01-15 15:11:39.490',NULL,'小炒肉',1,'','<p>请输入做菜步骤</p>','',15,''),(3,'2024-09-10 13:04:53.502','2025-01-15 15:11:33.490',NULL,'番茄炒蛋',1,'','<p>请输入做菜步骤</p>','',15,''),(4,'2024-09-10 14:05:53.502','2025-01-15 15:11:39.490',NULL,'红烧肉',1,'','<p>请输入做菜步骤</p>','',15,'');
/*!40000 ALTER TABLE `sys_food` ENABLE KEYS */;

#
# Structure for table "sys_order"
#

DROP TABLE IF EXISTS `sys_order`;
CREATE TABLE `sys_order` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `created_at` datetime(3) DEFAULT NULL,
  `updated_at` datetime(3) DEFAULT NULL,
  `deleted_at` datetime(3) DEFAULT NULL,
  `user` varchar(50) DEFAULT NULL,
  `food` varchar(50) DEFAULT NULL,
  `num` int(11) DEFAULT NULL,
  `remarks` longtext,
  PRIMARY KEY (`id`),
  KEY `idx_sys_order_deleted_at` (`deleted_at`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

#
# Data for table "sys_order"
#

/*!40000 ALTER TABLE `sys_order` DISABLE KEYS */;
INSERT INTO `sys_order` VALUES (1,'2025-01-15 15:11:38.909','2025-01-15 15:11:38.909',NULL,'admin','鱼香肉丝',1,'');
/*!40000 ALTER TABLE `sys_order` ENABLE KEYS */;

#
# Structure for table "sys_role"
#

DROP TABLE IF EXISTS `sys_role`;
CREATE TABLE `sys_role` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `created_at` datetime(3) DEFAULT NULL,
  `updated_at` datetime(3) DEFAULT NULL,
  `deleted_at` datetime(3) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `level` int(11) DEFAULT '0',
  `remarks` longtext,
  PRIMARY KEY (`id`),
  KEY `idx_sys_role_deleted_at` (`deleted_at`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

#
# Data for table "sys_role"
#

/*!40000 ALTER TABLE `sys_role` DISABLE KEYS */;
INSERT INTO `sys_role` VALUES (1,'2024-09-10 12:57:07.504','2024-09-10 12:57:07.504',NULL,'root',1,'最高管理员权限'),(2,'2024-09-10 12:57:07.510','2025-01-15 15:13:05.953',NULL,'client',2,'客户权限');
/*!40000 ALTER TABLE `sys_role` ENABLE KEYS */;

#
# Structure for table "sys_user"
#

DROP TABLE IF EXISTS `sys_user`;
CREATE TABLE `sys_user` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `created_at` datetime(3) DEFAULT NULL,
  `updated_at` datetime(3) DEFAULT NULL,
  `deleted_at` datetime(3) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(36) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `sex` varchar(20) DEFAULT NULL,
  `email` varchar(20) DEFAULT NULL,
  `status` tinyint(1) DEFAULT '0',
  `role_id` bigint(20) unsigned NOT NULL,
  `remarks` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_sys_user_deleted_at` (`deleted_at`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

#
# Data for table "sys_user"
#

/*!40000 ALTER TABLE `sys_user` DISABLE KEYS */;
INSERT INTO `sys_user` VALUES (1,'2024-09-10 12:57:07.507','2024-09-10 12:57:07.507',NULL,'admin','hJ58F_Qr96LW','18888888888','','男','1233@qq.com',1,1,'初始管理员'),(2,'2024-09-10 12:57:07.512','2024-09-10 12:57:07.512',NULL,'dev','D19e534b_com','18888888887','','男','1232@qq.com',1,1,'运维管理员'),(3,'2024-09-10 12:57:07.507','2025-01-15 15:13:15.170',NULL,'test','123456','18888888886','','男','1231@qq.com',1,2,'测试用户');
/*!40000 ALTER TABLE `sys_user` ENABLE KEYS */;
