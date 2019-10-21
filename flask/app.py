from flask import Flask, jsonify, render_template
from flask.views import MethodView
from flask_simplelogin import SimpleLogin, get_username, login_required
import os
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

my_users = {
    'Teacher': {'password': 'teacher', 'roles': ['admin']},
    'vishal': {'password': 'vishal', 'roles': []},
    'rishav': {'password': 'rishav', 'roles': []},
    'anuj': {'password': 'anuj', 'roles': []},
   
}


def check_my_users(user):
    """Check if user exists and its credentials.
    Take a look at encrypt_app.py and encrypt_cli.py
     to see how to encrypt passwords
    """
    user_data = my_users.get(user['username'])
    if not user_data:
        return False  # <--- invalid credentials
    elif user_data.get('password') == user['password']:
        return True  # <--- user is logged in!

    return False  # <--- invalid credentials

PEOPLE_FOLDER = os.path.join('static', 'people_photo')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
app.config['SECRET_KEY'] = 'secret-here'


SimpleLogin(app, login_checker=check_my_users)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/secret')
@login_required(username=['vishal', 'rishav','anuj'])
def secret():
    user_data = get_username()
    f = open("static/CSV/"+user_data+".csv","r")
    k = f.readlines()
    Subject = ["SB","BA","BB","ACJ","SM","MC"]
    objects = ["SB","BA","BB","ACJ","SM","MC"]
    Total = [0]*6
    Present = [0]*6
    Att = list()

    for i in k:
        a = i.split(",")
        b = a[1].split(" ")
        c = a[2].split(" ")
        
        for j in range(0,6):
            for l in b:
                if(Subject[j] == l):
                    Total[j] = Total[j]+1

            for m in c:
                if(Subject[j] == m):
                    Total[j] = Total[j]+1
                    Present[j] = Present[j]+1


    for i in range(0,6):
        a = Present[i]/Total[i]
        a = a*100
        a = int(a)
        objects[i] = objects[i]+" "+str(a)
        Att.append(a)

    y_pos = np.arange(len(objects))
    plt.bar(y_pos, Att, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Attendance')
    plt.title('Subject')

    plt.savefig("static/people_photo/"+user_data+"1.jpg")
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], user_data+'1.jpg')

    return render_template('secret.html', user_image = full_filename)


@app.route('/api', methods=['POST'])
@login_required(basic=True)
def api():
    return jsonify(data='You are logged in with basic auth')


def be_admin(username):
    """Validator to check if user has admin role"""
    user_data = my_users.get(username)
    if not user_data or 'admin' not in user_data.get('roles', []):
        return "User does not have admin role"


def have_approval(username):
    """Validator: all users approved, return None"""
    return


@app.route('/complex')
@login_required(must=[be_admin, have_approval])
def complexview():
    
    
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'vishal.jpg')
    return render_template('secret1.html', user_image = full_filename)


class ProtectedView(MethodView):
    decorators = [login_required]

    def get(self):
        return "You are logged in as <b>{0}</b>".format(get_username())


app.add_url_rule('/protected', view_func=ProtectedView.as_view('protected'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, use_reloader=True, debug=True)
