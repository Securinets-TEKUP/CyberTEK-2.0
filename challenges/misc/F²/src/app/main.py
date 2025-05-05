from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    filename = request.args.get('f')
    if filename:
        try:
            with open(filename, 'r') as f:     
                return f"<pre>{f.read()}</pre>"
        except Exception as e:
            return f"<p>Error: {e}</p>"        
    return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337)