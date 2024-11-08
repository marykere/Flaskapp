from accapp import db, login_manager, app
from datetime import datetime
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(200), unique=True, nullable=False)
    image_file=db.Column(db.String(200), nullable=False, default='default.jpg')
    password=db.Column(db.String(60), nullable=False)
    posts=db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self): # expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY']) #, expires_sec)
        return s.dumps({'user_id': self.id}) #.decode('utf-8')
        # If the token is bytes, decode it; otherwise, return it as is
        # if isinstance(token, bytes):
        #     return token.decode('utf-8')
    
        # return token

    
    @staticmethod
    def verify_reset_token(token): #this takes an argument as a token 
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id'] #loads that token

        except:
            return None
        return User.query.get(user_id)

    def __ref__(self):
        return f"({self.username}, {self.email}, {self.image_file})"
    
class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.now)
    content=db.Column(db.Text, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __ref__(self):
        return f"({self.title}, {self.date_posted})"
