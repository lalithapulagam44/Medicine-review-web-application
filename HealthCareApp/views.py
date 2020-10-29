from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
import time
import datetime
import smtplib
from email.message import EmailMessage

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def SetReminder(request):
    if request.method == 'GET':
       return render(request, 'SetReminder.html', {})

def ViewMedicineDetails(request):
    if request.method == 'GET':
       return render(request, 'ViewMedicineDetails.html', {})

def ViewMap(request):
    if request.method == 'GET':
        lat = request.GET['lat']
        lon = request.GET['lon']
        html = ''
        html+='<input type=\"hidden\" name=\"t1\" id=\"t1\" value='+lat+'>'
        html+='<input type=\"hidden\" name=\"t2\" id=\"t2\" value='+lon+'>'
        context= {'data':html}
        return render(request, 'ViewMap.html', context)

def ViewMedicineDetailsAction(request):
    if request.method == 'POST':
        name = request.POST.get('t1', False)
        output = ''
        con = pymysql.connect(host='127.0.0.1',port = 3308,user = 'root', password = 'root', database = 'HealthCareDB',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM medicinedetails where medicine_name='"+name+"'")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size=3 color=black>'+row[0]+'</font></td>'
                output+='<td><font size=3 color=black>'+row[1]+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[2])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[3])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[4])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[5])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[6])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[7])+'</font></td>'
                output+='<td><a href=\'ViewMap?lat='+str(row[6])+"&lon="+str(row[7])+'\'><font size=3 color=black>Click Here</font></a></td></tr>'
        context= {'data':output}
        return render(request, 'ViewMedicineDetailsPage.html', context)      
    


def ViewPatientRequest(request):
    if request.method == 'GET':
        user = ''
        output=''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        con = pymysql.connect(host='127.0.0.1',port = 3308,user = 'root', password = 'root', database = 'HealthCareDB',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM  prescription where doctor_name='"+user+"' and prescription='none'")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size=3 color=black>'+row[0]+'</font></td>'
                output+='<td><font size=3 color=black>'+row[1]+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[2])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[3])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[4])+'</font></td>'
                output+='<td><a href=\'SendPrescription?id='+str(row[0])+'\'><font size=3 color=black>Click Here</font></a></td></tr>'
        context= {'data':output}
        return render(request, 'ViewPatientRequest.html', context)     
    

def ViewReminder(request):
    if request.method == 'GET':
        user = ''
        output = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        con = pymysql.connect(host='127.0.0.1',port = 3308,user = 'root', password = 'root', database = 'HealthCareDB',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM reminder where patient_name='"+user+"'")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size=3 color=black>'+row[0]+'</font></td>'
                output+='<td><font size=3 color=black>'+row[1]+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[2])+'</font></td>'
        print(output)        
        context= {'data':output}
        return render(request, 'ViewReminder.html', context)              

