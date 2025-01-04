from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Analysis(db.Model):
	__tablename__ = "analysis" # required

	analysis_ID = db.Column(db.Integer,primary_key=True) # required
	playerID = db.Column(db.String(9))
	yearID = db.Column(db.Integer)
	G = db.Column(db.Integer)
	AB = db.Column(db.Integer)
	R = db.Column(db.Integer)
	H = db.Column(db.Integer)
	B2 = db.Column('2B', db.Integer)
	B3 = db.Column('3B', db.Integer)
	HR = db.Column(db.Integer)
	RBI = db.Column(db.Integer)
	SB = db.Column(db.Integer)
	CS = db.Column(db.Integer)
	BB = db.Column(db.Integer)
	SO = db.Column(db.Integer)
	IBB = db.Column(db.Integer)
	HBP = db.Column(db.Integer)
	SH = db.Column(db.Integer)
	SF = db.Column(db.Integer)
	GIDP = db.Column(db.Integer)
	OBP = db.Column(db.Numeric) 
	TB = db.Column(db.Integer)
	RC = db.Column(db.Numeric)
	RC27 = db.Column(db.Numeric) 

	def __repr__(self):
		return "<analysis(player='%s',RC27='%s')>" % (self.playerID,self.RC27)

	def setRC27(self):
		if self.RC is None:
			self.setRC()	
		outs=self.AB-self.H+self.coalesce(self.CS)+self.coalesce(self.SH)+self.coalesce(self.SF)+self.coalesce(self.GIDP)
		self.RC27 = 27 * self.RC/outs
		db.session.commit()

	def setRC(self):
		if self.OBP is None:
			self.setOBP()
		if self.TB is None:
			self.setTB()
		self.RC = self.OBP * self.TB

	def setOBP(self):
		onbase = self.H+self.BB+self.coalesce(self.HBP)
		pa = self.AB+self.BB+self.coalesce(self.HBP)+self.coalesce(self.SF)
		if pa == 0:
			self.OBP = 0
		else:
			self.OBP = onbase/pa

	def setTB(self):
		self.TB = self.H+self.B2+2*self.B3+3*self.HR

	def coalesce(self,x):
		if x is None:
			return 0
		else:
			return x



class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    favorite_team = db.Column(db.CHAR(3), nullable=True)
    favorite_team_year = db.Column(db.SMALLINT, nullable=True)
    favorite_franchise = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.favorite_team}', '{self.image_file}')"




class Player(db.Model):
    __tablename__ = 'people'

    playerID = db.Column(db.String(9), primary_key=True)
    birthYear = db.Column(db.Integer)
    birthMonth = db.Column(db.Integer)
    birthDay = db.Column(db.Integer)
    birthCountry = db.Column(db.String(255))
    birthState = db.Column(db.String(255))
    birthCity = db.Column(db.String(255))
    deathYear = db.Column(db.Integer)
    deathMonth = db.Column(db.Integer)
    deathDay = db.Column(db.Integer)
    deathCountry = db.Column(db.String(255))
    deathState = db.Column(db.String(255))
    deathCity = db.Column(db.String(255))
    nameFirst = db.Column(db.String(255))
    nameLast = db.Column(db.String(255))
    nameGiven = db.Column(db.String(255))
    weight = db.Column(db.Integer)
    height = db.Column(db.Integer)
    bats = db.Column(db.String(255))
    throws = db.Column(db.String(255))
    debut = db.Column(db.String(255))
    finalGame = db.Column(db.String(255))
    retroID = db.Column(db.String(255))
    bbrefID = db.Column(db.String(255))
    birth_date = db.Column(db.Date)
    debut_date = db.Column(db.Date)
    finalgame_date = db.Column(db.Date)
    death_date = db.Column(db.Date)

    battingStints = db.relationship('Batting', backref = 'stintPlayer')

    def __repr__(self):
        return "<Player(playerid='%s',LastName='%s')>" % (self.playerID, self.nameLast)


class League(db.Model):
    __tablename__ = 'leagues'

    lgID = db.Column(db.CHAR(2), primary_key=True)
    league = db.Column(db.String(50), nullable=False)
    active = db.Column(db.CHAR(1), nullable=False)

    def __repr__(self):
        return "<League(lgID='%s',LeagueName='%s', active='%s')>" % (self.lgID, self.league, self.active)


class Division(db.Model):
    __tablename__ = 'divisions'
    ID = db.Column(db.Integer, primary_key=True)
    divID = db.Column(db.CHAR(2), nullable=False)
    lgID = db.Column(db.CHAR(2), db.ForeignKey('leagues.lgID'))
    division = db.Column(db.String(50), nullable=False)
    active = db.Column(db.CHAR(1), nullable=False)

    league = db.relationship('League')


