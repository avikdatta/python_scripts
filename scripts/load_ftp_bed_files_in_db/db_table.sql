create table `bed_files`(
  `experiment_id` varchar(10) PRIMARY KEY,
  `filename` varchar(255) NOT NULL,
  `log_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
