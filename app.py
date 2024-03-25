from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

import constants as ckey

from database import Database
from login_system import LoginSystem

app = Flask(__name__)

app.secret_key = ckey.getSecretKey()

app.config['MYSQL_HOST']     = ckey.getSqlHost()
app.config['MYSQL_USER']     = ckey.getSqlUser()
app.config['MYSQL_PASSWORD'] = ckey.getSqlPassword()
app.config['MYSQL_DB']       = ckey.getSqlMainDatabase()

mysql = MySQL(app);

# LANDING PAGE ROUTER
@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


# LOGIN PAGE ROUTER
@app.route('/login', methods =['GET', 'POST'])
def login():
    re = LoginSystem(mysql).login(request)
    if re == 0:
        msg = "Incorrect Username or Password!"
        return render_template("login.html", msg = msg)
    elif re == 1:
        return redirect('/dashboard')
    
    if 'loginMsg' in session:
        msg = session['loginMsg']
        session.pop('loginMsg',None)
        return render_template("login.html", msg = msg)
    return render_template("login.html")


# REGISTER PAGE ROUTER
@app.route('/register', methods=['GET','POST'])
def register():
    re = LoginSystem(mysql).register(request)
    if re == 1:
        session['loginMsg'] = "User already Exists! Please Log In."
        return redirect("/login")
    elif re == 2:
        session['loginMsg'] = "User Registered Successfully! Please Log In."
        return redirect("/login")
    return render_template("register.html")
        


# DASHBOARD PAGE ROUTER
@app.route('/dashboard')
def dashboard():

    if 'loggedin' in session:
        var = session['loggedin']
    else:
        var = False

    if var:
        username = session['username']
        email    = session['email']
        pChar    = username[0]
        gName    = username
        storage  = 0        
        per      = 10
        file_array = Database(mysql).FetchFiles(username)
        array_size = 0
        if(file_array is None):
            array_size = 0
        else:
            array_size = len(file_array)
        if 'usedStorage' in session:
            storage = session['usedStorage']
            if storage is not None:
                storage = int(storage)
                per = (storage/20)*100
            else:
                storage = 0

        if 'first_name' in session:
            a = session['first_name']
            if a is not None:
                gName = a
                pChar = a[0]
        return render_template("dashboard.html",storage = storage,
                               per = per,fname = gName,uname = username,
                               email = email,letter = pChar,file_array = file_array,array_size = array_size)
    else:
        return redirect('/login')
    
@app.route('/my-projects')
def my_projects():
    return;

@app.route('/explore')
def explore():
    return;

@app.route('/starred')
def starred_projects():
    return;

@app.route('/discussions')
def discussions():
    return;
    
# CODENEXT AI PAGE ROUTER
@app.route('/codenext-ai')
def ai_chat():
    return render_template("codenext-ai.html")

@app.route('/create-project')
def create_project():
    username = session['username']
    alert = None
    if 'errorInRepo' in session:
        alert = session['errorInRepo']
        session.pop('errorInRepo')
    return render_template('create-project.html', username=username, alert=alert);

@app.route('/settings')
def my_settings():
    return;

@app.route('/my-profile')
def my_profile():
    return;

@app.route('/search')
def search():
    return;

@app.route('/view')
def preview_file():
    return;

@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('username',None)
    session.pop('email',None)
    session.pop('first_name',None)
    session.pop('last_name',None)
    session.pop('city',None)
    session.pop('gender',None)
    session.pop('dob',None)
    session.pop('martial_status',None)
    session.pop('age',None)
    session.pop('number',None)
    session.pop('url',None)
    session.pop('usedStorage',None)
    return redirect('/home')
    

@app.route('/display')
def display_file():
    file_path = "D:\\PebbleNew\\app\\google-services.json"  # Replace with the actual path to your file

    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        return render_template('display.html', file_content=file_content)
    except FileNotFoundError:
        return "File not found."
    
@app.route('/create-repo', methods =['GET', 'POST'])
def create_repos():
    if request.method == 'POST' and 'repo-name' in request.form and 'mode-select' in request.form:
            name = request.form['repo-name']
            mode = request.form.get('mode-select')
            exist = Database(mysql).CheckForFolderName(session['username'],name)
            if exist:
                session['errorInRepo'] = "Folder already exists!"
                return redirect('/create-project')
            else:
                Database(mysql).CreateRepository(name,mode)
                session['alertInDash'] = "Repository created successfully!"
                return redirect('/dashboard')
    
    else:
        return "not found"


def hello(): 
    ins = Database(mysql)
    ins.InsertUsers()
    return 'HELLO'


  
if __name__=='__main__': 
   app.run(debug=True) 