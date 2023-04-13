from flask import Flask, render_template, request, redirect
from flask_login import current_user, login_required, login_user, logout_user
from models import User, db, login
 
app = Flask(__name__)
# flask requires this in order to protect session information
app.secret_key = 'shouldbesecret'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# let sqalchemy know about the flask app.
db.init_app(app)

login.init_app(app)
login.login_view = 'login'

# decoration to create the database before the first request.
@app.before_first_request
def fill_db():
    db.create_all()

# maps url /products to the function products. login required requires credentials     
@app.route('/products')
@login_required
def products():
    products = [
        {'ID':1,'name':'Campus','sku':'cam3'},
        {'ID':2,'name':'Nike','sku':'ni2'},
        {'ID':3,'name':'Adidas','sku':'ad5'},
        {'ID':4,'name':'Puma','sku':'pu8'}
    ]


    return render_template("product.html", products=products) 
 
@app.route('/login',methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/products')
     
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email = email).first()
        if user is not None and user.check_pwd(request.form['password']):
            login_user(user)
            return redirect('/products')
        
    # for GET request
    return render_template('login.html')
 
@app.route('/register',methods=['POST','GET'])

def register():
    if current_user.is_authenticated:
        return redirect('/products')
     
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(email=email).first():
            return redirect('register')

        # add the user to the database
        user = User(email=email)
        user.set_pwd(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')
 
@app.route('/departments')
@login_required
def departments():
    
    departments = [
        {'ID':1,'name':'CSE','dept_no':101},
        {'ID':4,'name':'CE','dept_no':138},
        {'ID':7,'name':'ME','dept_no':142},
        {'ID':2,'name':'ECE','dept_no':201}
    ]
    return render_template('departments.html',departments=departments)
 
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

if __name__ == '__main__':
     app.run(debug=True)
