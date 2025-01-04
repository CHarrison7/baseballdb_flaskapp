from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import User, Team, FavoriteTeams
from app import db
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username already exists.')

    def validate_email(self, email):
        user_email = User.query.filter_by(email=email.data).first()
        if user_email:
            raise ValidationError('That email already exists.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class SearchForm(FlaskForm):
	playerID = StringField('Player', validators=[DataRequired()])
	# password = PasswordField('Password', validators=[DataRequired()])
	# yearid = StringField('Year', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Search')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Save Changes')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username already exists.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user_email = User.query.filter_by(email=email.data).first()
            if user_email:
                raise ValidationError('That email already exists.')


class UpdateFavoriteForm(FlaskForm):
    choices = db.session.query(FavoriteTeams).order_by(FavoriteTeams.franchName, FavoriteTeams.startYear).distinct(FavoriteTeams.franchName)
    choicesList = []
    for row in choices:
        choicesListObject = row.franchName + '  (Years: ' + str(row.startYear) + ' - ' + str(row.endYear) + ')'
        choicesList.append(choicesListObject)
    favorite_team = SelectField(u'Favorite Franchise', validators=[DataRequired()], choices=choicesList)
    submit = SubmitField('Save Changes')


#class UpdateFavoriteYear(FlaskForm):
#    yearsList = []
#    usersTeam = current_user.favorite_team
#    getUsersTeam = db.session.query(FavoriteTeams).filter_by(teamID = usersTeam).all()
#    for row in getUsersTeam:
#        startX = row.startYear
#        endX = row.endYear
#    #startX = int(getUsersTeam.startYear)
#    #endX = int(getUsersTeam.endYear) + 1
#    for x in range(startX, endX + 1 ):
#        yearsList += x
#    favorite_year = SelectField(u'Favorite Team Year', validators=[DataRequired()], choices=yearsList)
#    submit = SubmitField('Save Changes')


class TeamSearchForm(FlaskForm):
    choices = db.session.query(FavoriteTeams).order_by(FavoriteTeams.franchName, FavoriteTeams.startYear).distinct(FavoriteTeams.franchName)
    choicesList = []
    for row in choices:
        choicesListObject = row.franchName + '  (Years: ' + str(row.startYear) + ' - ' + str(row.endYear) + ')'
        choicesList.append(choicesListObject)
    team = SelectField(u'Pick a team', validators=[DataRequired()], choices=choicesList)
    submit = SubmitField('Search')


#class YearForm(FlaskForm):
#    yearList = []
#    years = db.session.query(FavoriteTeams).filter_by(teamID = team).all()
#    yearStart = 0
#    yearEnd = 0
#    for row in years:
#        yearStart = int(row.startYear)
#        yearEnd = int(row.endYear)
#    yearList = list(range(yearStart, yearEnd))
#    year = SelectField(u'Pick a year', validators=[DataRequired()], choices=yearList)
#    submit = SubmitField("Search")