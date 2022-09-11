from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    

    def __repr__(self):
        return '< %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    

    def __repr__(self):
        return '< %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "planet": self.name,
        }


class PeopleFav(db.Model):
    __tablename__ = 'peoplefav'
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user_relationship = db.relationship('User')
    people_relationship = db.relationship('People')
    

    def __repr__(self):
        return '<PeopleFav %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user_relationship.name,
            "name": self.people_relationship.name
            }


class PlanetFav(db.Model):
    __tablename__ = 'planetfav'
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user_relationship = db.relationship('User')
    planet_relationship = db.relationship('Planet')
    
    

    def __repr__(self):
        return '< %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user_relationship.name,
            "name": self.planet_relationship.name
            }

