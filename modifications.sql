-- Modifications.sql

/* Create "main" user for web app: web@localhost (as we did in Week 7) with ALL permission */
CREATE USER IF NOT EXISTS web@localhost IDENTIFIED BY 'dbrules';
GRANT ALL ON baseball TO web@localhost;


/*
****************************************
* CREATE "analysis" TABLE + STRUCTURE  *
****************************************
*/

DROP TABLE IF EXISTS `analysis`;
SET character_set_client = utf8mb4;
CREATE TABLE `analysis` (
  `analysis_ID` int(11) NOT NULL AUTO_INCREMENT,
  `playerID` varchar(9) NOT NULL,
  `yearID` smallint(6) NOT NULL,
  `G` smallint(6) DEFAULT NULL,
  `AB` smallint(6) DEFAULT NULL,
  `R` smallint(6) DEFAULT NULL,
  `H` smallint(6) DEFAULT NULL,
  `2B` smallint(6) DEFAULT NULL,
  `3B` smallint(6) DEFAULT NULL,
  `HR` smallint(6) DEFAULT NULL,
  `RBI` smallint(6) DEFAULT NULL,
  `SB` smallint(6) DEFAULT NULL,
  `CS` smallint(6) DEFAULT NULL,
  `BB` smallint(6) DEFAULT NULL,
  `SO` smallint(6) DEFAULT NULL,
  `IBB` smallint(6) DEFAULT NULL,
  `HBP` smallint(6) DEFAULT NULL,
  `SH` smallint(6) DEFAULT NULL,
  `SF` smallint(6) DEFAULT NULL,
  `GIDP` smallint(6) DEFAULT NULL,
  `OBP` numeric(5,3) DEFAULT NULL,
  `TB` smallint(6) DEFAULT NULL,
  `RC` numeric(5,1) DEFAULT NULL,
  `RC27` numeric(5,2) DEFAULT NULL,
  PRIMARY KEY (`analysis_ID`),
  UNIQUE KEY `analysisID` (`playerID`,`yearID`),
  CONSTRAINT `analysis_peoplefk` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


/*
***********************************************************************************
* Consolidate batting stats per year per player and insert into analysis table    *
******************************************************ß****************************
*/

INSERT INTO analysis(playerid,yearid,g,ab,r,h,2b,3b,hr,rbi,sb,
cs,bb,so,ibb,hbp,sh,sf,gidp)
SELECT playerid,yearid, SUM(g),SUM(ab),SUM(r),SUM(h),SUM(2b),
SUM(3b),SUM(hr),SUM(rbi),SUM(sb), SUM(cs),SUM( bb),SUM(so),
SUM(ibb),SUM(hbp),SUM(sh),SUM(sf),SUM(gidp)
FROM batting GROUP BY playerid,yearid;





/*
**************************************************************
* CREATE TRIGGER create_analysis to maintain analysis table  *
*****************************************************ß*********
*/

DELIMITER //

CREATE OR REPLACE TRIGGER create_analysis
AFTER INSERT ON batting
FOR EACH ROW
BEGIN
IF (SELECT COUNT(*) FROM analysis WHERE playerid = NEW.playerid AND yearid = NEW.yearid) = 0 THEN
	INSERT INTO analysis(playerid,yearid,g,ab,r,h,2b,3b,hr,rbi,sb,cs,bb,so,ibb, hbp,sh,sf,gidp)
	VALUES(NEW.playerid,NEW.yearid,NEW.g,NEW.ab,NEW.r,NEW.h,NEW.2b,NEW.3b,NEW.hr,NEW.rbi,NEW.sb,NEW.cs,NEW. bb,NEW.so,NEW.ibb,NEW.hbp,NEW.sh,NEW.sf,NEW.gidp);
ELSE
	UPDATE analysis SET
		g=g+NEW.g,
		ab=ab+NEW.ab,
		h=h+NEW.h,
		2b=2b+NEW.2b,
		3b=3b+NEW.3b,
		hr=hr+NEW.hr,
		rbi=rbi+NEW.rbi,
		sb=sb+NEW.sb,
		cs=cs+NEW.cs,
		bb=bb+NEW.bb,
		so=so+NEW.so,
		ibb=ibb+NEW.ibb,
		hbp=hbp+NEW.hbp,
		sh=sh+NEW.sh,
		sf=sf+NEW.sf,
		r=r+NEW.r,
		gidp=gidp+NEW.gidp
	WHERE playerid = NEW.playerid AND yearid = NEW.yearid;
END IF;
END;
//

DELIMITER ;




/*
*********************************
* CREATE USER TABLE IN DATABASE *
*********************************
*/

CREATE TABLE users (
  id int(5) NOT NULL AUTO_INCREMENT,
  username varchar(20) NOT NULL UNIQUE,
  email varchar(120) NOT NULL UNIQUE,
  image_file varchar(20) NOT NULL DEFAULT 'default.jpg',
  password varchar(60) NOT NULL,
  favorite_team char(3) DEFAULT NULL,
  favorite_team_year smallint(6) DEFAULT NULL,
  PRIMARY KEY (id)
);




/*
*************************************************************************************
* CREATE TABLE IN DATABASE TO MAKE IT EASIER TO CREATE FORM TO SELECT FAVORITE TEAM *
*************************************************************************************
*/

CREATE TABLE FavoriteTeams (
  id int(11) NOT NULL AUTO_INCREMENT,
  teamID char(3) NOT NULL,
  franchName varchar(100) NOT NULL,
  franchID varchar(3) NOT NULL,
  startYear smallint(6) NOT NULL,
  endYear smallint(6) NOT NULL,
  PRIMARY KEY (id)
);



/*
*************************************************************************************
* POPULATE FavoriteTeams TABLE WITH DATA FROM TEAMS TABLE                           *
*************************************************************************************
*/

INSERT INTO FavoriteTeams (teamID, franchID, franchName, startYear, endYear)
select distinct t.teamid, t.franchID, tf.franchName, min(yearID), max(yearID) from teamsfranchises tf JOIN teams t USING (franchID) group by teamid;
