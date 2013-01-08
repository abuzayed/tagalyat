
delimiter $$

CREATE DATABASE `fin` /*!40100 DEFAULT CHARACTER SET utf8 */$$

delimiter $$

CREATE TABLE `security` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `SYMBOL` varchar(16) NOT NULL,
  `DESCRIPTION` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `id_UNIQUE` (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8$$


CREATE TABLE `history_daily` (
  `SEC_ID` int(10) unsigned NOT NULL,
  `DATE` date NOT NULL,
  `OPEN` decimal(16,8) DEFAULT NULL,
  `HIGH` decimal(16,8) DEFAULT NULL,
  `LOW` decimal(16,8) DEFAULT NULL,
  `CLOSE` decimal(16,8) DEFAULT NULL,
  `ADJ_CLOSE` decimal(16,8) DEFAULT NULL,
  `VOLUME` decimal(24,8) DEFAULT NULL,
  KEY `SEC_DATE` (`SEC_ID`,`DATE`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8$$

