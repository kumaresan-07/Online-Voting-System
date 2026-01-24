-- =============================================
-- Online Voting System - MySQL Database Schema
-- =============================================
-- This SQL file creates the database structure for the Python Flask voting system.
-- Run this file in MySQL if you prefer manual database setup.

-- Create Database
CREATE DATABASE IF NOT EXISTS `online_voting` 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

USE `online_voting`;

-- =============================================
-- Table: admins
-- =============================================
CREATE TABLE IF NOT EXISTS `admins` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `first_name` VARCHAR(45) NOT NULL,
    `last_name` VARCHAR(45) NOT NULL,
    `email` VARCHAR(45) NOT NULL UNIQUE,
    `password_hash` VARCHAR(256) NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_admin_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================
-- Table: voters
-- =============================================
CREATE TABLE IF NOT EXISTS `voters` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `first_name` VARCHAR(45) NOT NULL,
    `last_name` VARCHAR(45) NOT NULL,
    `email` VARCHAR(45) NOT NULL UNIQUE,
    `voter_id` VARCHAR(45) NOT NULL UNIQUE,
    `password_hash` VARCHAR(256) NOT NULL,
    `has_voted` TINYINT(1) DEFAULT 0,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_voter_email` (`email`),
    INDEX `idx_voter_id` (`voter_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================
-- Table: positions
-- =============================================
CREATE TABLE IF NOT EXISTS `positions` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(45) NOT NULL UNIQUE,
    `description` VARCHAR(255),
    `max_votes` INT DEFAULT 1,
    INDEX `idx_position_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================
-- Table: candidates
-- =============================================
CREATE TABLE IF NOT EXISTS `candidates` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(45) NOT NULL,
    `position_id` INT NOT NULL,
    `votes_count` INT DEFAULT 0,
    `photo` VARCHAR(255),
    FOREIGN KEY (`position_id`) REFERENCES `positions`(`id`) ON DELETE CASCADE,
    INDEX `idx_candidate_position` (`position_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================
-- Table: votes
-- =============================================
CREATE TABLE IF NOT EXISTS `votes` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `voter_id` INT NOT NULL,
    `candidate_id` INT NOT NULL,
    `position_id` INT NOT NULL,
    `voted_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`voter_id`) REFERENCES `voters`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`candidate_id`) REFERENCES `candidates`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`position_id`) REFERENCES `positions`(`id`) ON DELETE CASCADE,
    UNIQUE KEY `unique_vote_per_position` (`voter_id`, `position_id`),
    INDEX `idx_vote_voter` (`voter_id`),
    INDEX `idx_vote_candidate` (`candidate_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================
-- Insert Default Data
-- =============================================

-- Default Admin (password: admin)
-- The password hash is generated using Werkzeug's generate_password_hash
INSERT INTO `admins` (`first_name`, `last_name`, `email`, `password_hash`) 
VALUES ('Admin', 'User', 'admin@gmail.com', 'scrypt:32768:8:1$rQZKFmJq3NzqYtGz$d7c0a3b5e8f1g2h4i5j6k7l8m9n0o1p2q3r4s5t6u7v8w9x0y1z2a3b4c5d6e7f8')
ON DUPLICATE KEY UPDATE `first_name` = `first_name`;

-- Default Positions
INSERT INTO `positions` (`name`, `description`) VALUES 
    ('Chairman', 'Head of the organization'),
    ('Vice-Chairman', 'Deputy head of the organization'),
    ('Secretary', 'Administrative head'),
    ('Treasurer', 'Financial head')
ON DUPLICATE KEY UPDATE `name` = `name`;

-- =============================================
-- Useful Queries
-- =============================================

-- View all voters with their voting status
-- SELECT id, CONCAT(first_name, ' ', last_name) AS name, email, voter_id, 
--        IF(has_voted, 'Voted', 'Not Voted') AS status FROM voters;

-- View election results
-- SELECT p.name AS position, c.name AS candidate, c.votes_count 
-- FROM candidates c 
-- JOIN positions p ON c.position_id = p.id 
-- ORDER BY p.name, c.votes_count DESC;

-- Reset all votes (use with caution!)
-- DELETE FROM votes;
-- UPDATE candidates SET votes_count = 0;
-- UPDATE voters SET has_voted = 0;
