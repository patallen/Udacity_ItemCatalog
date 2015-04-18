from app import app, db
from flask import render_template
from app.models import Genre, Game


#################################################
#                  Main Routes                  #
#################################################
@app.route('/')
@app.route('/home/')
def home():
    genres = db.session.query(Genre).all()
    recentgames = db.session.query(Game).order_by(Game.id.desc()).limit(5)
    return render_template('index.html', genres=genres, recent=recentgames)


@app.route('/<genre_id>/')
def viewGenre(genre_id):
    genre = db.session.query(Genre).filter_by(id=genre_id).one()
    games = db.session.query(Game).filter_by(genre_id=genre_id).all()
    return render_template('genre.html', genre=genre, games=games)


@app.route('/game/<int:game_id>/')
def game(genre_id, game_id):
    genre = db.session.query(Genre).filter_by(id=genre_id).one()
    game = db.session.query(Game).filter_by(id=game_id).all()
    return render_template('game.html', genre=genre, game=game)

@app.route('/game/new/')
@app.route('/game/<genre_id>/new/')
def addGame(genre_id=None):
    genres = db.session.query(Genre).all()
    return render_template('addGame.html', genre_id=genre_id, genres=genres)


@app.route('/game/<int:game_id>/delete/')
def deleteGame(genre_id, game_id):
    genre = db.session.query(Genre).filter_by(id=genre_id).one()
    game = db.session.query(Game).filter_by(id=game_id)
    return render_template('deleteGame.html', genre=genre, game=game)


#################################################
#                  JSON Routes                  #
#################################################
