from app import db


class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(500))
    picture = db.Column(db.String(250))

    def __init__(self, name, picture=None):
        if picture is None:
            self.picture = ''
        else:
            self.picture = picture
        self.name = name
        self.id = name.lower()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    picture = db.Column(db.String(250))

    def __init__(self, name, email, picture=None):
        self.name = name
        self.email = email
        if picture is None:
            self.picture = ''
        else:
            self.picture = picture


class Game(db.Model):
    __tablename__ = 'game'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    picture = db.Column(db.String(250), default='default.jpg')

    genre_id = db.Column(db.String(64), db.ForeignKey('genre.id'))
    genre = db.relationship(Genre)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'description' : self.description,
            'picture' : self.picture,
            'genre_id' : self.genre_id,
            'user_id' : self.user_id
        }
    
