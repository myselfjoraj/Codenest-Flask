import datetime
import time
from urllib.parse import urlparse, quote

import requests
from flask import Flask, Blueprint,render_template, request, redirect, url_for, session, flash, jsonify, send_file
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import urllib.request
import ssl
import tempfile

import firebase_admin
from firebase_admin import credentials, storage
from werkzeug.utils import secure_filename

import ParseFileData
import admin_app
import constants as ckey
from Extras import get_media_type

from database import Database
from login_system import LoginSystem


app = Flask(__name__)

app.secret_key = ckey.getSecretKey()

app.config['MYSQL_HOST'] = ckey.getSqlHost()
app.config['MYSQL_USER'] = ckey.getSqlUser()
app.config['MYSQL_PASSWORD'] = ckey.getSqlPassword()
app.config['MYSQL_DB'] = ckey.getSqlMainDatabase()

mysql = MySQL(app)

cred = credentials.Certificate("servicekey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'codenext-d476c.appspot.com'
})

bucket = storage.bucket()

def getMysql():
    return mysql

# LANDING PAGE ROUTER

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


# LOGIN PAGE ROUTER
@app.route('/login', methods=['GET', 'POST'])
def login():
    re = LoginSystem(mysql).login(request)
    if re == 0:
        msg = "Incorrect Username or Password!"
        return render_template("login.html", msg=msg)
    elif re == 1:
        if session['username'] == "admin":
            return redirect('/admin')
        else:
            return redirect('/dashboard')

    if 'loginMsg' in session:
        msg = session['loginMsg']
        session.pop('loginMsg', None)
        return render_template("login.html", msg=msg)
    return render_template("login.html")


# REGISTER PAGE ROUTER
@app.route('/register', methods=['GET', 'POST'])
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
        if username == "admin":
            return redirect('/admin/dashboard')
        email = session['email']
        pChar = username[0]
        gName = username
        file_array = Database(mysql).FetchFiles(username)
        file_map = ParseFileData.ParseFileData().remake(file_array)
        if file_array is None:
            array_size = 0
        else:
            array_size = file_map.size()

        if 'first_name' in session:
            a = session['first_name']
            if a is not None:
                gName = a
                pChar = a[0]
        return render_template("dashboard.html", fname=gName, uname=username,
                               email=email, letter=pChar, file_map=file_map, array_size=array_size)
    else:
        return redirect('/login')


@app.route('/my-projects')
def my_projects():
    if 'loggedin' in session:
        var = session['loggedin']
    else:
        var = False

    if var:
        username = session['username']
        email = session['email']
        pChar = username[0]
        gName = username
        per = 10
        file_array = Database(mysql).FetchFiles(username)
        file_map = ParseFileData.ParseFileData().remake(file_array)
        # print(file_map.get("a-repo"))
        array_size = 0
        if file_array is None:
            array_size = 0
        else:
            array_size = file_map.size()

        if 'first_name' in session:
            a = session['first_name']
            if a is not None:
                gName = a
                pChar = a[0]
        return render_template("my-projects.html",
                               per=per, fname=gName, uname=username,
                               email=email, letter=pChar, file_map=file_map, array_size=array_size)
    else:
        return redirect('/login')


@app.route('/explore')
def explore():
    if 'loggedin' in session:
        var = session['loggedin']
    else:
        var = False

    if var:
        username = session['username']
        email = session['email']
        pChar = username[0]
        gName = username
        storage = 0
        per = 10
        file_array = Database(mysql).FetchExplore()
        file_map = ParseFileData.ParseFileData().remake(file_array)
        # print(file_map.get("a-repo"))
        array_size = 0
        if file_array is None:
            array_size = 0
        else:
            array_size = file_map.size()
        if 'usedStorage' in session:
            storage = session['usedStorage']
            if storage is not None:
                storage = int(storage)
                per = (storage / 20) * 100
            else:
                storage = 0

        if 'first_name' in session:
            a = session['first_name']
            if a is not None:
                gName = a
                pChar = a[0]
        return render_template("explore.html", storage=storage,
                               per=per, fname=gName, uname=username,
                               email=email, letter=pChar, file_map=file_map, array_size=array_size)
    else:
        return redirect('/login')


