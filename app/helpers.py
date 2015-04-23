from app import app, db
from app.models import User
import os, time
#################################################
#             Helper Functions                  #
#################################################
# Return user object by its ID
def getUserInfo(user_id):
    user = db.session.query(User).filter_by(id=user_id).one()
    return user

# Get a user's ID from email address
def getUserID(email):
    try:
        user = db.session.query(User).filter_by(email=email).one()
        return user.id 
    except:
        return None

# Create user in DB and return its ID
def createUser(login_session):
    newUser = User(login_session['username'], login_session['email'], login_session['picture'])
    db.session.add(newUser)
    db.session.commit()
    return newUser.id

# Returns true if filename has a period and extensions are allowed
def validateFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


# Function for uploading an image for game
def uploadGameImage(file, game):
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