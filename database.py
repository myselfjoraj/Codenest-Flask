from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import FileModel

class Database:

    def __init__(self, sql):
        self.mysql = sql

    def InsertUsers(self, username, password, email):
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO users(username,password,email) VALUES (% s, % s, % s)', (username, password, email, ))
        self.mysql.connection.commit()

    def CheckForUser(self, username, password):
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        return account
        

    