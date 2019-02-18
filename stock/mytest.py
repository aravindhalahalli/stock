import pymysql.cursors
from flask import Flask, render_template, flash, request
import json
import sys



# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='stocks',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

#try:
    #with connection.cursor() as cursor:
        # Create a new record
#        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
#        cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    #connection.commit()

    
@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/Signup')
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
#            conn = mysql.connect()            
            cursor = connection.cursor()
    #_hashed_password = generate_password_hash(_password)
            print ("don")
            cursor.callproc('sp_createUser',[_email,_password,_phoneno])
            data = cursor.fetchall()
            
            if len(data) is 0:
                print("yo")
#                conn.commit()
#                conn.close()
#                
                return 'User created successfully !'
            else:
                conn.close()
                return json.dumps({'error':str(data[0])})
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
            cur.execute("SELECT pass FROM users WHERE name = %s;", [email_form]) # FETCH THE HASHED PASSWORD
            data = cur.fetchall()
            if password_form == data[0]:
                    flash("Login Successfull")
                    return render_template('hello.html')
            else:
                    return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
              
@app.route('/index')
def index():
    return "home"
    #return redirect(url_for('login'))
        
        
if __name__ == "__main__":    
    app.run(debug=True,port=8081)    
    
    
    
    
    
#    with connection.cursor() as cursor:
#        # Read a single record
#        sql = "SELECT * FROM `users`"
#        cursor.execute(sql)
#        result = cursor.fetchone()
#        print(result)
#finally:
#    connection.close()