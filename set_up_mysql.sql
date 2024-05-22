CREATE DATABASE IF NOT EXISTS siteswift_dev_db;
CREATE USER IF NOT EXISTS 'siteswift_dev'@'localhost' IDENTIFIED BY 'Siteswift_dev_2001';
GRANT ALL PRIVILEGES ON `siteswift_dev_db`.* TO 'siteswift_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'siteswift_dev'@'localhost';
FLUSH PRIVILEGES;
