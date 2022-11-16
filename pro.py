from sqlite3 import Cursor
from urllib import response

from flask import Flask,render_template,request,make_response
import pdfkit
import mysql.connector
import os

cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='usdetail')
msq=cnx.cursor(buffered=True)
app=Flask(__name__,template_folder='template')

@app.route('/')
def info():
    return render_template('home.html')
@app.route('/index',methods=['post','get'])
def index():
    return render_template('signup2.html')
@app.route('/adlogin1',methods=['post','get'])
def adlogin1():
    return render_template('adlogin.html')

@app.route('/signup2',methods=['post','get'])
def signup2():
    error=""
    error1=""
    k=[]
    if request.method=='POST':
        name=request.form.get('name')
        pno=request.form.get('pno')
        sno=request.form.get('sno')
        pas=request.form.get('ps')
        snot="`"+str(sno)+"`"
        print(sno)
        seno="`"+str(sno)+"`"
        print(seno)
        if len(name)<1:
            error="please enter the name"
        elif len(pno)<10:
            error="invalid phone number"
        elif len(pas)<6:
            error="your password should have above 6 characters"
        else:
            
            querry="insert into usregister2(servicenumber,username,phonenumber,password1) values (%s,%s,%s,%s)"
            msq.execute(querry,(sno,name,pno,pas))
            cnx.commit()
            error1="Your account created"
    if error:
        return render_template('signup2.html',err=error)
    else:
        return render_template('info.html',err=error,k=k)
k1=[]
k3=[]
@app.route('/Login1',methods=['post','get'])
def Login1():
    global k1
    global k3
    querry=""
    if request.method=='POST':
        sno=request.form.get('sno')
        pas=request.form.get('ps')
        msq.execute('SELECT * FROM usregister2 WHERE servicenumber = %s AND password1 = %s', (sno, pas))
        # Fetch one record and return result
        querry = msq.fetchall()
        print(tuple(querry))
        cnx.commit()
        if querry:
            msg1='select * from billdetails3 where servicenumber = %s'
            msq.execute(msg1,(sno,))
            
            k1=msq.fetchall()
            print(k1)
            cnx.commit()
            return render_template("result.html",k=k1)
        else:
            print("1")
    return render_template('Login1.html')
@app.route('/adlogin',methods=['post','get'])
def adlogin():
    querry=0
    k1=[]
    if request.method=='POST':
        sno=request.form.get('sno')
        pas=request.form.get('ps')
        if pas=="ranjith" and sno=="635305":
            querry=1
        else:
            querry=0
       
        if querry:
            msg1='select * from billdetails3'
            msq.execute(msg1)
            k1=msq.fetchall()
            print(k1)
            cnx.commit()
            return render_template("adresult.html",k=k1)
        else:
            print("1")
    return render_template('adlogin.html')
@app.route('/pdf',methods=['post','get'])
def pdf():
    l=[]
    l1=[]
    se=k1[0][1]
    for i in k1:
        l.append(int(i[2]))
        l1.append(float(i[3]))
    a=sum(l)
    b=int(sum(l1))
    msg='select servicenumber,username,phonenumber from usregister2 where servicenumber = %s'
    msq.execute(msg,(se,))
        # Fetch one record and return result
    c = msq.fetchall()
    cnx.commit()
    rendered=render_template("pdf.html",p=a,q=b,r=c)
    pdf = pdfkit.from_string(rendered, False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=billdetails.pdf"
    return response
@app.route('/ad',methods=['post','get'])
def ad():
    querry=""
    if request.method=='POST':
        sno=request.form.get('sno')
        msg='SELECT * FROM usregister2 WHERE servicenumber = %s'
        msq.execute(msg,(sno,))
        # Fetch one record and return result
        querry = msq.fetchall()
        print(tuple(querry))
        cnx.commit()
        if querry:
            msg1='select * from billdetails3 where servicenumber = %s'
            msq.execute(msg1,(sno,))
            
            k1=msq.fetchall()
            print(k1)
            cnx.commit()
            return render_template("adresult.html",k=k1)
        else:
            print("1")
    return render_template('Login1.html')

    

if __name__=="__main__":
    app.run(debug=True,port=8080,use_reloader=False)