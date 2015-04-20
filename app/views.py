from app import app, db
from flask import render_template, request, redirect, url_for
from app.models import Genre, Game
from app.forms import GameForm


#################################################
#                  Main Routes                  #
#################################################
@app.route('/')
def home():
    genres = db.session.query(Genre).all()
    recentgames = db.session.query(Game).order_by(Game.id.desc()).limit(5)
    return render_template('index.html', genres=genres, recent=recentgames)


@app.route('/games/<genre_id>/')
def genre(genre_id):
    genre = db.session.query(Genre).filter_by(id=genre_id).one()
    games = db.session.query(Game).filter_by(genre_id=genre_id).all()
    return render_template('genre.html', genre=genre, games=games)


@app.route('/game/<int:game_id>/')
def game(game_id):
    game = db.session.query(Game).filter_by(id=game_id).one()
    return render_template('game.html', game=game)


@app.route('/game/new/', methods=['POST', 'GET'])
@app.route('/games/<genre_id>/new/')
def addGame(genre_id=None):
    form = GameForm()
    form.genre.choices = [(g.id, g.name)
                          for g in db.session.query(Genre).all()]
    form.genre.choices.insert(0, ('', 'Select...'))
    # if genre_id in url set it as genre dropdown's default
    if genre_id is not None:
        form.genre.default = genre_id
        form.process()

    if form.validate_on_submit():
        user = 1
        title = form.title.data
        genre = form.genre.data
        description = form.description.data
        newGame = Game(
            user_id=user, title=title, genre_id=genre, description=description)
        db.session.add(newGame)
        db.session.commit()
        return redirect(url_for('game', game_id=newGame.id))

    return render_template('addGame.html', genre_id=genre_id, form=form)


@app.route('/game/<int:game_id>/edit/', methods=['POST', 'GET'])
def editGame(game_id):
    game = db.session.query(Game).filter_by(id=game_id).one()
    form = GameForm()

    # Fill genre select dropdown with choices from Genre table
    form.genre.choices = [(g.id, g.name)
                          for g in db.session.query(Genre).all()]
    form.genre.choices.insert(0, ('', 'Select...'))

    # If form validates and method='POST'
    if form.validate_on_submit():
        game.title = form.title.data
        game.genre_id = form.genre.data
        game.description = form.description.data
        db.session.add(game)
        db.session.commit()
        return redirect(url_for('game', game_id=game.id))

    # Set defaults in form as current values
    form.genre.default = game.genre_id
    form.title.default = game.title
    form.description.default = game.description
    form.process()

    print form.errors
    return render_template('editGame.html', game=game, form=form)


@app.route('/game/<int:game_id>/delete/', methods=['POST', 'GET'])
def deleteGame(game_id):
    game = db.session.query(Game).filter_by(id=game_id).one()
    if request.method == 'POST':
        db.session.delete(game)
        db.session.commit()

    return render_template('deleteGame.html', game=game)


#################################################
#                  JSON Routes                  #
#################################################
