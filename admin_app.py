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
    return render_template('admin-dash.html',user_array=user_array)

def admin_delete(mysql):
    user_array = Database(mysql).FetchEveryUser()
    return render_template('admin-delete.html',user_array=user_array)
