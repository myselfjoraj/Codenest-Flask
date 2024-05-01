from flask import Flask, render_template, request, redirect, url_for, session, json
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import FileModel
import Message
from datetime import datetime
import time

import UserModel


class Database:

    def __init__(self, sql):
        self.mysql = sql

    def InsertUsers(self, username, password, email):
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO users(username,password,email) VALUES (% s, % s, % s)',
                       (username, password, email,))
        self.mysql.connection.commit()

    def InsertUserName(self, username):
        uname = session['username']
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE users SET username=% s WHERE username=%s',
                       (username, uname))
        session['username'] = username
        self.mysql.connection.commit()

    def InsertPassword(self, password):
        uname = session['username']
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE users SET password=% s WHERE username=%s',
                       (password, uname))
        self.mysql.connection.commit()

    def InsertEmail(self, email):
        uname = session['username']
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE users SET email=% s WHERE username=%s',
                       (email, uname))
        session['email'] = email
        self.mysql.connection.commit()

    def InsertFirstName(self, name):
        uname = session['username']
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE users SET first_name=% s WHERE username=%s',
                       (name, uname))
        session['first_name'] = name
        self.mysql.connection.commit()

    def InsertLastName(self, name):
        uname = session['username']
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE users SET last_name=% s WHERE username=%s',
                       (name, uname))
        self.mysql.connection.commit()

    def InsertCity(self, name):
        uname = session['username']
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE users SET city=% s WHERE username=%s',
                       (name, uname))
        self.mysql.connection.commit()

    def InsertGender(self, name):
        uname = session['username']
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE users SET gender=% s WHERE username=%s',
                       (name, uname))
        self.mysql.connection.commit()

    def InsertDOB(self, name):
        uname = session['username']
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE users SET dob=% s WHERE username=%s',
                       (name, uname))
        self.mysql.connection.commit()

    def InsertMartialStatus(self, name):
        uname = session['username']
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE users SET martial_status=% s WHERE username=%s',
                       (name, uname))
        self.mysql.connection.commit()

    def InsertAge(self, name):
        uname = session['username']
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE users SET age=% s WHERE username=%s',
                       (name, uname))
        self.mysql.connection.commit()

    def InsertPhone(self, name):
        uname = session['username']
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE users SET number=% s WHERE username=%s',
                       (name, uname))
        self.mysql.connection.commit()

    def InsertProfileImage(self, name):
        uname = session['username']
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE users SET url=% s WHERE username=%s',
                       (name, uname))
        self.mysql.connection.commit()

    def CheckForUser(self, username, password):
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password,))
        account = cursor.fetchone()
        return account

    def FetchUser(self, name):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM users where username=%s or first_name like %s", (name, '%' + name + '%',))
        data = cur.fetchall()
        cur.close()
        model_instances = []
        for row in data:
            user_instance = UserModel.UserModel(*row)
            model_instances.append(user_instance)
        return model_instances

    def FetchEveryUser(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM users")
        data = cur.fetchall()
        cur.close()
        model_instances = []
        for row in data:
            user_instance = UserModel.UserModel(*row)
            model_instances.append(user_instance)
        return model_instances

    def FetchSingleUser(self, name):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM users where username=%s", (name,))
        data = cur.fetchall()
        cur.close()
        for row in data:
            return UserModel.UserModel(*row)

    def InitializeSessionVar(self, username, password):
        account = Database(self.mysql).CheckForUser(username, password)
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            session['email'] = account['email']
            session['first_name'] = account['first_name']
            session['last_name'] = account['last_name']
            session['city'] = account['city']
            session['gender'] = account['gender']
            session['dob'] = account['dob']
            session['martial_status'] = account['martial_status']
            session['age'] = account['age']
            session['number'] = account['number']
            session['url'] = account['url']

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
            # file_instance.size = str(size)

            model_instances.append(file_instance)
        return model_instances

    def FetchFilesByUserRepo(self, username, repo):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM file_details where username=%s and repo_name=%s and mode='Public'",
                    (username, repo,))
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

    def FetchFilesByUserRepoAdmin(self, username, repo):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM file_details where username=%s and repo_name=%s",
                    (username, repo,))
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
        cur.execute("SELECT * FROM file_details where mode='Public'")
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

            size = int(file_instance.size)
            size = size / (1000 * 1000)
            file_instance.size = str(size) + " MB"

            model_instances.append(file_instance)
        return model_instances

    def FetchFilesByName(self, username, name, is_mine):
        cur = self.mysql.connection.cursor()
        if is_mine:
            cur.execute("SELECT * FROM file_details WHERE username = %s and repo_name LIKE %s",
                        (username, '%' + name + '%',))
        else:
            cur.execute("SELECT * FROM file_details WHERE repo_name LIKE %s and mode = 'Public' ", ('%' + name + '%',))
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

    def FetchFilesByPublicUser(self, username):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM file_details where username=%s and mode='Public'", (username,))
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

    def CreateAiMessage(self, message, isMine):
        username = session['username']
        if not isMine:
            username = username + "-ai"
        timestamp = time.time()
        cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''INSERT INTO ai_message(username,message,timestamp) VALUES 
                       (% s, % s, % s)''', (username, message, timestamp))
        self.mysql.connection.commit()

    def FetchAiMessages(self):
        username = session['username']
        cur = self.mysql.connection.cursor()
        cur.execute("select * from ai_message where username = %s or username = %s;", (username, username + "-ai",))
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
        print("deleted " + repo_name)
        self.mysql.connection.commit()

    def getDiscussionsTableCreationStatement():
        return ''' create table discussions(id int primary key auto_increment,username varchar(22),message text,timestamp varchar(22)); '''

    def getAiMessageTableCreationStatement():
        return ''' create table ai_message(id int primary key auto_increment,username varchar(22),message text,timestamp varchar(22)); '''

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