@app.route('/starred')
def starred_projects():
    if 'loggedin' in session:
        var = session['loggedin']
    else:
        var = False

    if var:
        username = session['username']
        email = session['email']
        pChar = username[0]
        gName = username
        storage = 0
        per = 10
        file_array = Database(mysql).FetchStarred(username)
        file_map = ParseFileData.ParseFileData().remake(file_array)
        # print(file_map.get("a-repo"))
        array_size = 0
        if file_array is None:
            array_size = 0
        else:
            array_size = file_map.size()
        if 'usedStorage' in session:
            storage = session['usedStorage']
            if storage is not None:
                storage = int(storage)
                per = (storage / 20) * 100
            else:
                storage = 0

        if 'first_name' in session:
            a = session['first_name']
            if a is not None:
                gName = a
                pChar = a[0]
        return render_template("starred.html", storage=storage,
                               per=per, fname=gName, uname=username,
                               email=email, letter=pChar, file_map=file_map, array_size=array_size)
    else:
        return redirect('/login')


@app.route('/discussions')
def discussions():
    if 'loggedin' in session:
        var = session['loggedin']
    else:
        var = False

    if var:
        username = session['username']
        email = session['email']
        pChar = username[0]
        gName = username

        if 'first_name' in session:
            a = session['first_name']
            if a is not None:
                gName = a
                pChar = a[0]
        if username == "admin":
            return render_template("admin-discuss.html", fname=gName, uname=username, email=email, letter=pChar)
        else:
            return render_template("discuss.html", fname=gName, uname=username, email=email, letter=pChar)
    else:
        return redirect('/login')


# CODENEXT AI PAGE ROUTER
@app.route('/codenext-ai')
def ai_chat():
    if 'loggedin' in session:
        var = session['loggedin']
    else:
        var = False

    if var:
        username = session['username']
        email = session['email']
        pChar = username[0]
        gName = username

        if 'first_name' in session:
            a = session['first_name']
            if a is not None:
                gName = a
                pChar = a[0]
        return render_template("codenext-ai.html", fname=gName, uname=username, email=email, letter=pChar)
    else:
        return redirect('/login')


@app.route('/create-project')
def create_project():
    username = session['username']
    alert = None
    if 'errorInRepo' in session:
        alert = session['errorInRepo']
        session.pop('errorInRepo')
    return render_template('create-project.html', username=username, alert=alert)


@app.route('/settings')
def my_settings():
    if 'loggedin' in session:
        var = session['loggedin']
    else:
        var = False

    if var:
        username = session['username']
        email = session['email']
        pChar = username[0]
        gName = username
        username = username.replace("?", "")
        user = Database(mysql).FetchSingleUser(username)

        file_array = Database(mysql).FetchFiles(username)
        file_map = ParseFileData.ParseFileData().remake(file_array)

        if file_array is None:
            array_size = 0
        else:
            array_size = file_map.size()

        al = None
        if 'settingsAlert' in session:
            al = session['settingsAlert']
            session.pop('settingsAlert', None)

        if 'first_name' in session:
            a = session['first_name']
            if a is not None:
                gName = a
                pChar = a[0]
        return render_template("user-settings.html", fname=gName, uname=username,
                               email=email, letter=pChar, array_size=array_size, user=user, file_map=file_map, al=al)
    else:
        return redirect('/login')


@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':

        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        user_name = request.form.get("username")
        city = request.form.get("city")
        genderM = request.form.get("male")
        genderF = request.form.get("female")
        dob = request.form.get("dob")
        status = request.form.get("martial")
        age = request.form.get("age")

        if user_name is not None and not user_name == session['username']:
            nm = Database(mysql).FetchSingleUser(user_name)
            if nm:
                session['settingsAlert'] = "Username already exists!"
                return redirect('/settings')
            else:
                Database(mysql).InsertUserName(user_name)

        if first_name is not None:
            Database(mysql).InsertFirstName(first_name)
        if last_name is not None:
            Database(mysql).InsertLastName(last_name)
        if city is not None:
            Database(mysql).InsertCity(city)
        if genderM is not None:
            Database(mysql).InsertGender("Male")
        if genderF is not None:
            Database(mysql).InsertGender("Female")
        if dob is not None:
            Database(mysql).InsertDOB(dob)
        if status is not None:
            Database(mysql).InsertMartialStatus(status)
        if age is not None:
            if age == "12-18":
                ag = 1
            elif age == "19-32":
                ag = 2
            elif age == "33-45":
                ag = 3
            elif age == "46-62":
                ag = 4
            else:
                ag = 5
            Database(mysql).InsertAge(ag)
        return redirect('/settings')
    return request.method


