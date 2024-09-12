from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages
import mysql.connector
import re
import bcrypt
import os
import datetime

app = Flask(__name__, template_folder='templates')
app.secret_key = 'il_tuo_segreto'



# Configurazione del database MySQL
db_config = {
    'host': os.getenv('MYSQL_HOST', '192.168.178.162'),
    'port': os.getenv('MYSQL_PORT', '3308'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'my-secret-pw'),
    'database': os.getenv('MYSQL_DATABASE', 'asset_management')
}

def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

@app.route('/info')
def info():
    email = request.args.get('email')

    # Se l'email è fornita nella richiesta, salvala nella sessione
    if email:
        session['email'] = email
    elif 'email' in session:
        email = session['email']
    else:
        flash('Email non fornita.')
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Recupera tutte le informazioni del dipendente
    cursor.execute('SELECT * FROM dipendenti WHERE email = %s', (email,))
    dipendente = cursor.fetchone()

    cursor.close()
    conn.close()

    if dipendente:
        return render_template('info.html', dipendente=dipendente, email=email)
    else:
        flash('Dipendente non trovato.')
        return redirect('/')


@app.route('/')
def index():
    if 'loggedin' in session:
        app.logger.debug('User is logged in, redirecting to home page.')
        return redirect('http://192.168.178.162:14000/home?email=' + session['email'])
    app.logger.debug('User not logged in, rendering login page.')
    return redirect('http://192.168.178.162:13000/')

@app.route('/register_redirect')
def register_redirect():
    if 'loggedin' in session:
        app.logger.debug('User is logged in, redirecting to home page.')
        return redirect('http://192.168.178.162:11000/register?email=' + session['email'])
    app.logger.debug('User not logged in, rendering login page.')
    return redirect('http://192.168.178.162:13000/')



@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    return redirect('http://192.168.178.162:13000/')  # Reindirizza alla pagina di login dell'app di login

    
  


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=18000)
