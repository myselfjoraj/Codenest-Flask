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


def show_folders_of_user(username, repo_name,mysql):
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
