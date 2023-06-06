-- MySQL dump 10.13  Distrib 8.0.33, for macos13 (arm64)
--
-- Host: localhost    Database: baza
-- ------------------------------------------------------
-- Server version	8.0.33

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'Admini'),(4,'Autori'),(3,'Korisnici'),(2,'Kuce');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add uloga',6,'add_uloga'),(22,'Can change uloga',6,'change_uloga'),(23,'Can delete uloga',6,'delete_uloga'),(24,'Can view uloga',6,'view_uloga'),(25,'Can add knjiga',7,'add_knjiga'),(26,'Can change knjiga',7,'change_knjiga'),(27,'Can delete knjiga',7,'delete_knjiga'),(28,'Can view knjiga',7,'view_knjiga'),(29,'Can add licitacija',8,'add_licitacija'),(30,'Can change licitacija',8,'change_licitacija'),(31,'Can delete licitacija',8,'delete_licitacija'),(32,'Can view licitacija',8,'view_licitacija'),(33,'Can add najpopularniji mesec',9,'add_najpopularnijimesec'),(34,'Can change najpopularniji mesec',9,'change_najpopularnijimesec'),(35,'Can delete najpopularniji mesec',9,'delete_najpopularnijimesec'),(36,'Can view najpopularniji mesec',9,'view_najpopularnijimesec'),(37,'Can add autor',10,'add_autor'),(38,'Can change autor',10,'change_autor'),(39,'Can delete autor',10,'delete_autor'),(40,'Can view autor',10,'view_autor'),(41,'Can add izdavacka kuca',11,'add_izdavackakuca'),(42,'Can change izdavacka kuca',11,'change_izdavackakuca'),(43,'Can delete izdavacka kuca',11,'delete_izdavackakuca'),(44,'Can view izdavacka kuca',11,'view_izdavackakuca'),(45,'Can add korisnik',12,'add_korisnik'),(46,'Can change korisnik',12,'change_korisnik'),(47,'Can delete korisnik',12,'delete_korisnik'),(48,'Can view korisnik',12,'view_korisnik'),(49,'Can add recenzija',13,'add_recenzija'),(50,'Can change recenzija',13,'change_recenzija'),(51,'Can delete recenzija',13,'delete_recenzija'),(52,'Can view recenzija',13,'view_recenzija'),(53,'Can add objava',14,'add_objava'),(54,'Can change objava',14,'change_objava'),(55,'Can delete objava',14,'delete_objava'),(56,'Can view objava',14,'view_objava'),(57,'Can add prati',15,'add_prati'),(58,'Can change prati',15,'change_prati'),(59,'Can delete prati',15,'delete_prati'),(60,'Can view prati',15,'view_prati'),(61,'Can add ponuda',16,'add_ponuda'),(62,'Can change ponuda',16,'change_ponuda'),(63,'Can delete ponuda',16,'delete_ponuda'),(64,'Can view ponuda',16,'view_ponuda'),(65,'Can add kolekcija',17,'add_kolekcija'),(66,'Can change kolekcija',17,'change_kolekcija'),(67,'Can delete kolekcija',17,'delete_kolekcija'),(68,'Can view kolekcija',17,'view_kolekcija'),(69,'Can add prodajna mesta',18,'add_prodajnamesta'),(70,'Can change prodajna mesta',18,'change_prodajnamesta'),(71,'Can delete prodajna mesta',18,'delete_prodajnamesta'),(72,'Can view prodajna mesta',18,'view_prodajnamesta'),(73,'Can add povezani',19,'add_povezani'),(74,'Can change povezani',19,'change_povezani'),(75,'Can delete povezani',19,'delete_povezani'),(76,'Can view povezani',19,'view_povezani'),(77,'Can add napisao',20,'add_napisao'),(78,'Can change napisao',20,'change_napisao'),(79,'Can delete napisao',20,'delete_napisao'),(80,'Can view napisao',20,'view_napisao');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `autor`
--

