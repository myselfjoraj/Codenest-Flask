from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

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
    

    def getUsersTableCreationStatement():
        return '''create table users(username varchar(22) 
        primary key,password varchar(22),email varchar(22),
        first_name varchar(22),last_name varchar(22),city varchar(22),
        gender varchar(22),dob varchar(22),martial_status varchar(22),
        age int,number varchar(22),url varchar(500),
        used_storage varchar(500));'''
    
    def getFileDetailsTableCreationStatement():
        return '''create table file_details(id int primary key auto_increment,
        username varchar(22),file_name varchar(22),timestamp varchar(22),
        file_count varchar(22),uri varchar(500),modified varchar(22),
        size varchar(22),extension varchar(22),mode varchar(22),
        type varchar(22));'''
        
        

    