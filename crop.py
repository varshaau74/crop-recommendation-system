import pickle

from flask import Flask,render_template,request,flash
from flask_mysqldb import MySQL
import numpy as np
import requests

app=Flask(__name__)
app.secret_key= 'dont tell anyone'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='crop'

mysql=MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home1')
def home1():
    return render_template('home1.html')

@app.route('/aboutproject')
def aboutproject():
    return render_template('aboutproject.html')

@app.route('/adminhome')
def adminhome():
    return render_template('adminlayout.html')

@app.route('/crop',methods=['GET','POST'])
def crop():
    r=[]
    if request.method=='POST':
        longitude=request.form['longitude']
        latitude=request.form['latitude']
        print(longitude,latitude)

        p1 = {"lat": longitude, "lon": latitude}
        rest_url = "https://rest.isric.org"
        prop_query_url = f"{rest_url}/soilgrids/v2.0/properties/query"

        props = {"property": "silt", "depth": "0-5cm", "value": "mean"}
        res1 = requests.get(prop_query_url, params={**p1, **props})
        # print(res1)
        print(res1.json()['properties']["layers"][0]["depths"][0]["values"])

        res = res1.json()['properties']["layers"][0]["depths"][0]["values"]

        print("Silt = {}".format(res["mean"] / 10))

        silt = res["mean"] / 10

        props = {"property": "sand", "depth": "0-5cm", "value": "mean"}
        res1 = requests.get(prop_query_url, params={**p1, **props})
        # print(res1)
        print(res1.json()['properties']["layers"][0]["depths"][0]["values"])

        res = res1.json()['properties']["layers"][0]["depths"][0]["values"]

        print("Sand = {}".format(res["mean"] / 10))

        sand = res["mean"] / 10

        props = {"property": "phh2o", "depth": "0-5cm", "value": "mean"}
        res1 = requests.get(prop_query_url, params={**p1, **props})
        # print(res1)
        print(res1.json()['properties']["layers"][0]["depths"][0]["values"])

        res = res1.json()['properties']["layers"][0]["depths"][0]["values"]

        print("Ph = {}".format(res["mean"] / 10))

        ph = res["mean"] / 10

        props = {"property": "clay", "depth": "0-5cm", "value": "mean"}
        res1 = requests.get(prop_query_url, params={**p1, **props})
        # print(res1)
        print(res1.json()['properties']["layers"][0]["depths"][0]["values"])

        res = res1.json()['properties']["layers"][0]["depths"][0]["values"]
        print("clay = {}".format(res["mean"] / 10))

        clay = res["mean"] / 10

        props = {"property": "nitrogen", "depth": "0-5cm", "value": "mean"}
        res1 = requests.get(prop_query_url, params={**p1, **props})
        # print(res1)
        print(res1.json()['properties']["layers"][0]["depths"][0]["values"])

        res = res1.json()['properties']["layers"][0]["depths"][0]["values"]

        print("nitrogen = {}".format(res["mean"] / 10))

        nitrogen = res["mean"] / 10

        data = np.array([[ph]])

        print("data1 = ", data)
        # data = np.array([[6.23,2.10,22.0,34,5.0]])

        print("data = ", data)
        # data = np.array([[6.23,2.10]])
        file = open("Knnnew.pkl", 'rb')
        object_file = pickle.load(file)
        prediction = object_file.predict(data)
        print("Recomended crop is = ", prediction[0])

        d = {"silt": silt, "sand": sand, "ph": ph, "clay": clay, "nitrogen": nitrogen, "lang": longitude, "lat": latitude,
             "crop": prediction[0]}
        return render_template('result.html',data=d)
    else:
        return render_template('longitude.html')

@app.route('/login',methods=['GET','POST'])
def login():
    trace=[]
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("select * from register where user_id='"+username+"' and password='"+password+"'")
        trace = cur.fetchone()
        print(trace)
        if cur.rowcount>0:
            #flash('LOGIN SUCCESSFULL')
            #return render_template('longitude.html')
            rec=list(trace)

            if rec[6]=='0':
                flash('NOT YET APPROVED')
                return render_template('login.html')
            else:
                return render_template('longitude.html')
        else:
            flash("INCORRECT PASSWORD OR USERNAME")
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/forget',methods=['GET','POST'])
def forget():
    trace=[]
    if request.method == 'POST':
        sque = request.form['sque']
        ans = request.form['ans']
        cur = mysql.connection.cursor()
        cur.execute("select * from register where sque='" + sque + "' and ans='" + ans + "'")
        trace = cur.fetchone()
        print(trace)
        rec=list(trace)
        msg="your password is:"+rec[5]

        if cur.rowcount > 0:
            flash(msg)
            return render_template('login.html')
        else:
            flash("INCORRECT SQUE OR ANS")
            return render_template('forget.html')
    else:
        return render_template('forget.html')

@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        print(name,password)
        if name=="varsha" and password=="1234":
            #flash("WELCOME TO CROP RECOMANDED SYSTEM")
            return render_template('index.html')
        else:
            flash("login failed")
            return render_template('adminlogin.html')
    else:
        return render_template('adminlogin.html')


@app.route('/registration',methods=['GET','POST'])
def registration():
    if request.method=='POST':
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        contact_no= request.form['contact_no']
        user_id = request.form['user_id']
        address = request.form['address']
        password= request.form['password']
        sque=request.form['sque']
        ans = request.form['ans']
        cur=mysql.connection.cursor()
        cur.execute("insert into register(first_name,last_name,contact_no,user_id,address,password,sque,ans,status) values (%s,%s,%s,%s,%s,%s,%s,%s,'0')",(first_name,last_name,contact_no,user_id,address,password,sque,ans))
        mysql.connection.commit()
        cur.close()
        flash('Registration Successfull')
    return render_template('registration.html')

@app.route('/viewusers')
def display():
    trace=[]
    cur = mysql.connection.cursor()
    cur.execute("select * from register")
    trace=cur.fetchall()
    print(trace)
    return render_template('viewusers.html',recs=trace)

@app.route('/approve')
def approve():
    val=request.args.get('id')
    print(val)
    cur=mysql.connection.cursor()
    cur.execute("update register set status='1' where user_id='"+val+"'")
    cur.connection.commit()
    msg="<center><h1>User named "+val+" got approved</h1><br/><a href='/viewusers'>View here</a></center>"
    return (msg)

@app.route('/feedback',methods=['GET','POST'])
def feedback():
    if request.method=='POST':
        name=request.form['name']
        feedback=request.form['feedback']
        cur=mysql.connection.cursor()
        cur.execute("insert into feedback(name,feedback) values (%s,%s)",(name,feedback))
        mysql.connection.commit()
        cur.close()
        flash('THANK YOU')
        return render_template('empty.html')
    else:
        return render_template('feedback.html')


@app.route('/viewfeedback')
def viewfeedback():
    rec=[]
    cur = mysql.connection.cursor()
    cur.execute("select * from feedback")
    rec=cur.fetchall()
    print(rec)
    return render_template('viewfeedback.html',recs=rec)



if __name__=='__main__':
    app.run(debug=True)

