from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() #db es una "instancia" de SQLAlchemy 


class User (db.Model): #Model es una clase de db que a su vez es una instancia de SQLAlchemy
    id = db.Column (db.Integer, primary_key=True) #id automáticamente incremental
    user_email = db.Column (db.String(25), unique=True, nullable=False) #unique implica campo único, no pueden haber dos iguales y nullable=False implica que es obligatorio.
    user_password = db.Column(db.String(50), nullable=False) #no se usa unique porque pueden haber dos contraseñas iguales
    favorites = db.relationship('Favorites', lazy=True, uselist=False)
    def __repr__(self):
        return "<User %r>" % self.user_email #una adecuada práctica para localizar errores al momento de hacer un registro. Es opcional.
    def serialize(self): #nos permite retornar la información en un formato que se pueda leer
        return {
            "id":self.id,
            "email":self.user_email
        }

class Favorites (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character = db.relationship('Character', backref='favorites', lazy= True, uselist=False)
    location = db.relationship('Location', backref= 'favorites', lazy= True, uselist=False)
    episode = db.relationship('Episode', backref= 'favorites', lazy= True, uselist=False)

class Character (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(20))
    character_status = db.Column(db.String(20))
    character_species = db.Column(db.String(20))
    character_origin = db.Column(db.String(20))
    favorites_id = db.Column(db.Integer, db.ForeignKey('favorites.id'))
    location = db.relationship('Location', backref='character', lazy=True)
    episode = db.relationship('Episode', backref = 'character', lazy=True)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(30))
    location_type = db.Column(db.String(30))
    favorites_id = db.Column(db.Integer, db.ForeignKey('favorites.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    
#class Location(Base):
#    episode = relationship("Episode")
#    episode_id=Column(Integer, ForeignKey("episode.id"))

class Episode(db.Model):
    id = id = db.Column(db.Integer, primary_key=True)
    episode_name = db.Column(db.String(30))
    episode_air_date = db.Column(db.String(20))
    favorites_id = db.Column(db.Integer, db.ForeignKey("favorites.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"))

#class Episode(Base):
#    character = relationship(
#        "Character", secondary=character_episode, back_populates="episode")
#    location_id= Column(Integer, ForeignKey("location.id"))
#    location = relationship("Location")