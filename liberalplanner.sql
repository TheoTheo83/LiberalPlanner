-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : mar. 11 juil. 2023 à 11:38
-- Version du serveur : 8.0.31
-- Version de PHP : 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `liberalplanner`
--

-- --------------------------------------------------------

--
-- Structure de la table `parents`
--

DROP TABLE IF EXISTS `parents`;
CREATE TABLE IF NOT EXISTS `parents` (
  `ID_Parent` int NOT NULL,
  `ID_Patients` int DEFAULT NULL,
  `Prenom` varchar(255) DEFAULT NULL,
  `Nom` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID_Parent`),
  KEY `ID_Patients` (`ID_Patients`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `parents`
--

INSERT INTO `parents` (`ID_Parent`, `ID_Patients`, `Prenom`, `Nom`) VALUES
(1, 1, 'luis', 'cabral'),
(2, 1, 'theo', 'Dupont'),
(3, 2, 'benoit', 'Martin');

-- --------------------------------------------------------

--
-- Structure de la table `pathologies`
--

DROP TABLE IF EXISTS `pathologies`;
CREATE TABLE IF NOT EXISTS `pathologies` (
  `ID_Pathologie` int NOT NULL,
  `ID_Patients` int DEFAULT NULL,
  `Pathologie` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID_Pathologie`),
  KEY `ID_Patients` (`ID_Patients`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `pathologies`
--

INSERT INTO `pathologies` (`ID_Pathologie`, `ID_Patients`, `Pathologie`) VALUES
(1, 1, 'Diabète'),
(2, 3, 'Hypertension'),
(3, 2, 'Asthme');

-- --------------------------------------------------------

--
-- Structure de la table `patients`
--

DROP TABLE IF EXISTS `patients`;
CREATE TABLE IF NOT EXISTS `patients` (
  `ID_Patients` int NOT NULL,
  `Prenom` varchar(255) DEFAULT NULL,
  `Nom` varchar(255) DEFAULT NULL,
  `DateNaissance` date DEFAULT NULL,
  `Age` int DEFAULT NULL,
  PRIMARY KEY (`ID_Patients`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `patients`
--

INSERT INTO `patients` (`ID_Patients`, `Prenom`, `Nom`, `DateNaissance`, `Age`) VALUES
(1, 'Jean', 'Dupont', '1990-05-15', 31),
(2, 'Marie', 'Martin', '1985-09-22', 36),
(3, 'Pierre', 'Dubois', '1995-02-10', 26);

-- --------------------------------------------------------

--
-- Structure de la table `remarques`
--

DROP TABLE IF EXISTS `remarques`;
CREATE TABLE IF NOT EXISTS `remarques` (
  `ID_Remarque` int NOT NULL,
  `ID_Patients` int DEFAULT NULL,
  `Remarque` text,
  PRIMARY KEY (`ID_Remarque`),
  KEY `ID_Patients` (`ID_Patients`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `remarques`
--

INSERT INTO `remarques` (`ID_Remarque`, `ID_Patients`, `Remarque`) VALUES
(1, 1, 'Allergie aux fruits à coque'),
(2, 2, 'Pratique régulière de sport');

-- --------------------------------------------------------

--
-- Structure de la table `rendezvous`
--

DROP TABLE IF EXISTS `rendezvous`;
CREATE TABLE IF NOT EXISTS `rendezvous` (
  `ID_RendezVous` int NOT NULL,
  `ID_Patients` int DEFAULT NULL,
  `DateRdv` date DEFAULT NULL,
  `TarifPrestation` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`ID_RendezVous`),
  KEY `ID_Patients` (`ID_Patients`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `rendezvous`
--

INSERT INTO `rendezvous` (`ID_RendezVous`, `ID_Patients`, `DateRdv`, `TarifPrestation`) VALUES
(1, 1, '2023-07-15', '50.00'),
(2, 3, '2023-07-20', '60.00'),
(3, 2, '2023-07-18', '45.00');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
