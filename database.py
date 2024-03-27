from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import FileModel
import Message
from datetime import datetime
import time

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
    
    def CreateRepository(self,file_name,mode):
        username = session['username']
        timestamp = time.time()
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''INSERT INTO file_details(username,file_name,timestamp,file_count,modified,size,extension,mode,type) VALUES 
                       (% s, % s, % s, % s, % s, % s, % s, % s, % s)''', (username, file_name,timestamp,"1",timestamp,"1000","folder",mode,"folder" ))
        self.mysql.connection.commit()
    
    def FetchFiles(self,username):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM file_details where username=%s", (username,))
        data = cur.fetchall()
        cur.close()
        model_instances = []
        for row in data:
            file_instance = FileModel.FileModel(*row)

            timestamp_dt = datetime.fromtimestamp(float(file_instance.timestamp))
            formatted_date = timestamp_dt.strftime("%d/%m/%Y %I:%M %p")
            file_instance.timestamp = formatted_date

            timestamp_dt2 = datetime.fromtimestamp(float(file_instance.modified))
            formatted_date2 = timestamp_dt2.strftime("%d/%m/%Y %I:%M %p")
            file_instance.modified = formatted_date2

            size = int(file_instance.size);
            size = size/(1000*1000)
            file_instance.size = str(size)+" MB"

            model_instances.append(file_instance)
        return model_instances
    
    def FetchExplore(self,username):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM file_details where username=%s", (username,))
        data = cur.fetchall()
        cur.close()
        model_instances = []
        for row in data:
            file_instance = FileModel.FileModel(*row)

            timestamp_dt = datetime.fromtimestamp(float(file_instance.timestamp))
            formatted_date = timestamp_dt.strftime("%d/%m/%Y %I:%M %p")
            file_instance.timestamp = formatted_date

            timestamp_dt2 = datetime.fromtimestamp(float(file_instance.modified))
            formatted_date2 = timestamp_dt2.strftime("%d/%m/%Y %I:%M %p")
            file_instance.modified = formatted_date2

            size = int(file_instance.size);
            size = size/(1000*1000)
            file_instance.size = str(size)+" MB"

            model_instances.append(file_instance)
        return model_instances
    
    def FetchStarred(self,username):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM file_details where username=%s", (username,))
        data = cur.fetchall()
        cur.close()
        model_instances = []
        for row in data:
            file_instance = FileModel.FileModel(*row)

            timestamp_dt = datetime.fromtimestamp(float(file_instance.timestamp))
            formatted_date = timestamp_dt.strftime("%d/%m/%Y %I:%M %p")
            file_instance.timestamp = formatted_date

            timestamp_dt2 = datetime.fromtimestamp(float(file_instance.modified))
            formatted_date2 = timestamp_dt2.strftime("%d/%m/%Y %I:%M %p")
            file_instance.modified = formatted_date2

            size = int(file_instance.size);
            size = size/(1000*1000)
            file_instance.size = str(size)+" MB"

            model_instances.append(file_instance)
        return model_instances
    
    def FetchMessages(self, username):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM discussions;")
        data = cur.fetchall()
        cur.close()
        model_instances = []
        for row in data:
            message_instance = Message.Message(*row)
            timestamp_dt = datetime.fromtimestamp(float(message_instance.timestamp))
            formatted_date = timestamp_dt.strftime("%d/%m/%Y %I:%M %p")
            message_instance.timestamp = formatted_date
            if message_instance.username == username:
                message_instance.isMine = True
            else:
                message_instance.isMine = False

            model_instances.append(message_instance)

        return model_instances
    
    
    def CheckForFolderName(self, username, file_name):
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM file_details WHERE username = % s AND file_name= % s', (username, file_name, ))
        files = cursor.fetchone()
        return files
    
    def getDiscussionsTableCreationStatement():
        return ''' create table discussions(id int primary key auto_increment,username varchar(22),
        name varchar(22),message varchar(22),timestamp varchar(22)); '''

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
        
        

    