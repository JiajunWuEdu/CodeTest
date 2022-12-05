SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

-- Create User `mylearning` --

CREATE USER 'mylearning'@'localhost' IDENTIFIED by 'mylearning'; 

-- ------------------------------
-- Create Database `mylearning` --

CREATE DATABASE IF NOT EXISTS `mylearning`;

GRANT ALL PRIVILEGES ON `mylearning`.* TO 'mylearning'@'localhost';

-- ------------------------------

use `mylearning`;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;


CREATE TABLE `dataset` (
  `id` int(11) NOT NULL,
  `project_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `file_path` varchar(255) DEFAULT NULL,
  `row_count` int(11) DEFAULT NULL,
  `visualization_path` varchar(255) DEFAULT NULL,
  `upload_time` timestamp NULL DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `delete_time` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE `experiment` (
  `id` int(11) NOT NULL,
  `project_id` int(11) NOT NULL,
  `dataset_id` int(11) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `result_id` int(11) DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NULL DEFAULT NULL,
  `delete_time` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `project` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `delete_time` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `result` (
  `id` int(11) NOT NULL,
  `experiment_id` int(11) NOT NULL,
  `dataset_id` int(11) NOT NULL,
  `model` varchar(100) NOT NULL,
  `result_json` text,
  `result_text` text,
  `visualization_path` varchar(255) DEFAULT NULL,
  `finish_time` timestamp NULL DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `delete_time` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


ALTER TABLE `dataset`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_dataset_project` (`project_id`);


ALTER TABLE `experiment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_experiment_dataset` (`dataset_id`),
  ADD KEY `fk_experiment_project` (`project_id`),
  ADD KEY `fk_experiment_result` (`result_id`);


ALTER TABLE `project`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `result`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `dataset`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE `experiment`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE `project`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE `result`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE `dataset`
  ADD CONSTRAINT `fk_dataset_project` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;


ALTER TABLE `experiment`
  ADD CONSTRAINT `fk_experiment_dataset` FOREIGN KEY (`dataset_id`) REFERENCES `dataset` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_experiment_project` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_experiment_result` FOREIGN KEY (`result_id`) REFERENCES `result` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;
  
ALTER TABLE `result`
  ADD CONSTRAINT `fk_result_dataset` FOREIGN KEY (`dataset_id`) REFERENCES `dataset`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_result_experiment` FOREIGN KEY (`experiment_id`) REFERENCES `experiment`(`id`) ON DELETE CASCADE ON UPDATE CASCADE; 
  
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;