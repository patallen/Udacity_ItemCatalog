from app import app, db
from flask import render_template, request, redirect, url_for, jsonify, make_response
from app.models import Genre, Game
from app.forms import GameForm, DeleteForm

from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2, json, random, string, requests
from flask import session as login_session

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME="Game Catalog"


#################################################
#                  Main Routes                  #
#################################################
@app.route('/')
def home():
    genres = db.session.query(Genre).all()
    recentgames = db.session.query(Game).order_by(Game.id.desc()).limit(10)
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
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(game)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('deleteGame.html', game=game, form=form)


#################################################
#                  JSON Routes                  #
#################################################
@app.route('/games/<genre_id>/JSON/')
def genreJSON(genre_id):
    games = db.session.query(Game).filter_by(genre_id=genre_id).all()
    return jsonify(Games=[g.serialize for g in games])


@app.route('/game/<int:game_id>/JSON/')
def gameJSON(game_id):
    game = db.session.query(Game).filter_by(id=game_id).one()
    return jsonify(Game=[game.serialize])


#################################################
#               Routes for OAuth                #
#################################################
@app.route('/login/')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # if state is not correct, return 'invalid state' response
    if login_session['state'] != request.args.get('state'):
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if the user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connectd.'), 200)
        response.headers['Content-Type'] = 'application.json'

    # Store the access token in the session for later use
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt':'json'}

    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['username'] = data["name"]
    login_session['picture'] = data["picture"]
    login_session['email'] = data["email"]

    return "Welcome %s, redirecting..." % login_session['username']


@app.route('/gdisconnect/')
def gdisconnect():
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response('Current user not connected.', 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return reponse