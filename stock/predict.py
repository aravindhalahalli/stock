import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from flaskext.mysql import MySQL
from flask import Flask, render_template, flash, request
from sklearn.preprocessing import PolynomialFeatures
import datetime as dt
from sklearn.svm import SVR
from pandas import Timestamp

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



@app.route('/predict',methods=["GET","POST"])
def predict():
    #c = reequest.form['company']
    conn = mysql.connect()            
    cur = conn.cursor()
    company = "1"
    cur.execute("select stock_price from history where ID = %s;",[company])
    x= list()
    y= list()
    z= list (cur.fetchall())
    
    for i in range(cur.rowcount):
        x.append(z[i][0] )
   
    cur.execute("select Turn_over,GDP,sensex from history,market  where history.year_=market.year_ and history.ID=%s order by history.year_",[company])
    z= list(cur.fetchall())
    t=0
    for i in range(cur.rowcount):
        y.append([z[i][0],z[i][1],z[i][2]])
        t=z[i][0]
    y=y[1:]
    t = t * 1.2
    print (t)
    #poly = PolynomialFeatures(degree=3)
    #y = poly.fit_transform(y)
    
    y_test_ = [[t,6.1,32480],[t,6.1,33690],[t,6.1,32330],[t,7.5,31760],[t,7.5,30843],[t,7.5,32747]]
    #y_test_ = poly.fit_transform(y_test_)
    poly = PolynomialFeatures(degree=3)
    Y = poly.fit_transform(y)
    y_ = poly.fit_transform(y_test_)
    clf = linear_model.LinearRegression()
    clf.fit(y, x)
    X= clf.predict(y_test_)
    dat = ['2018-01-01','2018-02-01','2018-03-01','2018-04-01','2018-05-01','2018-06-01']
    print (X)
    for i in  range(len(dat)):
        
        cur.execute('insert into prediction(ID,year_,stock_price) values(%s,%s,%s);',[company,dat[i],str(X[i])])    
    #return render_template('predict.html',x_=X,Y=y_test_)
    conn.commit()
    conn.close()
    return "goto"

if __name__ == "__main__":    
    app.run(debug=True,port=8083)