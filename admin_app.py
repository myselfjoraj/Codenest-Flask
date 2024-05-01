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


def admin_dashboard(mysql):
    user_array = Database(mysql).FetchEveryUser()
    return render_template('admin-dash.html', user_array=user_array)


def admin_delete(mysql):
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
