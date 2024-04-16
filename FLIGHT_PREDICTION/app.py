
from flask import Flask, render_template, request, session, url_for, redirect,jsonify
from werkzeug.utils import secure_filename
import os
import pickle
from joblib import dump, load
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pymysql

# Import dataset 
df = pd.read_csv('Data/Processed_data15.csv')

# Label Encoding
le_carrier = LabelEncoder()
df['carrier'] = le_carrier.fit_transform(df['carrier'])

le_dest = LabelEncoder()
df['dest'] = le_dest.fit_transform(df['dest'])

le_origin = LabelEncoder()
df['origin'] = le_origin.fit_transform(df['origin'])

# Converting Pandas DataFrame into a Numpy array
X = df.iloc[:, 0:6].values # from column(years) to column(distance)
y = df['delayed']

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.25,random_state=61) # 75% training and 25% test

app = Flask(__name__)
model = load(open('model.pkl', 'rb'))
app.secret_key = 'random string'
def dbConnection():
    try:
        connection = pymysql.connect(host="localhost", user="root", password="root", database="androiddb",charset='utf8' ,port=3306)
        return connection
    except:
        print("Something went wrong in database Connection")

def dbClose():
    try:
        dbConnection().close()
    except:
        print("Something went wrong in Close DB Connection")

con=dbConnection()
cursor=con.cursor()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

##########################################################################################################
#                                               Login
##########################################################################################################
@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'] 

        print(email,password)

        con = dbConnection()
        cursor = con.cursor()
        result_count = cursor.execute('SELECT * FROM userdetails WHERE email = %s AND password = %s', (email, password))
        result = cursor.fetchone()
        print("result")
        print(result)
        if result_count>0:
            print("len of result")
            session['username'] = result[1]
           
            return redirect(url_for('home'))
        else:
            FinalMsg = "Wrong username an password Please Try Again!"
            return render_template('login.html',FinalMsg=FinalMsg)
    return render_template('login.html')

##########################################################################################################
#                                           Register
##########################################################################################################
@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        print("hii register")
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        mobile = request.form['mobile']

        print(email,password,username)

        try: 
            con = dbConnection()
            cursor = con.cursor()
            sql1 = "INSERT INTO userdetails (username, email, mobile, password) VALUES (%s, %s, %s, %s)"
            val1 = (username, email,mobile,password)
            cursor.execute(sql1, val1)
            print("query 1 submitted")
            con.commit()
            FinalMsg = "Congrats! Your account registerd successfully!"
        except:
            con.rollback()
            msg = "Database Error occured"
            print(msg)
            return render_template("register.html", FinalMsg=msg)
        finally:
            dbClose()
        return render_template("register.html",FinalMsg=FinalMsg)
    return render_template("register.html")
##########################################################################################################
#                                               Login
##########################################################################################################

@app.route('/home')
def home():
    if 'username' in session:
     return render_template('main.html')

##########################################################################################################
#                                       Prediction
##########################################################################################################
@app.route('/predict',methods=['POST'])
def predict():
    year = request.form['year']
    month = request.form['month']
    day = request.form['day']
    carrier = request.form['carrier']
    origin = request.form['origin']
    dest = request.form['dest']
    
    print(year,month,day,origin,carrier,dest)
    year = int(year)
    month = int(month)
    day = int(day)
    carrier = str(carrier)
    origin = str(origin)
    dest = str(dest)
    
    if year >= 2013:
        x1 = [year,month,day]
        x2 = [carrier, origin, dest]
        x1.extend(x2)
        df1 = pd.DataFrame(data = [x1], columns = ['year', 'month', 'date', 'carrier', 'origin', 'dest'])
        
        df1['carrier'] = le_carrier.transform(df1['carrier'])
        df1['origin'] = le_origin.transform(df1['origin'])
        df1['dest'] = le_dest.transform(df1['dest'])
        
        x = df1.iloc[:, :6].values
        
        ans = model.predict(x)
        print("---------------------------")
        print(ans)
        print("---------------------------")

        output = ans
    # return render_template('index.html')
    return render_template('main.html', prediction_text=output)

@app.route("/logout", methods = ['POST', 'GET'])
def logout():
    session.pop('username',None)
    return redirect(url_for(''))
    
if __name__ == '__main__':
    
 	app.run("0.0.0.0")
    # app.run(debug=True)