@app.route('/edit-password', methods=['GET', 'POST'])
def edit_password():
    npass = request.form.get("npass")
    vpass = request.form.get("vpass")
    if npass is None:
        session['settingsAlert'] = "Please enter a password!"
        return redirect('/settings')
    elif vpass is None:
        session['settingsAlert'] = "Please verify the password!"
        return redirect('/settings')
    elif npass != vpass:
        session['settingsAlert'] = "Passwords does not match!"
        return redirect('/settings')
    else:
        Database(mysql).InsertPassword(npass)
        session['settingsAlert'] = "Password changed successfully!"
        return redirect('/settings')


@app.route('/edit-contact', methods=['GET', 'POST'])
def edit_contact():
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    email = request.form.get('email')
    phone = request.form.get('phone')
    print(phone + "")
    if email is not None:
        if re.fullmatch(regex, email):
            Database(mysql).InsertEmail(email)
        else:
            session['settingsAlert'] = "Incorrect email format!"
    if phone is not None:
        Database(mysql).InsertPhone(phone)
        print(phone + "")
    return redirect('/settings')


@app.route('/my-profile')
def my_profile():
    if 'loggedin' in session:
        var = session['loggedin']
    else:
        var = False

    if var:
        username = session['username']
        email = session['email']
        pChar = username[0]
        gName = username
        username = username.replace("?", "")
        user = Database(mysql).FetchSingleUser(username)

        file_array = Database(mysql).FetchFiles(username)
        file_map = ParseFileData.ParseFileData().remake(file_array)

        if file_array is None:
            array_size = 0
        else:
            array_size = file_map.size()

        if 'first_name' in session:
            a = session['first_name']
            if a is not None:
                gName = a
                pChar = a[0]

        return render_template("user-profile.html", fname=gName, uname=username,
                               email=email, letter=pChar, array_size=array_size, user=user, file_map=file_map)
    else:
        return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('email', None)
    session.pop('first_name', None)
    session.pop('last_name', None)
    session.pop('city', None)
    session.pop('gender', None)
    session.pop('dob', None)
    session.pop('martial_status', None)
    session.pop('age', None)
    session.pop('number', None)
    session.pop('url', None)
    session.pop('usedStorage', None)
    return redirect('/home')


@app.route('/view/<file_name>/<path:link>')
def display_file(file_name, link):
    type_media = "application"
    tm_link = link
    try:
        expires = request.args.get('Expires')
        google_access_id = request.args.get('GoogleAccessId')
        signature = request.args.get('Signature')
        signature = quote(signature, safe='')
        tm_link = f"{link}?Expires={expires}&GoogleAccessId={google_access_id}&Signature={signature}"
        parsed_url = urlparse(link)
        file_path = parsed_url.path
        file_path = file_path.replace("/codenext-d476c.appspot.com/", "")
        print("File path:", file_path)
        blob = bucket.blob(file_path)
        # Save the file to a temporary location
        media_type = get_media_type(file_path)
        if media_type is not None:
            media_type = media_type.split("/")[0]
            print("Media Type:", media_type)
            type_media = media_type
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        blob.download_to_filename(temp_file.name)
        # Open the file using the appropriate module or library based on the file type
        # For example, if it's a text file, you can open it using the following code:
        with open(temp_file.name, 'r') as f:
            content = f.read()
            print(content)
            return render_template('display.html', file_content=content, file_name=file_name, file_link=tm_link,
                                   media_type=media_type)
    except Exception as e:
        print("Error:", e)
        content = "Raw file cannot be displayed"
        return render_template('display.html', file_content=content, file_name=file_name, file_link=tm_link,
                               media_type=type_media)


