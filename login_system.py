from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

from database import Database

class LoginSystem:

    def __init__(self,sql):
        self.mysql = sql

    def login(self,request):
        msg = -1
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']

            account = Database(self.mysql).CheckForUser(username,password)

            if account:
                session['loggedin'] = True
                session['username'] = account['username']
                session['email'] = account['email']
                session['first_name']  = account['first_name']
                session['last_name'] = account['last_name']
                session['city'] = account['city']
                session['gender'] = account['gender']
                session['dob'] = account['dob']
                session['martial_status'] = account['martial_status']
                session['age'] = account['age']
                session['number'] = account['number']
                session['url'] = account['url']
                session['usedStorage'] = account['used_storage']
                msg = 1
            else:
                msg = 0

        return msg
    
    def register(self,request):
        msg = -1
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            username = request.form['username']
            password = request.form['password']
            email    = request.form['email']

            account = Database(self.mysql).CheckForUser(username,password)

            if account:
                msg = 1
            else:
                Database(self.mysql).InsertUsers(username,password,email)
                msg = 2
        return msg