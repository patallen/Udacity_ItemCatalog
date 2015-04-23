from app import app, db
from app.models import User
import os
#################################################
#             Helper Functions                  #
#################################################
def getUserInfo(user_id):
    user = db.session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = db.session.query(User).filter_by(email=email).one()
        return user.id 
    except:
        return None


def createUser(login_session):
    newUser = User(login_session['username'], login_session['email'], login_session['picture'])
    db.session.add(newUser)
    db.session.commit()
    return newUser.id


def validateFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def uploadImage(file, game):
    if validateFile(file.filename):
        ext = '.' + file.filename.rsplit(".", 1)[1]
        name = 'game%simg' % str(game.id)
        filename = name + ext
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        game.picture = filename
        db.session.add(game)
        db.session.commit()