@app.route('/create-repo', methods=['GET', 'POST'])
def create_repos():
    if request.method == 'POST' and 'repo-name' in request.form and 'mode-select' in request.form:
        name = request.form['repo-name']
        mode = request.form.get('mode-select')
        exist = Database(mysql).CheckForFolderName(session['username'], name)
        if exist:
            session['errorInRepo'] = "Folder already exists!"
            return redirect('/create-project')
        else:
            Database(mysql).CreateRepository(name, mode)
            session['alertInDash'] = "Repository created successfully!"
            return redirect('/dashboard')
    else:
        return "not found"


@app.route('/check-repo-exists/<name>', methods=['GET', 'POST'])
def check_repo_existence(name):
    exist = Database(mysql).CheckForFolderName(session['username'], name)
    if exist:
        return jsonify({'status': 'Folder exists'}), 400
    else:
        return jsonify({'status': 'Folder does not exists'}), 200


@app.route('/upload-repository')
def upload_repository():
    username = session['username']
    return render_template('upload-repository.html', username=username)


@app.route('/repo/<repo_name>')
def show_folders(repo_name):
    exist = Database(mysql).CheckForFolderName(session['username'], repo_name)
    if not exist:
        return render_template("404.html")
    username = session['username']
    try:
        file_array = Database(mysql).FetchFilesByRepo(username, repo_name)
        file_map = ParseFileData.ParseFileData().remakeRepo(file_array, 1)
        # print(file_map.get("a-repo"))
        array_size = 0
        if file_array is None:
            array_size = 0
        else:
            array_size = file_map.size()

        return render_template('folder-open.html', file_map=file_map, array_size=array_size, repo_name=repo_name,
                               f_no=2, uname=None)
    except Exception as e:
        return render_template("404.html")


@app.route('/repo/<repo_name>/<file_name>/<no>')
def show_folder_files(repo_name, file_name, no):
    username = session['username']
    file_array = Database(mysql).FetchFilesByRepo(username, repo_name)
    file_map = ParseFileData.ParseFileData().remakeRepoByName(file_array, file_name, int(no))
    # print(file_map.get("a-repo"))
    array_size = 0
    if file_array is None:
        array_size = 0
    else:
        array_size = file_map.size()

    return render_template('folder-open.html', file_map=file_map, array_size=array_size, repo_name=repo_name,
                           f_no=int(no) + 1, uname=None)


@app.route('/<username>/repo/<repo_name>')
def show_folders_of_user(username, repo_name):
    exist = Database(mysql).CheckForFolderName(username, repo_name)
    if not exist:
        return render_template("404.html")
    try:
        file_array = Database(mysql).FetchFilesByUserRepo(username, repo_name)
        file_map = ParseFileData.ParseFileData().remakeRepo(file_array, 1)
        # print(file_map.get("a-repo"))
        array_size = 0
        if file_array is None:
            array_size = 0
        else:
            array_size = file_map.size()

        return render_template('folder-open.html', file_map=file_map, array_size=array_size, repo_name=repo_name,
                               f_no=2, uname=username)
    except Exception as e:
        return render_template("404.html")


@app.route('/<username>/repo/<repo_name>/<file_name>/<no>')
def show_folder_files_of_user(username, repo_name, file_name, no):
    file_array = Database(mysql).FetchFilesByUserRepo(username, repo_name)
    file_map = ParseFileData.ParseFileData().remakeRepoByName(file_array, file_name, int(no))
    # print(file_map.get("a-repo"))
    array_size = 0
    if file_array is None:
        array_size = 0
    else:
        array_size = file_map.size()

    return render_template('folder-open.html', file_map=file_map, array_size=array_size, repo_name=repo_name,
                           f_no=int(no) + 1, uname=username)


