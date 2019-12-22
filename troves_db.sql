CREATE DATABASE  IF NOT EXISTS `troves_of_treasure` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `troves_of_treasure`;
-- MySQL dump 10.13  Distrib 8.0.17, for Win64 (x86_64)
--
-- Host: localhost    Database: troves_of_treasure
-- ------------------------------------------------------
-- Server version	8.0.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `date_price_info`
--

DROP TABLE IF EXISTS `date_price_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `date_price_info` (
  `date_of_price` date NOT NULL,
  `price` int(11) DEFAULT NULL,
  `portfolio_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`date_of_price`),
  KEY `portfolio_id` (`portfolio_id`),
  CONSTRAINT `date_price_info_ibfk_1` FOREIGN KEY (`portfolio_id`) REFERENCES `portfolio` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `date_price_info`
--

LOCK TABLES `date_price_info` WRITE;
/*!40000 ALTER TABLE `date_price_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `date_price_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `portfolio`
--

DROP TABLE IF EXISTS `portfolio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `portfolio` (
  `name` varchar(30) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_name` (`user_name`),
  CONSTRAINT `portfolio_ibfk_1` FOREIGN KEY (`user_name`) REFERENCES `user_info` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `portfolio`
--

LOCK TABLES `portfolio` WRITE;
/*!40000 ALTER TABLE `portfolio` DISABLE KEYS */;
INSERT INTO `portfolio` VALUES ('infect',1,'jreiss1923'),('infect',2,'jreiss1923'),('my cards',5,'jreiss1923'),('mycards',6,'jreiss1923'),('mycards',7,'jreiss1923'),('mycards',8,'jreiss1923'),('mycards',9,'jreiss1923'),('mycards',10,'jreiss1923'),('mycards',11,'jreiss1923'),('mycards',12,'jreiss1923'),('mycards',13,'jreiss1923'),('mycards',14,'jreiss1923'),('mycards',15,'jreiss1923'),('mycards',16,'jreiss1923'),('mycards',17,'jreiss1923'),('mycards',18,'jreiss1923'),('mycards',19,'jreiss1923'),('mycards',20,'jreiss1923'),('mycards',21,'jreiss1923'),('mycards',22,'jreiss1923'),('mycards',23,'jreiss1923'),('mycards',24,'jreiss1923'),('mycards',25,'jreiss1923'),('mycards',26,'jreiss1923'),('mycards',27,'jreiss1923'),('mycards',28,'jreiss1923'),('mycards',29,'jreiss1923'),('mycards',30,'jreiss1923');
/*!40000 ALTER TABLE `portfolio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `portfolio_card_assc`
--

DROP TABLE IF EXISTS `portfolio_card_assc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `portfolio_card_assc` (
  `portfolio_id` int(11) NOT NULL,
  `card_id` int(11) NOT NULL,
  `card_count` int(11) DEFAULT NULL,
  `foiled` tinyint(1) DEFAULT NULL,
  KEY `portfolio_id` (`portfolio_id`),
  KEY `card_id` (`card_id`),
  CONSTRAINT `portfolio_card_assc_ibfk_1` FOREIGN KEY (`portfolio_id`) REFERENCES `portfolio` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `portfolio_card_assc`
--

LOCK TABLES `portfolio_card_assc` WRITE;
/*!40000 ALTER TABLE `portfolio_card_assc` DISABLE KEYS */;
INSERT INTO `portfolio_card_assc` VALUES (17,28579,4,0),(13,28579,4,1);
/*!40000 ALTER TABLE `portfolio_card_assc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_info`
--

DROP TABLE IF EXISTS `user_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_info` (
  `username` varchar(25) NOT NULL,
  `password` varchar(200) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_info`
--

LOCK TABLES `user_info` WRITE;
/*!40000 ALTER TABLE `user_info` DISABLE KEYS */;
INSERT INTO `user_info` VALUES ('jreiss1923','188239ced50cf7e51c6397aa425c76e5','joshua.reiss2@gmail.com');
/*!40000 ALTER TABLE `user_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-12-21 20:28:11
