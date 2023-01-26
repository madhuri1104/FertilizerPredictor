-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3307
-- Generation Time: Oct 12, 2022 at 12:39 PM
-- Server version: 10.4.19-MariaDB
-- PHP Version: 8.0.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fertilizer_predictor`
--
CREATE DATABASE IF NOT EXISTS `fertilizer_predictor` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `fertilizer_predictor`;

-- --------------------------------------------------------

--
-- Table structure for table `customer_details`
--

CREATE TABLE `customer_details` (
  `Customer_ID` int(20) NOT NULL,
  `Name` varchar(30) NOT NULL,
  `Village` varchar(30) NOT NULL,
  `Mobile_Number` bigint(14) DEFAULT NULL,
  `Email_Address` varchar(30) DEFAULT NULL,
  `Password` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `customer_details`
--

INSERT INTO `customer_details` (`Customer_ID`, `Name`, `Village`, `Mobile_Number`, `Email_Address`, `Password`) VALUES
(1001, 'Shubhada', 'Wategaon', 9123456789, 'shubhada.rajmane007@gmail.com', 'Shubhada123');

-- --------------------------------------------------------

--
-- Table structure for table `customer_records`
--

CREATE TABLE `customer_records` (
  `Customer_ID` int(20) DEFAULT NULL,
  `Temperature` float(15,5) NOT NULL,
  `Humidity` float(15,5) NOT NULL,
  `N` float(15,5) NOT NULL,
  `P` float(15,5) NOT NULL,
  `K` float(15,5) NOT NULL,
  `Soil_Type` varchar(30) NOT NULL,
  `Crop_Type` varchar(30) NOT NULL,
  `Fertilizer` varchar(30) NOT NULL,
  `Date` date DEFAULT curdate()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `customer_records`
--

INSERT INTO `customer_records` (`Customer_ID`, `Temperature`, `Humidity`, `N`, `P`, `K`, `Soil_Type`, `Crop_Type`, `Fertilizer`, `Date`) VALUES
(1001, 23.00000, 24.00000, 89.00000, 45.00000, 78.00000, 'soil', 'crop', 'udp', '2022-10-10');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customer_details`
--
ALTER TABLE `customer_details`
  ADD PRIMARY KEY (`Customer_ID`),
  ADD UNIQUE KEY `Mobile_Number` (`Mobile_Number`),
  ADD UNIQUE KEY `Email_Address` (`Email_Address`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