@app.route('/search/codenext/<repo_name>')
def search_codenext_repo(repo_name):
    if 'loggedin' in session:
        var = session['loggedin']
    else:
        var = False

    if var:
        username = session['username']
        email = session['email']
        pChar = username[0]
        gName = username
        file_array = Database(mysql).FetchFilesByName(username, repo_name, False)
        file_map = ParseFileData.ParseFileData().remake(file_array)
        array_size = 0
        desc = "Search Codenext"
        if file_array is None:
            array_size = 0
        else:
            array_size = file_map.size()
            desc = "Found " + str(array_size) + " file(s) from Codenext Repositories"

        if 'first_name' in session:
            a = session['first_name']
            if a is not None:
                gName = a
                pChar = a[0]
        return render_template("search-files.html", fname=gName, uname=username, repo_name=repo_name,
                               email=email, letter=pChar, file_map=file_map, array_size=array_size,
                               desc=desc, isMine=0)
    else:
        return redirect('/login')


@app.route('/search/me/<repo_name>')
def search_my_repo(repo_name):
    if 'loggedin' in session:
        var = session['loggedin']
    else:
        var = False

    if var:
        username = session['username']
        email = session['email']
        pChar = username[0]
        gName = username
        file_array = Database(mysql).FetchFilesByName(username, repo_name, True)
        file_map = ParseFileData.ParseFileData().remake(file_array)
        array_size = 0
        desc = "Search Repositories"
        if file_array is None:
            array_size = 0
        else:
            array_size = file_map.size()
            desc = "Found " + str(array_size) + " file(s) from your repositories"

        if 'first_name' in session:
            a = session['first_name']
            if a is not None:
                gName = a
                pChar = a[0]
        return render_template("search-files.html", fname=gName, uname=username, repo_name=repo_name,
                               email=email, letter=pChar, file_map=file_map, array_size=array_size,
                               desc=desc, isMine=1)
    else:
        return redirect('/login')


@app.route('/search/users/<name>')
def search_codenext_users(name):
    if 'loggedin' in session:
        var = session['loggedin']
    else:
        var = False

    if var:
        username = session['username']
        email = session['email']
        pChar = username[0]
        gName = username
        name = name.replace("?", "")
        user_array = Database(mysql).FetchUser(name)
        array_size = 0
        desc = "Search Users"

        if user_array is None:
            array_size = 0
        else:
            array_size = len(user_array)
            desc = "Found " + str(array_size) + " user(s) on Codenext"

        if 'first_name' in session:
            a = session['first_name']
            if a is not None:
                gName = a
                pChar = a[0]

        return render_template("search-users.html", fname=gName, uname=username, name=name, desc=desc,
                               email=email, letter=pChar, array_size=array_size, user_array=user_array)
    else:
        return redirect('/login')


@app.route('/user/<username>')
def user_profile(username):
    if 'loggedin' in session:
        var = session['loggedin']
    else:
        var = False

    if var:
        username = session['username']
        email = session['email']
        pChar = username[0]
        gName = username
        username = username.replace("?", "")
        user = Database(mysql).FetchSingleUser(username)

        file_array = Database(mysql).FetchFilesByPublicUser(username)
        file_map = ParseFileData.ParseFileData().remake(file_array)

        if file_array is None:
            array_size = 0
        else:
            array_size = file_map.size()

        if 'first_name' in session:
            a = session['first_name']
            if a is not None:
                gName = a
                pChar = a[0]

        return render_template("user-profile.html", fname=gName, uname=username,
                               email=email, letter=pChar, array_size=array_size, user=user, file_map=file_map)
    else:
        return redirect('/login')


@app.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        data = request.json  # Access JSON data from the request
        message = data.get('message')  # Get the 'message' value from JSON data

        if message:
            Database(mysql).CreateMessage(message)
            return jsonify({'status': 'Message sent successfully'}), 200
        else:
            return jsonify({'status': 'Message not provided'}), 400
    else:
        return jsonify({'status': 'Invalid request method'}), 405


@app.route('/fetch_messages', methods=['GET', 'POST'])
def fetch_message():
    return Database(mysql).FetchMessages()


@app.route('/send_ai_message', methods=['POST'])
def send_ai_message():
    if request.method == 'POST':
        data = request.json  # Access JSON data from the request
        message = data.get('message')  # Get the 'message' value from JSON data
        m_user = data.get('user')
        is_mine = False
        if m_user == "me":
            is_mine = True

        if message:
            Database(mysql).CreateAiMessage(message, is_mine)
            return jsonify({'status': 'Message sent successfully'}), 200
        else:
            return jsonify({'status': 'Message not provided'}), 400
    else:
        return jsonify({'status': 'Invalid request method'}), 405


