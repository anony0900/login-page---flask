from flask_sqlalchemy import SQLAlchemy
# Flask is lightweight and doesn't include database or model creation tools.
# import SQLAlchemy uses ORM Object relational mapping to create the model and interface with a database.
from werkzeug.security import generate_password_hash, check_password_hash
# Always want to encrypt passwords.
from flask_login import UserMixin, LoginManager
 
 
# instances
login = LoginManager()
db = SQLAlchemy()
 # subclass db.Model and UserMixin.
 # UserMixin provides methods to track the user.
 # is_authenticated() returns True if the user has already provided credentials
 # an is_active() method that returns True if the user’s account is active
 # an is_anonymous() method that returns True if the current user is an anonymous user
 # a get_id() method which, given a User instance, returns the unique ID for that object

 # 
class User(UserMixin,db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(),unique=True)
    pw_hash = db.Column(db.String())
    
    def set_pwd(self,pwd):
        self.pw_hash=generate_password_hash(pwd)
        
    def check_pwd(self,pwd):
        return check_password_hash(self.pw_hash,pwd)

 
# needed for Flask Login to get the user id from the DB for the session.
@login.user_loader
def load_user(id):
    return User.query.get(int(id))