def SetReminderAction(request):
    if request.method == 'POST':
        dd = time.strftime('%Y-%m-%d %H:%M:%S')
        details = request.POST.get('t1', False)
        reminder_time = request.POST.get('t2', False)
        tt = str(datetime.datetime.strptime(reminder_time, "%d-%m-%Y %H:%M:%S").strftime("'%Y-%m-%d %H:%M:%S'"))
        print(tt)
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        db_connection = pymysql.connect(host='127.0.0.1',port = 3308,user = 'root', password = 'root', database = 'HealthCareDB',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO reminder(patient_name,reminder_details,reminder_time) "
        student_sql_query+="VALUES('"+user+"','"+details+"',"+tt+")"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        context= {'data':'Reminder set successfully'}
        return render(request, 'SetReminder.html', context)        
    

def MedicineDetails(request):
    if request.method == 'GET':
       return render(request, 'MedicineDetails.html', {})

def SendQuery(request):
    if request.method == 'GET':
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        strs = '<tr><td><b>Patient&nbsp;Name</b></td><td><input type=\"text\" name=\"t1\" size=\"30\" value='+user+' readonly/></td></tr>'
        strs+='<tr><td><b>Choose&nbsp;Doctor</b></td><td><select name="t2">'
        con = pymysql.connect(host='127.0.0.1',port = 3308,user = 'root', password = 'root', database = 'HealthCareDB',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username FROM register where usertype='Doctor'")
            rows = cur.fetchall()
            for row in rows:
                strs+='<option value='+row[0]+'>'+row[0]+'</option>'
        context= {'data1':strs}
        return render(request, 'SendQuery.html', context)        
        
def SendQueryRequest(request):
    if request.method == 'POST':
        dd = str(time.strftime('%Y-%m-%d %H:%M:%S'))
        patient = request.POST.get('t1', False)
        doctor = request.POST.get('t2', False)
        query = request.POST.get('t3', False)
        db_connection = pymysql.connect(host='127.0.0.1',port = 3308,user = 'root', password = 'root', database = 'HealthCareDB',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO prescription(patient_name,doctor_name,query,prescription,prescribe_date) "
        student_sql_query+="VALUES('"+patient+"','"+doctor+"','"+query+"','none','"+dd+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        context= {'data':'Query sent to doctor '+doctor}
        return render(request, 'SendQuery.html', context)

def ViewPrescription(request):
    if request.method == 'GET':
        user = ''
        output = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        con = pymysql.connect(host='127.0.0.1',port = 3308,user = 'root', password = 'root', database = 'HealthCareDB',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM prescription where patient_name='"+user+"'")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size=3 color=black>'+row[0]+'</font></td>'
                output+='<td><font size=3 color=black>'+row[1]+'</font></td>'
                output+='<td><font size=3 color=black>'+row[2]+'</font></td>'
                output+='<td><font size=3 color=black>'+row[3]+'</font></td>'
                output+='<td><font size=3 color=black>'+str(row[4])+'</font></td>'
        context= {'data':output}
        return render(request, 'ViewPrescription.html', context)            
    
    
def Signup(request):
    if request.method == 'POST':
      username = request.POST.get('username', False)
      password = request.POST.get('password', False)
      contact = request.POST.get('contact', False)
      email = request.POST.get('email', False)
      address = request.POST.get('address', False)
      usertype = request.POST.get('type', False)
      db_connection = pymysql.connect(host='127.0.0.1',port = 3308,user = 'root', password = 'root', database = 'HealthCareDB',charset='utf8')
      index = 0
      with db_connection:
          cur = db_connection.cursor()
          cur.execute("select username FROM register")
          rows = cur.fetchall()
          for row in rows:
              if row[0] == username:
                  index = 1
                  break
      if index == 0:
          db_cursor = db_connection.cursor()
          student_sql_query = "INSERT INTO register(username,password,contact,email,address,usertype) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"','"+usertype+"')"
          db_cursor.execute(student_sql_query)
          db_connection.commit()
          print(db_cursor.rowcount, "Record Inserted")
          context= {'data':'Signup Process Completed'}
          return render(request, 'Register.html', context)
      else:
          context= {'data':username+' Username already exists'}
          return render(request, 'Register.html', context)    
        
def getEmail(user):
    email = ''
    con = pymysql.connect(host='127.0.0.1',port = 3308,user = 'root', password = 'root', database = 'HealthCareDB',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select * FROM register")
        rows = cur.fetchall()
        for row in rows:
            if row[0] == user:
                email = row[3]
                break
    return email            


def SendPrescription(request):
    if request.method == 'GET':
        patient = request.GET['id']
        html = '<table align=center>'
        html+='<tr><td>Patient Name</td><td><input type=\"text\" name=\"t1\" value='+patient+' readonly></td></tr>'
        html+='<tr><td>Prescription</td><td><textarea name=\"t2\" id=\"t2\" rows="15" cols="60"></textarea></td></tr>'
        context= {'data1':html}
        return render(request, 'Prescription.html', context)   
        
def sendEmail(emailid,msgs):
    msg = EmailMessage()
    msg.set_content(msgs)
    msg['Subject'] = 'Message From Online Digital Health System'
    msg['From'] = "kaleem202120@gmail.com"
    msg['To'] = emailid
    
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("kaleem202120@gmail.com", "offenburg")
    s.send_message(msg)
    s.quit()
    #text.insert(END,"Email Message Sent To Authorities")    

def PrescriptionAction(request):
    if request.method == 'POST':
        patient = request.POST.get('t1', False)
        prescription = request.POST.get('t2', False)
        email = getEmail(patient)
        sendEmail(email,prescription)
        db_connection = pymysql.connect(host='127.0.0.1',port = 3308,user = 'root', password = 'root', database = 'HealthCareDB',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "update prescription set prescription='"+prescription+"' where prescription='none' and patient_name='"+patient+"'";
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record updated")
        context= {'data':'Prescription sent to '+patient+" email"}
        return render(request, 'DoctorScreen.html', context)
    
def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        usertype = request.POST.get('type', False)
        utype = 'none'
        con = pymysql.connect(host='127.0.0.1',port = 3308,user = 'root', password = 'root', database = 'HealthCareDB',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and row[1] == password and row[5] == usertype:
                    utype = 'success'
                    break
        if utype == 'success' and usertype == 'Doctor':
            file = open('session.txt','w')
            file.write(username)
            file.close()
            context= {'data':'welcome '+username}
            return render(request, 'DoctorScreen.html', context)
        if utype == 'success' and usertype == 'Patient':
            file = open('session.txt','w')
            file.write(username)
            file.close()
            context= {'data':'welcome '+username}
            return render(request, 'PatientScreen.html', context)
        if utype == 'success' and usertype == 'Medical Services':
            file = open('session.txt','w')
            file.write(username)
            file.close()
            context= {'data':'welcome '+username}
            return render(request, 'MedicalScreen.html', context)
        if utype == 'none':
            context= {'data':'Invalid login details'}
            return render(request, 'Login.html', context)

def AddMedicineDetails(request):
    if request.method == 'POST':
        name = request.POST.get('t1', False)
        dosage = request.POST.get('t2', False)
        formula = request.POST.get('t3', False)
        details = request.POST.get('t4', False)
        sideeffects = request.POST.get('t5', False)
        address = request.POST.get('t6', False)
        latitude = request.POST.get('t7', False)
        longitude = request.POST.get('t8', False)
        db_connection = pymysql.connect(host='127.0.0.1',port = 3308,user = 'root', password = 'root', database = 'HealthCareDB',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO medicinedetails(medicine_name,dosage,formula,details,side_effects,address,latitude,longitude) "
        student_sql_query+="VALUES('"+name+"','"+dosage+"','"+formula+"','"+details+"','"+sideeffects+"','"+address+"','"+latitude+"','"+longitude+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        context= {'data':'Medicine details added'}
        return render(request, 'MedicineDetails.html', context)



        
           