@app.route('/fetch_ai_messages', methods=['GET', 'POST'])
def fetch_ai_message():
    return Database(mysql).FetchAiMessages()


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files found in request'}), 400

    files = request.files.getlist('files[]')
    paths = request.form.getlist('filepath[]')
    names = request.form.getlist('filename[]')
    sizes = request.form.getlist('filesize[]')
    extes = request.form.getlist('fileextension[]')
    name = request.form.get('repo-name')
    name.replace(" ", "-")

    print(paths)
    i = 0
    for file in files:
        # Upload file to Firebase Storage
        my_path = session['username'] + "/" + name
        blob = bucket.blob(f'{my_path}/{file.filename}')
        blob.upload_from_file(file)
        expiration_time = datetime.datetime.now() + datetime.timedelta(days=365)  # Set expiration to 1 year from now
        url = blob.generate_signed_url(expiration=expiration_time)
        Database(mysql).InsertUploadRepo(name, names[i], paths[i], url, sizes[i], extes[i], "Private")
        i = i + 1

    return jsonify({'message': 'Files uploaded successfully'}), 200


@app.route('/upload-single', methods=['POST'])
def upload_single_file():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files found in request'}), 400

    files = request.files.getlist('files[]')

    i = 0
    for file in files:
        # Upload file to Firebase Storage
        my_path = "profileimage/" + session['username']
        blob = bucket.blob(f'{my_path}/{session['username']}')
        blob.upload_from_file(file)
        expiration_time = datetime.datetime.now() + datetime.timedelta(days=365)  # Set expiration to 1 year from now
        url = blob.generate_signed_url(expiration=expiration_time)
        Database(mysql).InsertProfileImage(url)
        i = i + 1

    return jsonify({'message': 'Files uploaded successfully'}), 200


@app.route('/star/<repo_name>/<st>', methods=['POST', 'GET'])
def star_a_file(repo_name, st):
    Database(mysql).ChangeStarred(repo_name, st)
    return "success", 200


@app.route('/star/<repo_name>/<st>/<return_page>', methods=['POST', 'GET'])
def star_a_file_page(repo_name, st, return_page):
    Database(mysql).ChangeStarred(repo_name, st)
    return redirect('/' + return_page)


@app.route('/chmod/<repo_name>/<st>', methods=['POST'])
def mode_a_file(repo_name, st):
    Database(mysql).MakePrivatePublic(repo_name, st)
    return "success", 200


@app.route('/chmod/<repo_name>/<st>/<return_page>', methods=['POST', 'GET'])
def mode_a_file_page(repo_name, st, return_page):
    Database(mysql).MakePrivatePublic(repo_name, st)
    return redirect('/' + return_page)


@app.route('/delete/<repo_name>', methods=['POST'])
def delete_a_repo(repo_name):
    print("triggered delete for " + repo_name)
    Database(mysql).DeleteRepo(repo_name)
    return "success", 200


@app.route('/delete/<repo_name>/<return_page>', methods=['POST', 'GET'])
def delete_a_repo_page(repo_name, return_page):
    print("triggered delete for " + repo_name)
    Database(mysql).DeleteRepo(repo_name)
    return redirect('/' + return_page)


@app.route('/download/<repo_name>')
def download_folder(repo_name):
    username = session['username']
    return render_template('download-page.html', username=username, repo_name=repo_name)


@app.route('/<username>/download/<repo_name>')
def download_folder_of_user(username, repo_name):
    return render_template('download-page.html', username=username, repo_name=repo_name)


# Admin routers
@app.route('/admin')
@app.route('/admin/dashboard')
def admin_dash():
    if session['username'] != "admin":
        return redirect('/login')
    return admin_app.admin_dashboard(mysql)

@app.route('/admin/delete')
def admin_delete():
    if session['username'] != "admin":
        return redirect('/login')
    return admin_app.admin_delete(mysql)

if __name__ == '__main__':
    app.run(debug=True)
