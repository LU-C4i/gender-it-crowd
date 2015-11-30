CREATE TABLE `t_tus_twitteruser` (
  `tus_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `tus_twitter_user_id` bigint(20) NOT NULL,
  `tus_screenname` varchar(255) DEFAULT NULL,
  `tus_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `tus_description` text,
  `tus_picture_url` varchar(255) DEFAULT NULL,
  `tus_last_tweet` text,
  PRIMARY KEY (`tus_id`),
  UNIQUE KEY `tus_twitterid_UNIQUE` (`tus_twitter_user_id`),
  KEY `tus_screenname` (`tus_screenname`),
  KEY `tus_name` (`tus_name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE `t_usr_user` (
  `usr_id` int(11) NOT NULL AUTO_INCREMENT,
  `usr_login` varchar(45) DEFAULT NULL,
  `usr_password` char(60) DEFAULT NULL,
  PRIMARY KEY (`usr_id`),
  UNIQUE KEY `usr_login_UNIQUE` (`usr_login`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE `t_cpr_crowdprediction` (
  `cpr_id` int(11) NOT NULL AUTO_INCREMENT,
  `cpr_usr_id` int(11) NOT NULL,
  `cpr_tus_id` bigint(20) NOT NULL,
  `cpr_prediction` varchar(45) DEFAULT NULL,
  `cpr_created` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`cpr_id`),
  KEY `cpr_usr_id_and_tus_id` (`cpr_usr_id`,`cpr_tus_id`),
  KEY `cpr_usr_id` (`cpr_usr_id`),
  KEY `cpr_tus_id` (`cpr_tus_id`),
  KEY `cpr_prediction` (`cpr_prediction`)
) ENGINE=InnoDB AUTO_INCREMENT=13669 DEFAULT CHARSET=latin1;

CREATE TABLE `t_cpf_crowdprediction_final` (
  `cpf_id` int(11) NOT NULL AUTO_INCREMENT,
  `cpf_tus_id` bigint(20) NOT NULL,
  `cpf_prediction_final` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`cpf_id`),
  KEY `cpf_tus_id` (`cpf_tus_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2533 DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `p_crowdprediction_user_stats`()
BEGIN
	SELECT usr_login, COUNT(*)
	FROM t_cpr_crowdprediction
	INNER JOIN t_usr_user ON cpr_usr_id = usr_id
	WHERE cpr_prediction <> 'skipped'
	GROUP BY usr_login
    ORDER BY COUNT(*) DESC;
END$$
DELIMITER ;


DELIMITER $$
CREATE DEFINER=`ungp_db`@`%` PROCEDURE `p_cpf_crowdprediction_final_refresh`()
BEGIN
    truncate t_cpf_crowdprediction_final;
    insert into t_cpf_crowdprediction_final (cpf_tus_id, cpf_prediction_final)
    select cpr_tus_id, cpr_prediction from t_cpr_crowdprediction
    where  cpr_prediction <> 'skipped'
    group by cpr_tus_id, cpr_prediction
    having count(*) > 2;
END$$
DELIMITER ;


