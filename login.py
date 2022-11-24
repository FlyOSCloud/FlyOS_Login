# FlyOS Cloud Project GPL-3.0 LICENSE
# login.py creator: Edward Hsing
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, login_required, UserMixin, login_user, logout_user
import uuid
from werkzeug.security import generate_password_hash
import os


from gevent import pywsgi
# for sqlite
import sqlite3
conn = sqlite3.connect('flyos.db')
cs = conn.cursor()
try:
    cs.execute('''CREATE TABLE user
        (id varchar(20) PRIMARY KEY,
            name varchar(20),
            password varchar(20)
            );''')
except:
    pass
cs.execute("REPLACE INTO user (id, name, password) VALUES ('1', 'admin', '123456')")
cs.execute("REPLACE INTO user (id, name, password) VALUES ('2', 'admin1', '123456')")
conn.commit()
cs.close()
conn.close()

from werkzeug.security import check_password_hash
def checkuser(username, password):
        conn = sqlite3.connect('flyos.db')
        cs = conn.cursor()
        cursor = cs.execute(f"select * from user where name='{username}';")
        print(cursor)
        for row in cursor:
            uid = row[0]
            getusername = row[1]
            getpassword = row[2]
        cs.close()
        conn.close()
        try:
            if getusername == username:
                if getpassword == password:
                    return True
        except:
            return None
        else:
            return None
class User(UserMixin):
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return "1"

# end flyos user init

app = Flask(__name__)

app.secret_key = os.urandom(24) # protect flyos
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user = User()
    return user
@app.route('/')
@login_required
def panelmain():
    return render_template('./main.html',username=user_name)
@app.route('/login', methods=['GET', 'POST'])
def login():
    global user_name
    if request.method == 'POST':
        user_name = request.form.get('username')
        password = request.form.get('password')
        print(user_name + password)
        user = User()
        if user_name == '':
            return 'Incorrect username or password'
        if password == '':
            return 'Incorrect username or password'
        if checkuser(user_name, password):
            login_user(user)
            return redirect(url_for('panelmain'))
        return 'Incorrect username or password'
        

    return render_template('./login.html')
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
