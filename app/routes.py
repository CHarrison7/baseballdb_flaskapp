import secrets
import os
import re
from flask import render_template, flash, redirect, url_for, request
from app import app, db, bcrypt
from app.forms import SearchForm, RegistrationForm, LoginForm, UpdateAccountForm, UpdateFavoriteForm, TeamSearchForm
from app.models import Analysis, Player, User, Team, FavoriteTeams, Teamsfranchise, Batting
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import text




@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        if current_user.favorite_team:
            team = db.session.query(Team).filter_by(teamID = current_user.favorite_team, yearID = current_user.favorite_team_year).all()
            for row in team:
                franchID = row.franchID
                yearID = row.yearID
            teamPlayers = db.session.query(Player).join(Batting).filter_by(yearID = current_user.favorite_team_year, teamID =  current_user.favorite_team).all()
            battingPlayers = db.session.query(Batting).filter_by(yearID = current_user.favorite_team_year, teamID = current_user.favorite_team).all()
            teamfranchise = db.session.query(Teamsfranchise).filter_by(franchID = franchID)
            return render_template('home.html', team=team, teamfranchise=teamfranchise, battingPlayers=battingPlayers, year = yearID, players=teamPlayers)
    return render_template('home.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/search', methods=['GET','POST'])
def search():
	form = SearchForm()
	if form.validate_on_submit():
		stats = Analysis.query.filter_by(playerID=form.playerID.data).all()
		for row in stats:
			if row.RC27 is None:
				row.setRC27()
		return render_template('search.html',title='Results',form=form, stats=stats)
	return render_template('search.html',title='Search',form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_filename)
    form_picture.save(picture_path)
    return picture_filename



@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account info has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',title='Account', image_file=image_file, form=form)


@app.route("/updatefavorite", methods=['GET','POST'])
@login_required
def updatefavorite():
    form = UpdateFavoriteForm()
    if form.validate_on_submit():
        current_user.favorite_franchise = form.favorite_team.data
        parsedString = form.favorite_team.data.split()
        pattern = re.compile("Years:")
        found = False
        franchise_name = ""
        for item in parsedString:
            if found:
                favorite_team_start_year = item
            if pattern.search(item):
                found = True
            else:
                if (found == False):
                    franchise_name += ' ' + item
        franchise_name = franchise_name[1:]
        results = db.session.query(FavoriteTeams).filter_by(franchName = franchise_name).all()
        result_teamid = ""
        for row in results:
            result_teamid = row.teamID
            result_endYear = row.endYear
        current_user.favorite_team = result_teamid
        current_user.favorite_team_year = result_endYear
        db.session.commit()
        flash('Favorite team info has been updated!', 'success')
        return redirect(url_for('account'))

    return render_template('updatefavorite.html',title='Favorite Team', form=form)


#@app.route("/updatefavoriteyear", methods=['GET','POST'])
#@login_required
#def updatefavorite():
#    form = UpdateFavoriteYearForm()
#    if form.validate_on_submit():
#        current_user.favorite_team_year = form.favorite_year.data
#        db.session.commit()
#        flash('Favorite team info has been updated!', 'success')
#        return redirect(url_for('account'))
#
#    return render_template('updateyear.html',title='Favorite Team Year', form=form)
#



@app.route("/teamsearch", methods=['GET','POST'])
@login_required
def teamsearch():
    form = TeamSearchForm()
    if form.validate_on_submit():
        parsedString = form.team.data.split()
        pattern = re.compile("Years:")
        found = False
        franchise_name = ""
        for item in parsedString:
            if found:
                team_start_year = item
            if pattern.search(item):
                found = True
            else:
                if (found == False):
                    franchise_name += ' ' + item
        franchise_name = franchise_name[1:]
        results = db.session.query(FavoriteTeams).filter_by(franchName = franchise_name).all()
        result_teamid = ""
        for row in results:
            result_teamid = row.teamID
            result_endYear = row.endYear
            result_startYear = row.startYear
            
        teamInfo = Team.query.filter_by(teamID = result_teamid, yearID = result_endYear).all()
#        yearForm = YearForm(result_teamid)
#        if yearForm.validate_on_submit():
#            yearInfo = yearForm.year.data  
#            teamInfo = Team.query.filter_by(teamID = result_teamid, yearID = yearInfo).all()
#            return render_template('teamsearch.html',title='Results',form=form, teamInfo=teamInfo, yearForm = yearForm)
#        else:
        return render_template('teamsearch.html',title='Results',form=form, teamInfo = teamInfo)
    return render_template('teamsearch.html',title='Team Search',form=form)


