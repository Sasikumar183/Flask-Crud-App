from flask import Flask,render_template,url_for,request,redirect,flash
from flask_mysqldb import MySQL
app=Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin@123'
app.config['MYSQL_DB'] = 'employee'
app.config['MYSQL_CURSORCLASS']='DictCursor'

# Initialize MySQL
mysql = MySQL(app)

@app.route('/')

def home():
    con=mysql.connection.cursor() 
    sql="SELECT * FROM details" 
    con.execute(sql)
    res=con.fetchall()
    mysql.connection.commit()
    con.close()
    return render_template("index.html",datas=res)

@app.route('/adminuser',methods=['GET','POST'])

def createuser():
    if request.method=='POST':
        fname=request.form['fname']
        lname=request.form['lname']
        city=request.form['city']
        con=mysql.connection.cursor()
        sql="insert into details(firstname,lastname,city) values(%s,%s,%s)"
        con.execute(sql,[fname,lname,city])
        mysql.connection.commit()
        con.close()
        flash('User Added Successfully')
        return redirect(url_for('home'))
    return render_template('adduser.html')

@app.route('/edituser/<string:id>',methods=['GET','POST'])

def editdetails(id):
    if request.method=='POST':
        fname=request.form['fname']
        lname=request.form['lname']
        city=request.form['city']
        con=mysql.connection.cursor()
        sql="update details set firstname=%s,lastname=%s,city=%s where id=%s"
        con.execute(sql,[fname,lname,city,id])
        mysql.connection.commit()
        con.close()
        flash('User Details Updated Successfully')
        return redirect(url_for('home'))
    con=mysql.connection.cursor()
    sql="select * from details where id=%s"
    con.execute(sql,[id])
    res=con.fetchone()
    return render_template('edituser.html',datas=res)

@app.route('/deleteuser/<string:id>',methods=['GET','POST'])

def deletedetails(id):
    con=mysql.connection.cursor()
    sql="delete from details where id=%s"
    con.execute(sql,[id])
    mysql.connection.commit()
    con.close()
    flash('User Details Deleted Successfully')
    return redirect(url_for('home'))
    

    
if __name__=='__main__':
    app.secret_key = 'your_secret_key'
    app.run(debug=True)