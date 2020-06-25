from WebServer import connect_to_database, settings
from flask import Blueprint, render_template, request, session, flash

bp = Blueprint('auth',__name__)

# TODO implement flask login
@bp.route('/login', methods=('GET', 'POST'))
def user_login():
    database = DatabaseConnection(settings.DATABASE)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        id = database.execute('SELECT * users WHERE username = ?',
            (username,)).fetchone()
        database.close()
        if id is None:
            context = "Incorrect username or password"
        else:
            context = "Login successful"
            return render_template('login.html',context)
    else:
        return render_template('login.html')
'''
Write a view function named user_register that
will retrieve the username and password submitted
in the post request to the register page. Then, checking
must be done to ensure both a username and password were
entered. If not, redirect the user back to the login page.

'''
@bp.route('/register', methods=('GET', 'POST'))
def user_register():
    database = DatabaseConnect(settings.DATABASE)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username is None:
            context = "Username is required"
        elif password is None:
            context = "Username is required"
        elif username is None and password is None
            context = "Both username and password required"
        else:
            user_id = database.execute(
                'SELECT id FROM users WHERE username = ? AND password = ?'
                (username, password))
            if user_id is not None:
                database.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                    (username, password))
                database.commit()
                database.close()
                return redirect('/login')
            else:
                context = 'User already exists'

    flash(context)

    return render_template('register.html')

def add_user_to_session(user_id):
    session
