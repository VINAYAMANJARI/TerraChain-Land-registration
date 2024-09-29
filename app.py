from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from blockchain import Blockchain

app = Flask(__name__)
app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

blockchain = Blockchain()

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Sign up route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = sha256_crypt.encrypt(request.form['password'])
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return 'Username already exists!'
        
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and sha256_crypt.verify(password, user.password):
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials!'
    
    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

# Add new block
# @app.route('/add_block', methods=['POST'])
# def add_block():
#     if 'username' in session:
#         data = request.form['data']
#         blockchain.add_block(data)
#         return redirect(url_for('dashboard'))
#     return redirect(url_for('login'))
@app.route('/add_block', methods=['POST'])
def add_block():
    if 'username' in session:
        data = request.form['data']
        
        # Check if the block data already exists
        if any(block['data'] == data for block in blockchain.get_chain()):
            flash('This block data already exists!', 'danger')  # Flash a message
        else:
            blockchain.add_block(data)
            flash('Block added successfully!', 'success')  # Flash a success message
        
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# View block history
@app.route('/history')
def history():
    if 'username' in session:
        blocks = blockchain.get_chain()
        return render_template('history.html', blocks=blocks)
    return redirect(url_for('login'))

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# about page
@app.route('/about')
def about():
    return render_template('about.html')

# Main Function
if __name__ == '__main__':
    with app.app_context():  # Use app context to initialize the database
        db.create_all()      # Creates the database tables
    
    app.run(debug=True)       # Run the Flask app
