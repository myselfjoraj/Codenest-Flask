from flask import Flask, render_template, request, redirect, url_for, session, json
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
        cursor.execute('INSERT INTO users(username,password,email) VALUES (% s, % s, % s)',
                       (username, password, email,))
        self.mysql.connection.commit()

    def CheckForUser(self, username, password):
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password,))
        account = cursor.fetchone()
        return account

    def CreateRepository(self, file_name, mode):
        username = session['username']
        timestamp = time.time()
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''INSERT INTO file_details(username,file_name,repo_name,timestamp,file_count,modified,size,
        extension, mode,type) VALUES (% s, % s, % s,% s, % s, % s, % s, % s, % s, % s)''',
                       (username, file_name, file_name, timestamp, "1", timestamp, "1000", "folder", mode, "folder"))
        self.mysql.connection.commit()

    def InsertUploadRepo(self, repo_name, file_name, path, uri, size, extension, mode):
        username = session['username']
        timestamp = time.time()
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''INSERT INTO file_details(username,file_name,repo_name,timestamp,uri,file_count,path,modified,
        size,extension,mode,type) VALUES (% s, % s, % s,% s,% s,% s, % s, % s, % s, % s, % s, % s)''',
                       (username, file_name, repo_name.replace(" ", "-"), timestamp, uri, "1", path, timestamp, size,
                        extension, mode, "files"))
        self.mysql.connection.commit()

    def FetchFiles(self, username):
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

            size = float(file_instance.size)
            #file_instance.size = str(size)

            model_instances.append(file_instance)
        return model_instances

    def FetchFilesByRepo(self, username, repo):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM file_details where username=%s and repo_name=%s", (username, repo,))
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

            size = float(file_instance.size)
            #file_instance.size = str(size)

            model_instances.append(file_instance)
        return model_instances

    def FetchExplore(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM file_details")
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

            size = float(file_instance.size)
            # file_instance.size = str(size)

            model_instances.append(file_instance)
        return model_instances

    def FetchStarred(self, username):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM file_details where username=%s and type='star' ", (username,))
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
            size = size / (1000 * 1000)
            file_instance.size = str(size) + " MB"

            model_instances.append(file_instance)
        return model_instances

    def CreateMessage(self, message):
        username = session['username']
        timestamp = time.time()
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''INSERT INTO discussions(username,message,timestamp) VALUES 
                       (% s, % s, % s)''', (username, message, timestamp))
        self.mysql.connection.commit()

    def FetchMessages(self):
        username = session['username']
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
        messages_dict = [message.to_dict() for message in model_instances]
        json_data = json.dumps(messages_dict)

        # return model_instances
        return json_data

    def CheckForFolderName(self, username, file_name):
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM file_details WHERE username = % s AND repo_name= % s', (username, file_name,))
        files = cursor.fetchone()
        return files

    # FILE OPERATIONS ///
    def ChangeStarred(self, repo_name, starred):
        username = session['username']
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if starred == "star":
            cursor.execute('''UPDATE file_details SET type= 'notstar' WHERE username = %s and repo_name = %s''',
                           (username, repo_name,))
            print("changed star")
        else:
            cursor.execute('''UPDATE file_details SET type= 'star' WHERE username = %s and repo_name = %s''',
                           (username, repo_name,))
            print("made star")
        self.mysql.connection.commit()

    def MakePrivatePublic(self, repo_name, mode):
        username = session['username']
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if mode == "Private":
            cursor.execute('''UPDATE file_details SET mode= 'Public' WHERE username = %s and repo_name = %s''',
                           (username, repo_name,))
            print("made public")
        else:
            cursor.execute('''UPDATE file_details SET mode= 'Private' WHERE username = %s and repo_name = %s''',
                           (username, repo_name,))
            print("made private")
        self.mysql.connection.commit()

    def DeleteRepo(self, repo_name):
        username = session['username']
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''DELETE FROM file_details WHERE username = %s and repo_name = %s''',
                           (username, repo_name,))
        print("deleted "+repo_name)
        self.mysql.connection.commit()

    def getDiscussionsTableCreationStatement():
        return ''' create table discussions(id int primary key auto_increment,username varchar(22),message varchar(22),timestamp varchar(22)); '''

    def getUsersTableCreationStatement():
        return '''create table users(username varchar(22) 
        primary key,password varchar(22),email varchar(22),
        first_name varchar(22),last_name varchar(22),city varchar(22),
        gender varchar(22),dob varchar(22),martial_status varchar(22),
        age int,number varchar(22),url varchar(500),
        used_storage varchar(500));'''

    def getFileDetailsTableCreationStatement():
        return '''create table file_details(id int primary key auto_increment,
        username varchar(22),file_name TEXT,repo_name TEXT,timestamp varchar(22),
        file_count varchar(22),path TEXT,uri TEXT,modified varchar(22),
        size TEXT,extension TEXT,mode varchar(22),
        type varchar(22));'''
