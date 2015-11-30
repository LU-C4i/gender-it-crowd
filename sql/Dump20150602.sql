CREATE DATABASE  IF NOT EXISTS `skills_match_db` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `skills_match_db`;
-- MySQL dump 10.13  Distrib 5.5.43, for debian-linux-gnu (x86_64)
--
-- Host: 127.0.0.1    Database: skills_match_db
-- ------------------------------------------------------
-- Server version	5.5.43-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `t_prs_person`
--

DROP TABLE IF EXISTS `t_prs_person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_prs_person` (
  `prs_id` int(11) NOT NULL AUTO_INCREMENT,
  `prs_name` varchar(45) NOT NULL,
  `prs_email` varchar(45) NOT NULL,
  PRIMARY KEY (`prs_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_skl_skills`
--

DROP TABLE IF EXISTS `t_skl_skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_skl_skills` (
  `skl_id` int(11) NOT NULL AUTO_INCREMENT,
  `skl_name` varchar(45) NOT NULL,
  PRIMARY KEY (`skl_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_skp_skillsPerson`
--

DROP TABLE IF EXISTS `t_skp_skillsPerson`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_skp_skillsPerson` (
  `skp_id` int(11) NOT NULL AUTO_INCREMENT,
  `prs_id` int(11) NOT NULL,
  `skl_id` int(11) NOT NULL,
  `skp_rating` tinyint(4) NOT NULL DEFAULT '50',
  PRIMARY KEY (`skp_id`),
  KEY `fk_t_skp_skillsPerson_1_idx` (`prs_id`),
  KEY `fk_t_skp_skillsPerson_2_idx` (`skl_id`),
  CONSTRAINT `fk_t_skp_skillsPerson_1` FOREIGN KEY (`prs_id`) REFERENCES `t_prs_person` (`prs_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_t_skp_skillsPerson_2` FOREIGN KEY (`skl_id`) REFERENCES `t_skl_skills` (`skl_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_tgp_tagPerson`
--

DROP TABLE IF EXISTS `t_tgp_tagPerson`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_tgp_tagPerson` (
  `tgp_id` int(11) NOT NULL AUTO_INCREMENT,
  `tgp_prs_id` int(11) NOT NULL,
  `tgp_name` varchar(45) NOT NULL,
  PRIMARY KEY (`tgp_id`),
  KEY `fk_t_tgp_tagPerson_1_idx` (`tgp_prs_id`),
  KEY `idx_t_tgp_tagPerson_tgp_name` (`tgp_name`),
  CONSTRAINT `fk_t_tgp_tagPerson_1` FOREIGN KEY (`tgp_prs_id`) REFERENCES `t_prs_person` (`prs_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-06-02 11:44:19
