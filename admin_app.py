import datetime
import time
from urllib.parse import urlparse, quote

import requests
from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, send_file
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
import constants as ckey
from Extras import get_media_type

from database import Database
from login_system import LoginSystem


def admin_dashboard(mysql, name):
    if name is not None:
        user_array = Database(mysql).FetchUser(name)
    else:
        user_array = Database(mysql).FetchEveryUser()
    return render_template('admin-dash.html', user_array=user_array)


def admin_delete(mysql, name):
    if name is not None:
        user_array = Database(mysql).FetchUser(name)
    else:
        user_array = Database(mysql).FetchEveryUser()
    return render_template('admin-delete.html', user_array=user_array)


def admin_show_profile(mysql, uname):
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
        user = Database(mysql).FetchSingleUser(uname)

        file_array = Database(mysql).FetchFiles(uname)
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

        return render_template("admin-user-profile.html", fname=gName, uname=username,
                               email=email, letter=pChar, array_size=array_size, user=user, file_map=file_map)
    else:
        return redirect('/login')


def show_folders_of_user(username, repo_name, mysql):
    exist = Database(mysql).CheckForFolderName(username, repo_name)
    if not exist:
        return render_template("404.html")
    try:
        file_array = Database(mysql).FetchFilesByUserRepoAdmin(username, repo_name)
        file_map = ParseFileData.ParseFileData().remakeRepo(file_array, 1)
        if file_array is None:
            array_size = 0
        else:
            array_size = file_map.size()

        return render_template('admin-folder-open.html', file_map=file_map, array_size=array_size, repo_name=repo_name,
                               f_no=2, uname=username)
    except Exception as e:
        return render_template("404.html")


def show_folder_files_of_user(username, repo_name, file_name, no, mysql):
    file_array = Database(mysql).FetchFilesByUserRepoAdmin(username, repo_name)
    file_map = ParseFileData.ParseFileData().remakeRepoByName(file_array, file_name, int(no))
    if file_array is None:
        array_size = 0
    else:
        array_size = file_map.size()

    return render_template('admin-folder-open.html', file_map=file_map, array_size=array_size, repo_name=repo_name,
                           f_no=int(no) + 1, uname=username)


def display_file(file_name, link, bucket):
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
            return render_template('admin-display.html', file_content=content, file_name=file_name, file_link=tm_link,
                                   media_type=media_type)
    except Exception as e:
        print("Error:", e)
        content = "Raw file cannot be displayed"
        return render_template('admin-display.html', file_content=content, file_name=file_name, file_link=tm_link,
                               media_type=type_media)


def admin_add_user(request, mysql):
    username = request.form['username']
    password = request.form['password']
    r_password = request.form['repeatpassword']
    first_name = request.form['firstname']
    last_name = request.form['lastname']
    phone = request.form['phone']
    email = request.form['email']
    if username is None:
        session['addUserAlert'] = "Please enter an username!"
        return redirect('/admin/user/add')

    nm = Database(mysql).FetchSingleUser(username)
    if nm:
        session['addUserAlert'] = "Username already exists!"

    elif password != r_password:
        session['addUserAlert'] = "Passwords does not match!"

    elif email is None:
        session['addUserAlert'] = "Please enter a email!"
    else:
        Database(mysql).InsertUserAdmin(username, password, email, first_name, last_name, phone)
        session['addUserAlert'] = "User Added Successfully"

    return redirect('/admin/user/add')


def admin_upload_single_file(request, name, bucket, mysql):
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files found in request'}), 400

    files = request.files.getlist('files[]')

    i = 0
    for file in files:
        # Upload file to Firebase Storage
        my_path = "profileimage/" + name
        blob = bucket.blob(f'{my_path}/{name}')
        blob.upload_from_file(file)
        expiration_time = datetime.datetime.now() + datetime.timedelta(days=365)  # Set expiration to 1 year from now
        url = blob.generate_signed_url(expiration=expiration_time)
        Database(mysql).InsertAdminProfileImage(url, name)
        i = i + 1

    return jsonify({'message': 'Files uploaded successfully'}), 200


def admin_edit_password(request, uname, mysql):
    npass = request.form.get("npass")
    vpass = request.form.get("vpass")
    if npass is None:
        session['editUserAlert'] = "Please enter a password!"
        return redirect('/admin/user/edit/' + uname)
    elif vpass is None:
        session['editUserAlert'] = "Please verify the password!"
        return redirect('/admin/user/edit/' + uname)
    elif npass != vpass:
        session['editUserAlert'] = "Passwords does not match!"
        return redirect('/admin/user/edit/' + uname)
    else:
        Database(mysql).InsertAdminPassword(uname, npass)
        session['editUserAlert'] = "Password changed successfully!"
        return redirect('/admin/user/edit/' + uname)


def admin_edit_contact(request, uname, mysql):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    email = request.form.get('email')
    phone = request.form.get('phone')
    print(phone + "")
    if email is not None:
        if re.fullmatch(regex, email):
            Database(mysql).InsertAdminEmail(uname, email)
        else:
            session['editUserAlert'] = "Incorrect email format!"
    if phone is not None:
        Database(mysql).InsertAdminPhone(uname, phone)
        print(phone + "")
    return redirect('/admin/user/edit/' + uname)


def admin_edit_profile(request, uname, mysql):
    if request.method == 'POST':

        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        user_name = request.form.get("username")
        city = request.form.get("city")
        genderM = request.form.get("male")
        genderF = request.form.get("female")
        dob = request.form.get("dob")
        status = request.form.get("marital")
        age = request.form.get("age")

        if user_name is not None and not user_name == uname:
            nm = Database(mysql).FetchSingleUser(user_name)
            if nm:
                session['editUserAlert'] = "Username already exists!"
                return redirect('/admin/user/edit/' + uname)
            else:
                Database(mysql).InsertAdminUserName(uname, user_name)

        if first_name is not None:
            Database(mysql).InsertAdminFirstName(uname, first_name)
        if last_name is not None:
            Database(mysql).InsertAdminLastName(uname, last_name)
        if city is not None:
            Database(mysql).InsertAdminCity(uname, city)
        if genderM is not None:
            Database(mysql).InsertAdminGender(uname, "Male")
        if genderF is not None:
            Database(mysql).InsertAdminGender(uname, "Female")
        if dob is not None:
            Database(mysql).InsertAdminDOB(uname, dob)
        if status is not None:
            Database(mysql).InsertAdminMartialStatus(uname, status)
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
            Database(mysql).InsertAdminAge(uname, ag)
        session['editUserAlert'] = "Successfully updated!"
        return redirect('/admin/user/edit/' + uname)
    return request.form


def admin_delete_user(uname, mysql):
    Database(mysql).DeleteUser(uname)
    return redirect('/admin/delete')
