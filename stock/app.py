from flask import Flask, render_template, flash, request
import json
#from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import datetime as dt
import sys

mysql = MySQL()

app = Flask(__name__)


app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'stocks'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['MYSQL_DATABASE_PORT'] = 3307
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'

mysql.init_app(app)
app.config.from_object(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/Signup',methods=['POST','GET'])
def Signup():
     return render_template('signup.html')

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _phoneno = request.form['pno']
        _email = request.form['email']
        _password = request.form['password']

        print("working")
        if _phoneno and _email and _password :
            
            print("hi")
            conn = mysql.connect()            
            cursor = conn.cursor()
    #_hashed_password = generate_password_hash(_password)
            print ("don")
            cursor.callproc('sp_createUser',[_email,_password,_phoneno])
            data = cursor.fetchall()
            
            if len(data) is 0:
                print("yo")
                conn.commit()
                conn.close()
                
                return render_template('hello.html')
            else:
                conn.close()
                #return json.dumps({'error':str(data[0])})
                return render_template('wrong.html',variable=str(data[0]))
        else:
            
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        print ("goto")
        print (e)
        return json.dumps({'error':str(e)})
#    finally:
#        cursor.close() 
#        conn.close()

@app.route('/login',methods=['GET', 'POST'])
def login():
        return render_template('login.html')
@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
        email_form  = request.form['email']
        password_form  = request.form['password']
        conn = mysql.connect()
        cur = conn.cursor()        
        cur.execute("SELECT COUNT(1) FROM users WHERE email = %s;", [email_form]) # CHECKS IF USERNAME EXSIST
        if cur.fetchone()[0]:
            print("yes")
            cur.execute("SELECT password FROM users WHERE email = %s;", [email_form]) # FETCH THE HASHED PASSWORD
            data = cur.fetchone()[0]
            if str(password_form) == str(data):
                    print ("done")
                    flash("Login Successfull")
                    conn.close()
                    return render_template('home.html')
            else:
                    #return json.dumps({'error':str(data)})
                    conn.close()
                    return render_template('wrong.html',variable="wrong password or email")
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
              
@app.route('/index')
def index():
    return "home"
    #return redirect(url_for('login'))
        
@app.route('/company',methods = ['GET','POST'])
def company():
    company = request.form['company']

    conn = mysql.connect()
    cur = conn.cursor()
    print("hogo")
    cur.execute("select year_ from history where ID = %s;",[company])
    print ("yoyo")
    x= list()
    y = list(cur.fetchall())
    for i in range(cur.rowcount):
        x.append(y[i][0])
    cur.execute("select stock_price from history where ID = %s;",[company])
    y= list()
    z = list(cur.fetchall())
    for i in range(cur.rowcount):
        y.append(int(z[i][0])) 
    cur.execute("select * from company where ID=%s;",[company])
    data= list(cur.fetchall())
    
    print (data)
    print(x)
    print(y)
    table_data = zip(x,y)
    cur.execute('select stock_price from prediction where ID = %s;',[company])
    c = list()
    d= list (cur.fetchall())
    for q in range(cur.rowcount):
        c.append(d[q][0])
    
    return render_template('data.html',X=x,Y=y,d=data,t=table_data,p = c)


if __name__ == "__main__":    
    app.run(debug=True,port=8081)