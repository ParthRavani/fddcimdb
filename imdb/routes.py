from flask import render_template, url_for, flash, redirect, request, jsonify, json
from imdb import app, db, bcrypt
from imdb.forms import RegistrationForm, LoginForm, SearchForm
from imdb.models import User, Movie
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/search", methods=['GET', 'POST'])
def search():

    #keyword = request.args.get('keyword')
    #keyword = request.get_data()
    keyword = request.get_json()['keyword']
    if keyword:
        movies = Movie.query.filter((Movie.name.like('%' + keyword + '%'))
                                | (Movie.production.like('%' + keyword + '%'))
                                | (Movie.genre.like('%' + keyword + '%'))
                                | (Movie.year.like('%' + keyword + '%')))
    else:
        movies = Movie.query.all()

    output = []
    for movie in movies:
        data={}
        data['name'] = movie.name
        data['production'] = movie.production
        data['genre'] = movie.genre
        data['popularity'] = movie.popularity
        data['year'] = movie.year
        output.append(data)

    return jsonify({'movies': output})
    # form = SearchForm()
    # return render_template('home.html', movies=movies, form=form)


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    #if form.validate_on_submit():
    if form.keyword.data:
        movies = Movie.query.filter((Movie.name.like('%'+form.keyword.data+'%'))
                                    | (Movie.production.like('%' + form.keyword.data + '%'))
                                    | (Movie.genre.like('%' + form.keyword.data + '%'))
                                    | (Movie.year.like('%'+form.keyword.data+'%')))
    else:
        movies = Movie.query.all()
    return render_template('home.html', movies=movies, form=form)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


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
        flash('Your account has been created! You are now able to log in', 'success')
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


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
