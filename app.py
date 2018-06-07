from flask import Flask, render_template, request, json
# from flask.ext.mysql import MySQL
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask_cors import CORS, cross_origin

print('app start')
app = Flask(__name__)
CORS(app)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'xxxxx'
app.config['MYSQL_DATABASE_DB'] = 'bucketlist'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST'])
def signUp():
    # try:
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    # validate the received values
    if _name and _email and _password:
    #     # All Good, let's call MySQL
        conn = mysql.connect()
        cur = conn.cursor()

        if checkExist(cur,_email) is 'True':
            return json.dumps({'html': '<span>Your account has been registered here</span>'})
        else:
            print('---- Create your account ----')
            _hashed_password = generate_password_hash(_password)

            cur.execute('''INSERT INTO tbl_user (user_username, user_email, user_password) VALUES ("%s","%s","%s")''' % (_name,_email,_hashed_password))
            conn.commit()
            cur.close()
            conn.close()

            return json.dumps({'message': 'User created successfully !'})

    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})


def checkExist(cur, email):
    print('check your existance')
    cur.execute('''SELECT * FROM tbl_user where user_email = "%s" ''' % email)
    res = cur.fetchone()
    return 'True' if res else 'False'

if __name__ == "__main__":
    app.run( host='0.0.0.0', port = 5000, debug = True )