class Teamsfranchise(db.Model):
    __tablename__ = 'teamsfranchises'

    franchID = db.Column(db.String(3), primary_key=True)
    franchName = db.Column(db.String(50))
    active = db.Column(db.CHAR(1))
    NAassoc = db.Column(db.String(3))



class Team(db.Model):
    __tablename__ = 'teams'

    ID = db.Column(db.Integer, primary_key=True)
    yearID = db.Column(db.SMALLINT, nullable=False)
    lgID = db.Column(db.ForeignKey('leagues.lgID'))
    teamID = db.Column(db.CHAR(3), nullable=False)
    franchID = db.Column(db.ForeignKey('teamsfranchises.franchID'))
    divID = db.Column(db.CHAR(1))
    div_ID = db.Column(db.ForeignKey('divisions.ID'))
    teamRank = db.Column(db.SMALLINT)
    G = db.Column(db.SMALLINT)
    Ghome = db.Column(db.SMALLINT)
    W = db.Column(db.SMALLINT)
    L = db.Column(db.SMALLINT)
    DivWin = db.Column(db.String(1))
    WCWin = db.Column(db.String(1))
    LgWin = db.Column(db.String(1))
    WSWin = db.Column(db.String(1))
    R = db.Column(db.SMALLINT)
    AB = db.Column(db.SMALLINT)
    H = db.Column(db.SMALLINT)
    B2 = db.Column('2B', db.SMALLINT)
    B3 = db.Column('3B', db.SMALLINT)
    HR = db.Column(db.SMALLINT)
    BB = db.Column(db.SMALLINT)
    SO = db.Column(db.SMALLINT)
    SB = db.Column(db.SMALLINT)
    CS = db.Column(db.SMALLINT)
    HBP = db.Column(db.SMALLINT)
    SF = db.Column(db.SMALLINT)
    RA = db.Column(db.SMALLINT)
    ER = db.Column(db.SMALLINT)
    ERA = db.Column(db.Float(asdecimal=True))
    CG = db.Column(db.SMALLINT)
    SHO = db.Column(db.SMALLINT)
    SV = db.Column(db.SMALLINT)
    IPouts = db.Column(db.Integer)
    HA = db.Column(db.SMALLINT)
    HRA = db.Column(db.SMALLINT)
    BBA = db.Column(db.SMALLINT)
    SOA = db.Column(db.SMALLINT)
    E = db.Column(db.Integer)
    DP = db.Column(db.Integer)
    FP = db.Column(db.Float(asdecimal=True))
    name = db.Column(db.String(50))
    park = db.Column(db.String(255))
    attendance = db.Column(db.Integer)
    BPF = db.Column(db.Integer)
    PPF = db.Column(db.Integer)
    teamIDBR = db.Column(db.String(3))
    teamIDlahman45 = db.Column(db.String(3))
    teamIDretro = db.Column(db.String(3))

    division = db.relationship('Division')
    teamsfranchise = db.relationship('Teamsfranchise')
    league = db.relationship('League')


class FavoriteTeams(db.Model):
    __tablename__ = 'FavoriteTeams'

    id = db.Column(db.Integer, primary_key=True)
    teamID = db.Column(db.CHAR(3), nullable=False)
    franchName = db.Column(db.String(100), nullable=False)
    franchID = db.Column(db.String(3), nullable=False)
    startYear = db.Column(db.SMALLINT, nullable=False)
    endYear = db.Column(db.SMALLINT, nullable=False)



class Batting(db.Model):
    __tablename__ = 'batting'

    ID = db.Column(db.Integer, primary_key=True)
    playerID = db.Column(db.ForeignKey('people.playerID'), nullable=False)
    yearID = db.Column(db.SMALLINT, nullable=False)
    stint = db.Column(db.SMALLINT, nullable=False)
    teamID = db.Column(db.CHAR(3))
    team_ID = db.Column(db.ForeignKey('teams.ID'))
    lgID = db.Column(db.ForeignKey('leagues.lgID'))
    G = db.Column(db.SMALLINT)
    G_batting = db.Column(db.SMALLINT)
    AB = db.Column(db.SMALLINT)
    R = db.Column(db.SMALLINT)
    H = db.Column(db.SMALLINT)
    B2 = db.Column('2B', db.SMALLINT)
    B3 = db.Column('3B', db.SMALLINT)
    HR = db.Column(db.SMALLINT)
    RBI = db.Column(db.SMALLINT)
    SB = db.Column(db.SMALLINT)
    CS = db.Column(db.SMALLINT)
    BB = db.Column(db.SMALLINT)
    SO = db.Column(db.SMALLINT)
    IBB = db.Column(db.SMALLINT)
    HBP = db.Column(db.SMALLINT)
    SH = db.Column(db.SMALLINT)
    SF = db.Column(db.SMALLINT)
    GIDP = db.Column(db.SMALLINT)

    team = db.relationship('Team')
    player = db.relationship('Player')