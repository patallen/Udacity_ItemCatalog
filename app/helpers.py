from app import app, db
from flask import session as login_session
from app.models import User
from flask import redirect, url_for
import os, time
from functools import wraps
#################################################
#             Helper Functions                  #
#################################################
def getUserInfo(user_id):
    '''Return user object by its ID'''
    user = db.session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    '''Get a user's ID from email address'''
    try:
        user = db.session.query(User).filter_by(email=email).one()
        return user.id 
    except:
        return None


def createUser(login_session):
    '''Create user in DB and return its ID'''
    newUser = User(login_session['username'], login_session['email'], login_session['picture'])
    db.session.add(newUser)
    db.session.commit()
    return newUser.id


def validateFile(filename):
    '''Returns true if filename has a period and extensions are allowed'''
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def uploadGameImage(file, game):
    '''Function for uploading an image for game'''
    if validateFile(file.filename):
        currentFile = game.picture

        ext = '.' + file.filename.rsplit(".", 1)[1]
        name = '%s-%s' % (str(game.id), str(int(time.time())))
        filename = name + ext

        # Save file and update game.picture in DB
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        game.picture = filename
        db.session.add(game)
        db.session.commit()

        # Delete previous file
        if currentFile != 'default.jpg':
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], currentFile))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kawrgs):
        if 'credentials' not in login_session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
