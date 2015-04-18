from app import app, db
from flask import render_template
from app.models import Genre, Game


@app.route('/')
def home():
    genres = db.session.query(Genre).all()
    recentgames = db.session.query(Game).order_by(Game.id.desc()).limit(5)

    return render_template('index.html', genres=genres, recent=recentgames) 


@app.route('/<genre_id>/')
def viewGenre(genre_id):
    genre = db.session.query(Genre).filter_by(id=genre_id).one()
    games = db.session.query(Game).filter_by(genre_id=genre_id).all()
    output = ''
    output += 'Genre: %s </br>' % genre.name
    for game in games:
        output += game.name + '</br>'
    return output
