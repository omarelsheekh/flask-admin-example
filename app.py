from flask import Flask,request,jsonify
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import Column, String, Integer, create_engine

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='secret'
# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
db=SQLAlchemy(app)

# models
class User(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String, nullable=False)
    posts=db.relationship('Post', backref='user')

class Post(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)
    user_id = Column(db.Integer , db.ForeignKey('user.id'),nullable=False) 

db.create_all()

# admin
admin = Admin(app, name='microblog', template_mode='bootstrap3')

class AppModelView(ModelView):
    # full reference
    # https://flask-admin.readthedocs.io/en/latest/introduction/#customizing-builtin-views
    can_view_details = True

    def is_accessible(self):
        # return is_authorized() for example
        return True

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return 'you need to login'

admin.add_view(AppModelView(User, db.session))
admin.add_view(AppModelView(Post, db.session))

if __name__ == "__main__":
    app.run(port=5000, debug=True, host='0.0.0.0')