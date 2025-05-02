from flask import Flask, request, redirect, session, render_template
import bcrypt
import os
import requests
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(16)
admin_token = os.urandom(16).hex()
user_token = os.urandom(16).hex()

DB_PATH = 'app.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')

    username = "a_retro_hero_fighting_80s_monster"
    uuid = "bdf7418a-8ec1-4624-a5fa-69d3f8d50abc"
    generated_password = username + ":" + uuid + ":" + generate_random_password()

    password_hash = bcrypt.hashpw(generated_password.encode(), bcrypt.gensalt()).decode('utf-8')


    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    if not cur.fetchone():
        cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))


    cur.execute("SELECT * FROM config WHERE key = 'API_AUTH'")
    if not cur.fetchone():
        api_auth_token = generate_random_password()
        cur.execute("INSERT INTO config (key, value) VALUES ('API_AUTH', ?)", (api_auth_token,))

    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def get_api_auth_token():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT value FROM config WHERE key = 'API_AUTH'")
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def set_api_auth_token(new_token):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("REPLACE INTO config (key, value) VALUES ('API_AUTH', ?)", (new_token,))
    conn.commit()
    conn.close()

def generate_random_password():
    with open("/dev/random", "rb") as f:
         password = f.read(64)
    return password.hex()


FLAG = "Securinets{FAKE_FLAG}"

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_input = request.form.get('username')
        password_input = request.form.get('password', '')

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT password_hash FROM users WHERE username = ?", (username_input,))
        user = cur.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password_input.encode(), user[0].encode()):
            session['user'] = username_input
            session['token'] = user_token
            return redirect('/')
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/gallery')
def gallery():
    token = request.args.get('token', '')
    if token != user_token:
        return redirect('/login')
    return render_template('gallery.html')

@app.route('/api/fetch')
def fetch():
    token = request.args.get('token', '')
    if token != user_token:
        return redirect('/login')
    url = request.args.get('url', '')
    try:
        res = requests.get(url, timeout=2)
        return res.text[:1000]
    except Exception as e:
        return f"Error: {e}"

@app.route('/api/setAuthorization')
def set_auth():
    if request.remote_addr != '127.0.0.1':
        return "Forbidden!"
   
    auth = request.args.get('auth')
    token = request.args.get('token')

    if not auth:
        return "Missing auth param"

    set_api_auth_token(auth)
    
    if token and token == admin_token:
        return "Succesfully update AUTH Token"
    else:
        api_auth = generate_random_password()
        set_api_auth_token(api_auth)
        return "Admin Token is not valid"

@app.route('/flag')
def flag():
    auth = request.args.get('auth', '')
    if auth == get_api_auth_token():
        return render_template('flag.html', secret=FLAG)
    else:
        return "Wrong Auth!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