DROP TABLE IF EXISTS `autor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `autor` (
  `uloga_ptr_id` varchar(20) NOT NULL,
  `ImePrezime` varchar(40) NOT NULL,
  `DatumRodjenja` date NOT NULL,
  `Biografija` varchar(1000) NOT NULL,
  PRIMARY KEY (`uloga_ptr_id`),
  CONSTRAINT `autor_uloga_ptr_id_68647b9c_fk_uloga_KorIme` FOREIGN KEY (`uloga_ptr_id`) REFERENCES `uloga` (`KorIme`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `autor`
--

LOCK TABLES `autor` WRITE;
/*!40000 ALTER TABLE `autor` DISABLE KEYS */;
INSERT INTO `autor` VALUES ('djape','Predrag Pesic','2001-04-14','Rodjen u Beogradu, gde je završio osnovnu i srednju školu. Trenutno studira na Elektrotehničkom fakultetu u Beogradu i u slobodno vreme piše knjige.'),('kafka','Franc Kafka','1883-07-03','Franc Kafka (nem. Franz Kafka, češ. František Kafka; Prag, 3. jul 1883 — Klosternojburg, 3. jun 1924) je nemački pisac jevrejsko-češkoga porekla kojeg kritika danas smatra jednim od najvećih autora XX veka. Kafka je govorio i svoja dela pisao na nemačkom jeziku. Dobro je znao i češki jezik. Stilom pisanja, Kafka je pripadao avangardi, pravcu iz srednje faze modernizma, ali je svojim delovanjem uveliko uticao na brojne stilove kasnog modernizma, uključujući i egzistencijalizam. Njegova najznačajnija dela, pripovetka Preobražaj, te romani Proces i Dvorac prepuni su tematike koja predstavlja arhetipove otuđenosti, psihofizičke brutalnosti, sukoba na relaciji roditelji-deca, likova na zastrašujućim putovanjima i mističnih transformacija.'),('tolstoj','Lav Tolstoj','1828-09-09','Lav Nikolajevič Tolstoj (rus. Лев Николаевич Толстой; Jasna Poljana, 9. septembar 1828 — Astapovo, 20. novembar 1910) bio je grof, ruski pisac svrstan u najveće ruske realiste toga doba. Poznat po svoja dva najveća dela, Ana Karenjina i Rat i mir, koja oslikavaju duboku, psihološku i društvenu pozadinu Rusije i njenog društva u 19. veku.\r\nBio je esejista, poznati borac za prava radnika, dramaturg, kritičar i moralni filozof, a pored svega pacifista i levičar. Svojim naprednim idejama o nenasilnom otporu je uticao na ličnosti, koje su se pojavile kasnije, među kojima su najpoznatije Martin Luter King i Gandi. Prema glasanju 125 poznatih svetskih autora Tolstojeve knjige uvrštene su u najveće knjige svih vremena.');
/*!40000 ALTER TABLE `autor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_uloga_KorIme` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_uloga_KorIme` FOREIGN KEY (`user_id`) REFERENCES `uloga` (`KorIme`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2023-06-06 12:03:48.887916','1','Admini',1,'[{\"added\": {}}]',3,'ljubica'),(2,'2023-06-06 12:03:53.270962','2','Kuce',1,'[{\"added\": {}}]',3,'ljubica'),(3,'2023-06-06 12:03:59.563528','3','Korisnici',1,'[{\"added\": {}}]',3,'ljubica'),(4,'2023-06-06 12:04:03.242520','4','Autori',1,'[{\"added\": {}}]',3,'ljubica');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(10,'citajneskitaj','autor'),(11,'citajneskitaj','izdavackakuca'),(7,'citajneskitaj','knjiga'),(17,'citajneskitaj','kolekcija'),(12,'citajneskitaj','korisnik'),(8,'citajneskitaj','licitacija'),(9,'citajneskitaj','najpopularnijimesec'),(20,'citajneskitaj','napisao'),(14,'citajneskitaj','objava'),(16,'citajneskitaj','ponuda'),(19,'citajneskitaj','povezani'),(15,'citajneskitaj','prati'),(18,'citajneskitaj','prodajnamesta'),(13,'citajneskitaj','recenzija'),(6,'citajneskitaj','uloga'),(4,'contenttypes','contenttype'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2023-06-06 08:13:20.433097'),(2,'contenttypes','0002_remove_content_type_name','2023-06-06 08:13:20.468161'),(3,'auth','0001_initial','2023-06-06 08:13:20.553105'),(4,'auth','0002_alter_permission_name_max_length','2023-06-06 08:13:20.574619'),(5,'auth','0003_alter_user_email_max_length','2023-06-06 08:13:20.577451'),(6,'auth','0004_alter_user_username_opts','2023-06-06 08:13:20.581108'),(7,'auth','0005_alter_user_last_login_null','2023-06-06 08:13:20.584043'),(8,'auth','0006_require_contenttypes_0002','2023-06-06 08:13:20.585025'),(9,'auth','0007_alter_validators_add_error_messages','2023-06-06 08:13:20.587671'),(10,'auth','0008_alter_user_username_max_length','2023-06-06 08:13:20.590499'),(11,'auth','0009_alter_user_last_name_max_length','2023-06-06 08:13:20.593143'),(12,'auth','0010_alter_group_name_max_length','2023-06-06 08:13:20.602397'),(13,'auth','0011_update_proxy_permissions','2023-06-06 08:13:20.605537'),(14,'auth','0012_alter_user_first_name_max_length','2023-06-06 08:13:20.608117'),(15,'citajneskitaj','0001_initial','2023-06-06 08:13:21.070904'),(16,'admin','0001_initial','2023-06-06 08:13:21.113969'),(17,'admin','0002_logentry_remove_auto_add','2023-06-06 08:13:21.122627'),(18,'admin','0003_logentry_add_action_flag_choices','2023-06-06 08:13:21.131095'),(19,'citajneskitaj','0002_alter_recenzija_idrec','2023-06-06 08:13:21.147555'),(20,'citajneskitaj','0003_alter_licitacija_idlicitacija_alter_objava_idobjava_and_more','2023-06-06 08:13:21.229249'),(21,'citajneskitaj','0004_alter_recenzija_datumobjave','2023-06-06 08:13:21.237203'),(22,'citajneskitaj','0005_alter_recenzija_datumobjave','2023-06-06 08:13:21.244110'),(23,'citajneskitaj','0006_alter_recenzija_datumobjave_alter_uloga_slika','2023-06-06 08:13:21.256734'),(24,'citajneskitaj','0007_alter_recenzija_datumobjave','2023-06-06 08:13:21.262671'),(25,'citajneskitaj','0008_alter_recenzija_datumobjave','2023-06-06 08:13:21.268541'),(26,'citajneskitaj','0009_alter_recenzija_datumobjave','2023-06-06 08:13:21.274150'),(27,'citajneskitaj','0010_alter_recenzija_datumobjave','2023-06-06 08:13:21.280267'),(28,'sessions','0001_initial','2023-06-06 08:13:21.288092'),(29,'citajneskitaj','0011_alter_knjiga_opis','2023-06-06 12:40:00.533725');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('0au9i2u471ds9ngoc8ynyzdyuq4ow6qz','.eJxVjE0OwiAQhe_C2hCQdqAu3fcMZGCooAaS0rrQeHdp0kV9u_f3fZjFdYl2rWG2idiFvfFViJ2OuUP_CHkr6Y75VrgveZmT49uE723lY6HwvO7bP0DEGtsbwQxSTP0AyoCUHWp_BqUxaKB-IlBeoxHNO0OChO9lp8mICUEGpYxr0FRdbiR5FPv-AHUXPoI:1q6W2N:IxZIFlqVJtM5urlI6h6V8v--UaVzepVPzrjZvpTzTsE','2023-06-20 12:43:47.004573'),('ojweg3o4vg2nmvurw80lq7e466iu7tkj','.eJxVjDsOgzAQBe_iOrIWsFk7ZXrOYO167RiCQOJTRbl7QKJIuifNzHurQPtWwr6mJfSi7mocdu4jqdsvYYqvNJ1YBpqes47ztC0961PRF111N0saH5f7d1BoLUeNDUXfkjW1gQoEsQYxjh1KZmc8g_V1ssit-CwI3GZzjGTQVY0H8OrzBY9oOdY:1q6VPX:gaG4KAjFieeZefNQgQpLL1alIrGdz_QeMZEJgSV-wsQ','2023-06-20 12:03:39.101169'),('q6037aojcw63e3c0euyydwc9b0wr5z10','.eJxVjMEOgjAQRP-lZ9MspWW7Hr37DaTLLhY1QCicjP8uJhz0Npn3Zl6mTdua263o0g5izkbuaVZz-u05dQ8dDzjeJttN47oMbL-KPWix10n0eTncv4OcSt7XWKeOmhS881CBIDoQHzmi9Bw9MQRyGpAboV4QuOn9HtRjrGoCIPP-AP28OQA:1q6Vdw:QsDNyNurbU6HCyOZTkhblhiViD7Ml4bPOqWiY7EK-FI','2023-06-20 12:18:32.833163'),('sgbn2laanc1be0lmm08nzn0ovku2ayzm','.eJxVjb0OgzAQg98lcxUdELikY3eeAd3lQkl_EonAVPXdCxJD8WT5s-yPioWTuir8l7qogdZlGtYS5iHKxt_RUzrnTP4Z0g7lQemetc9pmSPrvaIPWnSfJbxuR_c0MFGZ9uuGvOuoNbWBCgSxBjGWLcrI1jiG1tWhRe7EjYLA3Wg2EwzaqnEATn1__YI-aQ:1q6WXC:D8ebYDOAmRDz5L8pC-ZROQoq8s7LgdV1p8NV0-e6Viw','2023-06-20 13:15:38.506804'),('sgw9gn6k5zkenx1hljqv6bnw127e08ic','.eJxVjE0OgyAQhe_CuiGjAgNddt8zGMaBajWYCK6a3r2YuLBv9fJ-vo_o_V7Gfs9h6ycWdzEvoRRxu-bkhzmko-S3T69VDmsq20TymMizzfK5clge5_YPMPo81jd2fnDGa9UqaIARW2BlySJHssoRaNcGjWTYRUYgE1U1QaFtOgfgKnTKlCrJXCW-P3LOPng:1q6WLs:8lh2-kCeQOWEtuX_VjQUJ_BjNTwW3kv7GRgSQwOxTVg','2023-06-20 13:03:56.957851');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `izdavackakuca`
--

DROP TABLE IF EXISTS `izdavackakuca`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `izdavackakuca` (
  `uloga_ptr_id` varchar(20) NOT NULL,
  `Naziv` varchar(40) NOT NULL,
  `Istorija` varchar(1000) DEFAULT NULL,
  `Adresa` varchar(60) NOT NULL,
  PRIMARY KEY (`uloga_ptr_id`),
  CONSTRAINT `izdavackakuca_uloga_ptr_id_3c26dd62_fk_uloga_KorIme` FOREIGN KEY (`uloga_ptr_id`) REFERENCES `uloga` (`KorIme`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `izdavackakuca`
--

LOCK TABLES `izdavackakuca` WRITE;
/*!40000 ALTER TABLE `izdavackakuca` DISABLE KEYS */;
INSERT INTO `izdavackakuca` VALUES ('dereta','Dereta','Jedna od najstarijih srpskih kuća, izdavačka kuća Dereta prisutna je na srpskoj izdavačkoj sceni već četiri decenije.','Vladimira Rolovica 94, Beograd'),('jasen','Jasen','Izdavačka kuća JASEN osnovana je 1990. godine. Dobila je naziv po drami „Jasen“ Radomana Raca Stanišića. JASEN izdaje knjige u kojima se neguju sadržaji iz oblasti teologije, filozofije, lingvistike, beletristike, arhitekture, medicine i istorije.','Lomina 4, Beograd'),('klett','Klett','Izdavač sa dugogodišnjom tradicijom u izdavanju školskih udžbenika, Klet je jedna od najvećih izdavačkih grupa na svetu, sa zavidnim renomeom u mnogim državama. Grupa Klet je u porodičnoj tradiciji porodice Klet još od 1897. godine. Danas Klet ima preko 3.200 zaposlenih u 15 država i spada među najveće evropske izdavače','Maršala Birjuzova 3, Beograd'),('zavod','Zavod za udžbenike','Najpoznatija državna izdavačka kuća kod nas.','Obilićev venac 5, Beograd');
/*!40000 ALTER TABLE `izdavackakuca` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `knjiga`
--

DROP TABLE IF EXISTS `knjiga`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `knjiga` (
  `ISBN` varchar(20) NOT NULL,
  `Naziv` varchar(40) NOT NULL,
  `Slika` varchar(100) DEFAULT NULL,
  `Opis` varchar(1000) DEFAULT NULL,
  `ProsecnaOcena` decimal(5,2) NOT NULL,
  `IDIzdKuca` varchar(20) NOT NULL,
  PRIMARY KEY (`ISBN`),
  KEY `knjiga_IDIzdKuca_47ae5161_fk_izdavackakuca_uloga_ptr_id` (`IDIzdKuca`),
  CONSTRAINT `knjiga_IDIzdKuca_47ae5161_fk_izdavackakuca_uloga_ptr_id` FOREIGN KEY (`IDIzdKuca`) REFERENCES `izdavackakuca` (`uloga_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `knjiga`
--

LOCK TABLES `knjiga` WRITE;
/*!40000 ALTER TABLE `knjiga` DISABLE KEYS */;
INSERT INTO `knjiga` VALUES ('0000000000000','Operativni sistemi','knjigaImgs/os.png','Udzbenik iz operativnih sistema.',4.50,'jasen'),('1111111111111','Ana Karenjina','knjigaImgs/ana_karenjina.jpg','Čini se da Ana Karenjina ima sve što se poželeti može – lepa je, bogata, omiljena u društvu, a njen sin je jednostavno obožava. Međutim, Ana ipak oseća da je život suviše prazan, sve dok ne sretne naočitog i šarmantnog oficira, grofa Vronskog. Njihova veza postaće pravi skandal u visokom društvu i izazvaće ogorčenost i zavist ljudi koji okružuju ovo dvoje ljubavnika. Strastvenoj ljubavi i Aninom putu ka samouništenju suprotstavljena je priča Konstantina Ljevina, mladog čoveka koji teži tome da pronađe spokoj i smisao života – briljantan autoportret samog autora ove izuzetne, bezvremene knjige.',0.00,'klett'),('2222222222222','Rat i mir I tom','knjigaImgs/rat_i_mir_i.jpg','U ovom Tolstojevom remek – delu, jednom od najznačajnijih velikih romana XIX veka, prepliću se životi pojedinaca sa velikim svetskoistorijskim događajima u vreme Napoleonovih ratova i francuske invazije na Rusiju. Sudbine Rostovljevih i Bolkonskih, Nataše i Andreja, intimno su povezane sa epskim odvijanjem istorije koja, u Tolstojevom delu, teče paralelno sa njihovim životima. Slike raskošnih balova smenjuju se sa slikama ratnih taktika. Nasilne scene ratnih okršaja ukrštaju se sa svakodnevnim ljudskim strastima i željama u ovom romanu koji spada među najuticajnija dela svjetske književnosti.',2.00,'jasen'),('3333333333333','Rat i mir II tom','knjigaImgs/rat_i_mir_ii.jpg','Nastavak sjajne drame Rat i mir.',5.00,'jasen'),('4444444444444','Detinjstvo','knjigaImgs/detinjstvo.jpeg','Detinjstvo (prereformski ruski: Dѣtstvo; poreformski ruski: Detstvo, tr. Detstvo) je prvi objavljeni roman Lava Tolstoja, objavljen pod inicijalima L. N. u novembarskom broju popularnog ruskog književnog časopisa Savremenik iz 1852. godine.\n\nTo je prvi u nizu od tri romana, a zatim slede Dečaštvo i Mladost. Objavljena kada je Tolstoj imao samo dvadeset tri godine, knjiga je odmah postigla uspeh. To je Tolstoja privuklo pažnju drugih ruskih romanopisaca, uključujući Ivana Turgenjeva, koji je mladog Tolstoja najavio kao glavnu ličnost u usponu ruske književnosti.',0.00,'dereta'),('5555555555555','Proces','knjigaImgs/proces.jpeg','Jedan od najznačajnijih romana XX veka. Jozef K., perspektivni prokurista jedne velike banke, uhapšen je na svoj 30. rođendan, rano ujutro, čim je otvorio oči. Optužba nije poznata, baš kao ni to pred kojim se sudom vodi postupak i kakav će biti njegov tok. Jozefu K. saopštavaju da sud ne želi da remeti njegov uobičajeni način života, te da se on, u skladu s tim, slobodno može vratiti svakodnevnim aktivnostima. Međutim, K. se narednih dana i meseci sve više zapliće u nevidljivu mrežu svog procesa i nedokučivog suda koji ga je pokrenuo. Korak po korak, Jozef K. saznaje da „sve pripada sudu“.   Uoči svog 31. rođendana, godinu dana po hapšenju, Jozef K. spremno čeka dželate…',0.00,'klett'),('6666666666666','Preobrazaj','knjigaImgs/preobrazaj.jpeg','U Preobražaju je posejano seme za preobražaj svetske književnosti, na način, do tada, u književnosti neviđen: premisa da je Gregor Samsa, tek tako, probudivši se, shvatio da se, u toku noći, preobrazio u bubu (na nemačkom ungeheures Ungeziefer, doslovno u čudovišnu štetočinu) dovedena je, u svojoj unutrašnjoj logici, do savršenstva. Prva pomisao Gregora Samse ne tiče se preobražaja njegovog tela u bubu, već toga šta će sada da radi (!) – kako će da se pojavi na oči svojoj porodici, čije izdržavanje je, mahom, u njegovim rukama; kako će da ode na posao, kada ne može ni da se okrene ni da stane na svoje tanke i dlakave nožice. Kafkin protagonist se, uopšte, ne pita kako je do preobražaja došlo, to ga se ne tiče jer deluje da je čitav njegov život, njegov svet, podređen sistemima porodice i posla; nema mesta za njega, kao pojedinca, već za zupčanik, šraf u mašineriji života u savremenom svetu koji ga proždire, a da on to i ne zna i da ga se to i ne tiče.',0.00,'klett'),('7777777777777','Dvorac','knjigaImgs/dvorac.jpeg','Poslednje, a možda i najznačajnije delo Franca Kafke. Radnja romana se dešava u selu kojim dominira dvorac. Vreme kao da je stalo u ovom zimskom krajoliku i gotovo sve scene se dešavaju u mraku. Roman počiva na dvema tezama: jedna je osećaj beznačajnosti i nemoći pojedinca u nepoznatoj sredini, a druga je skrivena moć vladanja nad drugima. U prvoj tezi oličen je glavni junak, geometar K, koji pokušava da prebrodi osećaj beznačajnosti i izgubljenosti nakon samo nedelju dana boravka u selu. On pokušava da se izbori sa tajanstvenim zamkom, koji upravlja selom i koji ne dozvoljava da mu se iko približi osim par službenika koji idu po selu i skupljaju podatke za...',0.00,'klett');
/*!40000 ALTER TABLE `knjiga` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kolekcija`
--

DROP TABLE IF EXISTS `kolekcija`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kolekcija` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `ISBN` varchar(20) NOT NULL,
  `KorIme` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `kolekcija_KorIme_ISBN_0edfd23b_uniq` (`KorIme`,`ISBN`),
  KEY `kolekcija_ISBN_5d8af367_fk_knjiga_ISBN` (`ISBN`),
  CONSTRAINT `kolekcija_ISBN_5d8af367_fk_knjiga_ISBN` FOREIGN KEY (`ISBN`) REFERENCES `knjiga` (`ISBN`),
  CONSTRAINT `kolekcija_KorIme_44f593ae_fk_uloga_KorIme` FOREIGN KEY (`KorIme`) REFERENCES `uloga` (`KorIme`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kolekcija`
--

LOCK TABLES `kolekcija` WRITE;
/*!40000 ALTER TABLE `kolekcija` DISABLE KEYS */;
INSERT INTO `kolekcija` VALUES (6,'6666666666666','djape'),(1,'0000000000000','ljubica'),(2,'1111111111111','ljubica'),(3,'0000000000000','mican'),(4,'2222222222222','mican'),(5,'3333333333333','mican');
/*!40000 ALTER TABLE `kolekcija` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `korisnik`
--

DROP TABLE IF EXISTS `korisnik`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `korisnik` (
  `uloga_ptr_id` varchar(20) NOT NULL,
  `ImePrezime` varchar(40) NOT NULL,
  `DatumRodjenja` date NOT NULL,
  PRIMARY KEY (`uloga_ptr_id`),
  CONSTRAINT `korisnik_uloga_ptr_id_3cd2ff5d_fk_uloga_KorIme` FOREIGN KEY (`uloga_ptr_id`) REFERENCES `uloga` (`KorIme`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `korisnik`
--

LOCK TABLES `korisnik` WRITE;
/*!40000 ALTER TABLE `korisnik` DISABLE KEYS */;
INSERT INTO `korisnik` VALUES ('ljubica','Ljubica Muravljov','2001-12-21'),('mican','Aleksa Micanovic','2001-09-24'),('nevajda','Luka Nevajda','2000-11-10');
/*!40000 ALTER TABLE `korisnik` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `licitacija`
--

DROP TABLE IF EXISTS `licitacija`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `licitacija` (
  `IDLicitacija` int NOT NULL AUTO_INCREMENT,
  `NazivDela` varchar(40) NOT NULL,
  `PDF` varchar(100) DEFAULT NULL,
  `DatumPocetka` datetime(6) NOT NULL,
  `DatumKraja` datetime(6) NOT NULL,
  `PocetnaCena` int NOT NULL,
  `TrenutniIznos` int NOT NULL,
  `IDAutor` varchar(20) NOT NULL,
  `IDPobednik` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`IDLicitacija`),
  KEY `licitacija_IDAutor_a111d448_fk_autor_uloga_ptr_id` (`IDAutor`),
  KEY `licitacija_IDPobednik_cd20ded9_fk_izdavackakuca_uloga_ptr_id` (`IDPobednik`),
  CONSTRAINT `licitacija_IDAutor_a111d448_fk_autor_uloga_ptr_id` FOREIGN KEY (`IDAutor`) REFERENCES `autor` (`uloga_ptr_id`),
  CONSTRAINT `licitacija_IDPobednik_cd20ded9_fk_izdavackakuca_uloga_ptr_id` FOREIGN KEY (`IDPobednik`) REFERENCES `izdavackakuca` (`uloga_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `licitacija`
--

LOCK TABLES `licitacija` WRITE;
/*!40000 ALTER TABLE `licitacija` DISABLE KEYS */;
INSERT INTO `licitacija` VALUES (1,'Operativni sistemi','izmenitiOvdePutanju','2023-04-10 00:00:00.000000','2023-04-15 00:00:00.000000',200,2000,'djape','jasen'),(2,'KDP','pdfs/KDP_Udzbenik_882UIhl_QhMZyHI.pdf','2023-06-06 12:20:17.403870','2023-06-08 14:18:00.000000',300,3000,'djape','zavod');
/*!40000 ALTER TABLE `licitacija` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `najpopularnijimesec`
--

DROP TABLE IF EXISTS `najpopularnijimesec`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `najpopularnijimesec` (
  `IDOcenjenog` varchar(20) NOT NULL,
  `ProsecnaOcena` decimal(5,2) NOT NULL,
  `Tip` varchar(1) NOT NULL,
  PRIMARY KEY (`IDOcenjenog`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `najpopularnijimesec`
--

LOCK TABLES `najpopularnijimesec` WRITE;
/*!40000 ALTER TABLE `najpopularnijimesec` DISABLE KEYS */;
INSERT INTO `najpopularnijimesec` VALUES ('0000000000000',4.50,'K'),('2222222222222',2.00,'K'),('3333333333333',5.00,'K'),('dereta',0.00,'I'),('djape',2.00,'A'),('jasen',0.00,'I'),('kafka',0.00,'A'),('klett',0.00,'I'),('tolstoj',4.00,'A');
/*!40000 ALTER TABLE `najpopularnijimesec` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `napisao`
--

DROP TABLE IF EXISTS `napisao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `napisao` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `ISBN` varchar(20) NOT NULL,
  `IDAutor` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `napisao_IDAutor_ISBN_46052d4b_uniq` (`IDAutor`,`ISBN`),
  KEY `napisao_ISBN_12ac9a02_fk_knjiga_ISBN` (`ISBN`),
  CONSTRAINT `napisao_IDAutor_0ce38672_fk_autor_uloga_ptr_id` FOREIGN KEY (`IDAutor`) REFERENCES `autor` (`uloga_ptr_id`),
  CONSTRAINT `napisao_ISBN_12ac9a02_fk_knjiga_ISBN` FOREIGN KEY (`ISBN`) REFERENCES `knjiga` (`ISBN`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `napisao`
--

LOCK TABLES `napisao` WRITE;
/*!40000 ALTER TABLE `napisao` DISABLE KEYS */;
INSERT INTO `napisao` VALUES (1,'0000000000000','djape'),(6,'5555555555555','kafka'),(7,'6666666666666','kafka'),(8,'7777777777777','kafka'),(2,'1111111111111','tolstoj'),(9,'2222222222222','tolstoj'),(4,'3333333333333','tolstoj'),(5,'4444444444444','tolstoj');
/*!40000 ALTER TABLE `napisao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `objava`
--

DROP TABLE IF EXISTS `objava`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `objava` (
  `IDObjava` int NOT NULL AUTO_INCREMENT,
  `Sadrzaj` varchar(1000) NOT NULL,
  `DatumObjave` datetime(6) NOT NULL,
  `Slika` varchar(100) DEFAULT NULL,
  `KorIme` varchar(20) NOT NULL,
  PRIMARY KEY (`IDObjava`),
  KEY `objava_KorIme_c8edcadd_fk_uloga_KorIme` (`KorIme`),
  CONSTRAINT `objava_KorIme_c8edcadd_fk_uloga_KorIme` FOREIGN KEY (`KorIme`) REFERENCES `uloga` (`KorIme`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `objava`
--

LOCK TABLES `objava` WRITE;
/*!40000 ALTER TABLE `objava` DISABLE KEYS */;
INSERT INTO `objava` VALUES (1,'Danas je lep dan, nisam popio ban. Za razliku od Nevajde Luke, teške li su mu muke.','2023-05-01 00:00:00.000000',NULL,'djape'),(2,'Dela Lava Tolstoja od sada možete videti i na aplikaciji Čitaj ne skitaj.','2021-07-23 00:00:00.000000','objavaImgs/tolstoj.jpg','tolstoj'),(3,'Jako mi se svidja nova Peđina knjiga!','2023-04-15 00:00:00.000000','objavaImgs/micanov_ket.jpg','ljubica'),(4,'Novosti o popustima mozete pronaci na nasoj web stranici.','2022-09-10 00:00:00.000000','objavaImgs/klett.png','klett'),(5,'Rat i mir od sad i u izdanju Jasena!','2023-06-06 12:46:15.950887','','jasen');
/*!40000 ALTER TABLE `objava` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ponuda`
--

DROP TABLE IF EXISTS `ponuda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ponuda` (
  `IDPonuda` int NOT NULL AUTO_INCREMENT,
  `Iznos` int NOT NULL,
  `IDLicitacija` int NOT NULL,
  `IDIzdKuca` varchar(20) NOT NULL,
  PRIMARY KEY (`IDPonuda`),
  KEY `ponuda_IDIzdKuca_ca9bc52b_fk_izdavackakuca_uloga_ptr_id` (`IDIzdKuca`),
  KEY `ponuda_IDLicitacija_e207ca41_fk` (`IDLicitacija`),
  CONSTRAINT `ponuda_IDIzdKuca_ca9bc52b_fk_izdavackakuca_uloga_ptr_id` FOREIGN KEY (`IDIzdKuca`) REFERENCES `izdavackakuca` (`uloga_ptr_id`),
  CONSTRAINT `ponuda_IDLicitacija_e207ca41_fk` FOREIGN KEY (`IDLicitacija`) REFERENCES `licitacija` (`IDLicitacija`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ponuda`
--

LOCK TABLES `ponuda` WRITE;
/*!40000 ALTER TABLE `ponuda` DISABLE KEYS */;
INSERT INTO `ponuda` VALUES (1,200,1,'klett'),(2,1600,1,'dereta'),(3,2000,1,'jasen'),(4,400,2,'jasen'),(5,1500,2,'klett'),(6,1800,2,'dereta'),(7,3000,2,'zavod');
/*!40000 ALTER TABLE `ponuda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `povezani`
--

DROP TABLE IF EXISTS `povezani`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `povezani` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `IDAutor` varchar(20) NOT NULL,
  `IDIzdKuca` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `povezani_IDAutor_IDIzdKuca_9c4b656e_uniq` (`IDAutor`,`IDIzdKuca`),
  KEY `povezani_IDIzdKuca_2fd9ac00_fk_izdavackakuca_uloga_ptr_id` (`IDIzdKuca`),
  CONSTRAINT `povezani_IDAutor_a4245922_fk_autor_uloga_ptr_id` FOREIGN KEY (`IDAutor`) REFERENCES `autor` (`uloga_ptr_id`),
  CONSTRAINT `povezani_IDIzdKuca_2fd9ac00_fk_izdavackakuca_uloga_ptr_id` FOREIGN KEY (`IDIzdKuca`) REFERENCES `izdavackakuca` (`uloga_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `povezani`
--

LOCK TABLES `povezani` WRITE;
/*!40000 ALTER TABLE `povezani` DISABLE KEYS */;
INSERT INTO `povezani` VALUES (2,'djape','jasen'),(1,'djape','klett'),(6,'kafka','klett'),(5,'tolstoj','dereta'),(4,'tolstoj','jasen'),(3,'tolstoj','klett');
/*!40000 ALTER TABLE `povezani` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prati`
--

DROP TABLE IF EXISTS `prati`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prati` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `IDPracen` varchar(20) NOT NULL,
  `IDPratilac` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `prati_IDPratilac_IDPracen_1dd94902_uniq` (`IDPratilac`,`IDPracen`),
  KEY `prati_IDPracen_ff80d1a1_fk_uloga_KorIme` (`IDPracen`),
  CONSTRAINT `prati_IDPracen_ff80d1a1_fk_uloga_KorIme` FOREIGN KEY (`IDPracen`) REFERENCES `uloga` (`KorIme`),
  CONSTRAINT `prati_IDPratilac_80f56ac6_fk_uloga_KorIme` FOREIGN KEY (`IDPratilac`) REFERENCES `uloga` (`KorIme`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prati`
--

LOCK TABLES `prati` WRITE;
/*!40000 ALTER TABLE `prati` DISABLE KEYS */;
INSERT INTO `prati` VALUES (6,'jasen','djape'),(3,'dereta','ljubica'),(2,'djape','ljubica'),(1,'mican','ljubica'),(4,'ljubica','mican'),(5,'tolstoj','mican'),(7,'zavod','mican');
/*!40000 ALTER TABLE `prati` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prodajnamesta`
--

DROP TABLE IF EXISTS `prodajnamesta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prodajnamesta` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `Adresa` varchar(60) NOT NULL,
  `IDIzdKuca` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `prodajnamesta_IDIzdKuca_Adresa_5130a72e_uniq` (`IDIzdKuca`,`Adresa`),
  CONSTRAINT `prodajnamesta_IDIzdKuca_b706228d_fk_izdavackakuca_uloga_ptr_id` FOREIGN KEY (`IDIzdKuca`) REFERENCES `izdavackakuca` (`uloga_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prodajnamesta`
--

LOCK TABLES `prodajnamesta` WRITE;
/*!40000 ALTER TABLE `prodajnamesta` DISABLE KEYS */;
INSERT INTO `prodajnamesta` VALUES (2,'Knez Mihailova 46, Beograd','dereta'),(9,'Kosovska 45, Beograd','zavod'),(10,'Obilićev venac 5, Beograd','zavod'),(11,'Palmotićeva 1a, Beograd','zavod');
/*!40000 ALTER TABLE `prodajnamesta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recenzija`
--

DROP TABLE IF EXISTS `recenzija`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recenzija` (
  `IDRec` int NOT NULL AUTO_INCREMENT,
  `Ocena` decimal(5,1) NOT NULL,
  `DatumObjave` datetime(6) NOT NULL,
  `Tekst` varchar(1000) NOT NULL,
  `IDDavalac` varchar(20) NOT NULL,
  `IDPrimalacKnjiga` varchar(20) DEFAULT NULL,
  `IDPrimalacUloga` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`IDRec`),
  KEY `recenzija_IDDavalac_69400301_fk_uloga_KorIme` (`IDDavalac`),
  KEY `recenzija_IDPrimalacKnjiga_729376f2_fk_knjiga_ISBN` (`IDPrimalacKnjiga`),
  KEY `recenzija_IDPrimalacUloga_df3ccd1d_fk_uloga_KorIme` (`IDPrimalacUloga`),
  CONSTRAINT `recenzija_IDDavalac_69400301_fk_uloga_KorIme` FOREIGN KEY (`IDDavalac`) REFERENCES `uloga` (`KorIme`),
  CONSTRAINT `recenzija_IDPrimalacKnjiga_729376f2_fk_knjiga_ISBN` FOREIGN KEY (`IDPrimalacKnjiga`) REFERENCES `knjiga` (`ISBN`),
  CONSTRAINT `recenzija_IDPrimalacUloga_df3ccd1d_fk_uloga_KorIme` FOREIGN KEY (`IDPrimalacUloga`) REFERENCES `uloga` (`KorIme`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recenzija`
--

LOCK TABLES `recenzija` WRITE;
/*!40000 ALTER TABLE `recenzija` DISABLE KEYS */;
INSERT INTO `recenzija` VALUES (1,5.0,'2023-04-15 00:00:00.000000','Sjajna knjiga, vise puta sam je procitala.','ljubica','0000000000000',NULL),(2,4.0,'2023-04-16 00:00:00.000000','Dobra knjiga, pomogla mi je da dam OS u septembru.','nevajda','0000000000000',NULL),(3,4.0,'2023-04-17 00:00:00.000000','Iskreno, jako kvalitetan pisac. Mnogo mi se svidja njegova brada.','nevajda',NULL,'tolstoj'),(4,2.0,'2023-04-18 00:00:00.000000','Ocekivao sam mnogo vise od knjige.','mican','2222222222222',NULL),(5,5.0,'2023-04-19 00:00:00.000000','U potpunosti je dopunio sve nedostatke iz prvog toma.','mican','3333333333333',NULL),(6,2.0,'2023-04-20 00:00:00.000000','Moj brat, ali ne zna da pise.','mican',NULL,'djape'),(7,5.0,'2023-06-06 12:16:13.790098','Iskreno najjači udžbenici!','mican',NULL,'zavod');
/*!40000 ALTER TABLE `recenzija` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `uloga`
--

DROP TABLE IF EXISTS `uloga`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `uloga` (
  `is_superuser` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `KorIme` varchar(20) NOT NULL,
  `Sifra` varchar(128) NOT NULL,
  `Email` varchar(40) NOT NULL,
  `Slika` varchar(100) DEFAULT NULL,
  `BrPratilaca` int NOT NULL,
  `ProsecnaOcena` decimal(5,2) NOT NULL,
  `Tip` varchar(1) NOT NULL,
  `Banovan` tinyint(1) NOT NULL,
  PRIMARY KEY (`KorIme`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `uloga`
--

LOCK TABLES `uloga` WRITE;
/*!40000 ALTER TABLE `uloga` DISABLE KEYS */;
INSERT INTO `uloga` VALUES (0,0,1,'dereta','pbkdf2_sha256$600000$dzqCyi5ntJCgq1jRa4yn0v$HwR28mG1geKLDhgaBhMBynZZepUXWxaA6XTKHFDtxYE=','dereta@etf.rs','ulogaImgs/dereta.jpg',1,0.00,'I',0),(0,0,1,'djape','pbkdf2_sha256$600000$dzqCyi5ntJCgq1jRa4yn0v$HwR28mG1geKLDhgaBhMBynZZepUXWxaA6XTKHFDtxYE=','djape@etf.rs','ulogaImgs/pedja_profilna.jpg',1,2.00,'A',0),(0,0,1,'jasen','pbkdf2_sha256$600000$dzqCyi5ntJCgq1jRa4yn0v$HwR28mG1geKLDhgaBhMBynZZepUXWxaA6XTKHFDtxYE=','jasen@etf.rs','ulogaImgs/jasen.png',1,0.00,'I',0),(0,0,1,'kafka','pbkdf2_sha256$600000$dzqCyi5ntJCgq1jRa4yn0v$HwR28mG1geKLDhgaBhMBynZZepUXWxaA6XTKHFDtxYE=','kafka@etf.rs','ulogaImgs/kafka.jpg',0,0.00,'A',0),(0,0,1,'klett','pbkdf2_sha256$600000$dzqCyi5ntJCgq1jRa4yn0v$HwR28mG1geKLDhgaBhMBynZZepUXWxaA6XTKHFDtxYE=','klett@etf.rs','ulogaImgs/klett.png',0,0.00,'I',0),(1,1,1,'ljubica','pbkdf2_sha256$600000$dzqCyi5ntJCgq1jRa4yn0v$HwR28mG1geKLDhgaBhMBynZZepUXWxaA6XTKHFDtxYE=','ljubica@etf.rs','ulogaImgs/ljubica_profilna.jpg',1,0.00,'K',0),(0,0,1,'mican','pbkdf2_sha256$600000$dzqCyi5ntJCgq1jRa4yn0v$HwR28mG1geKLDhgaBhMBynZZepUXWxaA6XTKHFDtxYE=','mican@etf.rs','ulogaImgs/mican_profilna.jpg',1,0.00,'K',0),(0,0,0,'nevajda','pbkdf2_sha256$600000$dzqCyi5ntJCgq1jRa4yn0v$HwR28mG1geKLDhgaBhMBynZZepUXWxaA6XTKHFDtxYE=','nevajda@etf.rs',NULL,0,0.00,'K',1),(0,0,1,'tolstoj','pbkdf2_sha256$600000$dzqCyi5ntJCgq1jRa4yn0v$HwR28mG1geKLDhgaBhMBynZZepUXWxaA6XTKHFDtxYE=','tolstoj@etf.rs','ulogaImgs/tolstoj.jpg',1,4.00,'A',0),(0,0,1,'zavod','pbkdf2_sha256$600000$mcB7tYfOUnZpqbx3ZHGVCM$Xh73BpK60pBWRMxHTRkMpIeF828N5mO0U5+BRVo3aq8=','zavod@etf.rs','ulogaImgs/zavod.png',1,5.00,'I',0);
/*!40000 ALTER TABLE `uloga` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `uloga_groups`
--

DROP TABLE IF EXISTS `uloga_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `uloga_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `uloga_id` varchar(20) NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uloga_groups_uloga_id_group_id_dc255368_uniq` (`uloga_id`,`group_id`),
  KEY `uloga_groups_group_id_0cee1529_fk_auth_group_id` (`group_id`),
  CONSTRAINT `uloga_groups_group_id_0cee1529_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `uloga_groups_uloga_id_48ea24e3_fk_uloga_KorIme` FOREIGN KEY (`uloga_id`) REFERENCES `uloga` (`KorIme`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `uloga_groups`
--

LOCK TABLES `uloga_groups` WRITE;
/*!40000 ALTER TABLE `uloga_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `uloga_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `uloga_user_permissions`
--

DROP TABLE IF EXISTS `uloga_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `uloga_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `uloga_id` varchar(20) NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uloga_user_permissions_uloga_id_permission_id_e1b7990a_uniq` (`uloga_id`,`permission_id`),
  KEY `uloga_user_permissio_permission_id_2bb13e35_fk_auth_perm` (`permission_id`),
  CONSTRAINT `uloga_user_permissio_permission_id_2bb13e35_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `uloga_user_permissions_uloga_id_b4721777_fk_uloga_KorIme` FOREIGN KEY (`uloga_id`) REFERENCES `uloga` (`KorIme`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `uloga_user_permissions`
--

LOCK TABLES `uloga_user_permissions` WRITE;
/*!40000 ALTER TABLE `uloga_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `uloga_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-06 15:26:01
