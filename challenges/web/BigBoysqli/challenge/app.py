from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import hashlib
import os
from utils import generate,hash_password,banned_list

app = Flask(__name__)
app.secret_key = generate(60)


FLAG = os.getenv('FLAG')

def init_db():
    try:
        os.remove('CTF.db')
    except:
        pass
    conn = sqlite3.connect('CTF.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logging (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flags (
            id INTEGER PRIMARY KEY,
            flag TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_flag(flag):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO flags (flag) VALUES (?)', (flag,))
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS prevent_update
        BEFORE UPDATE ON flags
        BEGIN
            SELECT RAISE(FAIL, "Don't touch the Flag troll");
        END;
         ''')
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS prevent_insert
        BEFORE INSERT ON flags
        BEGIN
            SELECT RAISE(FAIL, "Don't touch the Flag troll");
        END;
         ''')
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS prevent_delete
        BEFORE DELETE ON flags
        BEGIN
            SELECT RAISE(FAIL, "Don't touch the Flag troll");
        END;
         ''')
    conn.commit()
    conn.close()


def add_user(username,email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute('INSERT INTO users (username,email, password) VALUES (?,?, ?)', (username,email, hashed_password))
    conn.commit()
    conn.close()
    
def reset_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users;')
    conn.commit()
    conn.close()


init_db()

def get_db_connection():
    conn = sqlite3.connect('CTF.db')
    conn.row_factory = sqlite3.Row
    return conn


def add_admin():
    add_user("admin","admin@admin.cfg",hash_password(generate(30)))

add_admin()
add_flag(FLAG)


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
       try: 
        username = request.form['username']
        password = request.form['password']
        if any(banned in username.lower() for banned in banned_list):
            return render_template('login.html', error='Invalid username or password')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.executescript(f'''
                             INSERT INTO logging (username) VALUES ('{username}');
                             
                             ''')
        conn.close()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f'SELECT username,email,password FROM users WHERE username ="{username}"')
        user = cursor.fetchone()
        conn.close()
        reset_users()
        add_admin()
        if user and user['password'] == hash_password(password):
            session['username'] = user['username']
            session['email'] = user['email']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')
       except:
           return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        email = session['email']
        return render_template('dashboard.html', user=username,email=email)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()