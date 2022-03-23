from flask import Flask, render_template, request, redirect, Blueprint, send_file,jsonify,send_from_directory
from errors.handlers import errors
import pyrebase
import subprocess,urllib
import requests
from bs4 import BeautifulSoup
import json
import difflib
import time
import csv
from cryptography.fernet import Fernet
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import psutil



key = b'sJjlXtamtK6jFAWGy4j_EiA1VhZImH0PIsp-DGW4Dpg='
crypter = Fernet(key)

def encrypt(text):

    return crypter.encrypt(str(text).encode()).decode()

def decrypt(text):
    #crypter.decrypt(str(text).encode())
    return crypter.decrypt(text.encode()).decode()

app = Flask(__name__)

app.register_blueprint(errors)


firebaseConfig = {
    "apiKey": "AIzaSyDFiO7NBou0MBvNY1pELxb3juzeDJbGrVA",
    "authDomain": "project-cetele.firebaseapp.com",
    "databaseURL": "https://project-cetele.firebaseio.com",
    "projectId": "project-cetele",
    "storageBucket": "project-cetele.appspot.com",
    "messagingSenderId": "816156403835",
    "appId": "1:816156403835:web:bfc72d7ff42b1dfebc9ade",
    "measurementId": "G-F3SF25VM47"
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()


sender_email = "efeakaroz1@gmail.com"
reciever_email = "efeakaroz@gmail.com"
password = "gbeqxrdbffzbgjqc"
#WriterFirebase
firebaseConfig2 = {
    "apiKey": "AIzaSyAmmB5tpKCyWUwwOzNymw20XILlVReQ3D0",
    "authDomain": "cetelewritersupport.firebaseapp.com",
    "projectId": "cetelewritersupport",
    "storageBucket": "cetelewritersupport.appspot.com",
    "messagingSenderId": "95012497808",
    "appId": "1:95012497808:web:e87c1d11e41fc055072b15",
    "measurementId": "G-FTE96NS71V",
    "databaseURL":"https://cetelewritersupport-default-rtdb.europe-west1.firebasedatabase.app/"
}
firebaseWriter = pyrebase.initialize_app(firebaseConfig2)
writerDB = firebaseWriter.database()
writerAuth = firebaseWriter.auth()



unknownChars = ["#","?","/","\\","+"]








def notify(reciever,message,title):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    gmail_sender = 'sakizteam@gmail.com'
    gmail_passwd = 'efe12345'
    
    message = 'Subject: {}\n\n{}'.format(title,message)
    server.login(gmail_sender, gmail_passwd)


    server.sendmail(gmail_sender,reciever,message.encode('utf-8'))





@app.route('/')
def index2():
    #Competition
    compDataMathsName = db.child("Competition/maths/username").get().val()
    compDataMathsNumber = db.child("Competition/maths/questionNumber").get().val()

    compDataTurkishName = db.child("Competition/turkish/username").get().val()
    compDataTurkishNumber = db.child("Competition/turkish/questionNumber").get().val()

    compDataScienceName = db.child("Competition/science/username").get().val()
    compDataScienceNumber = db.child("Competition/science/questionNumber").get().val()



    oldView = db.child('KentelAnalitcys/index/count').get().val()

    if oldView == None:
        oldView=0
        data={'count':int(oldView['count'])+1}
        db.child('KentelAnalitcys').child('index').child('count').set(data)

    else: 
        data={'count':int(oldView['count'])+1}
        db.child('KentelAnalitcys').child('index').child('count').set(data)
    return render_template('index.html',compDataMathsName=compDataMathsName,
                            compDataMathsNumber=compDataMathsNumber,
                            compDataTurkishName=compDataTurkishName,
                            compDataTurkishNumber=compDataTurkishNumber,
                            compDataScienceName=compDataScienceName,
                            compDataScienceNumber=compDataScienceNumber
                            )


@app.route('/main')
def index():
    #Competition
    compDataMathsName = db.child("Competition/maths/username").get().val()
    compDataMathsNumber = db.child("Competition/maths/questionNumber").get().val()

    compDataTurkishName = db.child("Competition/turkish/username").get().val()
    compDataTurkishNumber = db.child("Competition/turkish/questionNumber").get().val()

    compDataScienceName = db.child("Competition/science/username").get().val()
    compDataScienceNumber = db.child("Competition/science/questionNumber").get().val()



    oldView = db.child('KentelAnalitcys/index/count').get().val()

    if oldView == None:
        oldView=0
        data={'count':int(oldView['count'])+1}
        db.child('KentelAnalitcys').child('index').child('count').set(data)

    else: 
        data={'count':int(oldView['count'])+1}
        db.child('KentelAnalitcys').child('index').child('count').set(data)
    return render_template('index.html',compDataMathsName=compDataMathsName,
                            compDataMathsNumber=compDataMathsNumber,
                            compDataTurkishName=compDataTurkishName,
                            compDataTurkishNumber=compDataTurkishNumber,
                            compDataScienceName=compDataScienceName,
                            compDataScienceNumber=compDataScienceNumber
                            )




@app.route('/new_user', methods=['POST', 'GET'])
def new_user():

    if request.method == "POST":
        password = request.form['password']
        password_again = request.form['password-again']
        emailNotReal = request.form['email']
        email = emailNotReal.lower()
        if password != password_again:
            return render_template('new_user.html', notsame=True, email=email)
        if password == password_again:
            try:
                username = email.split('@')

                data = {
                    'username': username[0],
                    'counter': 0,
                    'connect': False
                }
                for c in unknownChars:
                    if c in password:
                        return render_template("new_user.html",passwordCharError=True)
                    if c in username[0]:
                        return render_template("new_user.html",userNameCharError=True)
                    else:
                        pass
                
                auth.create_user_with_email_and_password(email, password)

                db.child('Users').child(username[0]).set(data)
                return render_template('registered.html')
            except Exception as e:
                notify("efeakaroz13@gmail.com",f"""{e} \n Error Time:{time.ctime(time.time())}""","Error")
                return render_template('new_user.html', alredyuser=True)

    return render_template('new_user.html')


@app.route('/index', methods=['POST', 'GET'])
def PageLoadisTrue():
    if request.method == "POST":
        if request.form['submit'] == "Giriş Yap":

            try:
                email = request.form['email']
                password = request.form['password']
                username = email.split('@')
                username0 = username[0]
                emailext = username[1]
                return redirect(f"/dashboardUsername='{encrypt(username0)}'AndPassword='{encrypt(password)}'Email='{encrypt(emailext)}'")

            except:
                return render_template('login.html', error=True)
        else:
            return redirect('/')

    if request.method == "GET":
        return render_template('login.html')


"""Students Start"""


@app.route("/dashboardUsername='<username0>'AndPassword='<pwd0>'Email='<emailextention0>'", methods=['POST', 'GET'])
def dashboard(username0, pwd0, emailextention0):
    try:
        username = decrypt(username0)
        pwd = decrypt(pwd0)
        emailextention = decrypt(emailextention0)
    except:
        username = username0
        pwd = pwd0
        emailextention = emailextention0
    if request.method == "POST":
        if request.form['submit'] == "Bilgileri Onayla":
            sno = request.form['studentNumber']
            
            FullName=request.form['FullName']

            ClassNumber = request.form['ClassNumber']
            ClassLetter = request.form['ClassLetter']
            className = f"{ClassNumber}/{ClassLetter}"
            schoolLevel  =request.form['schoolLevel']

            data = {
                'connect': True,
                'SchoolNumber': int(sno),
                'className':className,
                'FullName':FullName,
                'schoolLevel':schoolLevel,
                'ClassNumber':ClassNumber,
                'ClassLetter':ClassLetter,

            }

            db.child('Users').child(username).update(data)
            return redirect(f"/dashboardUsername='{encrypt(username)}'AndPassword='{encrypt(pwd)}'Email='{encrypt(emailextention)}'")

        if request.form['submit'] == "Soru sayısını ekle":


            questionSource = request.form['srcQuest']


            mistakeNumber = request.form['mistakesNumber']


            lessonname = request.form['lesson']


            questionnumber = request.form['questionNumber']


            timeUpdate = request.form['timeis']

            new_data = {
                'lesson': lessonname,
                'questioNumber': questionnumber,
                'time': timeUpdate,
                'mistakes': mistakeNumber,
                'source':questionSource


            }
            db.child('Users').child(username).child(lessonname).set(new_data)
            return redirect(f"/dashboardUsername='{encrypt(username)}'AndPassword='{encrypt(pwd)}'Email='{encrypt(emailextention)}'")

    if request.method == "GET":
        try:
            """Try and Except"""
            science = db.child(f'Users/{username}/science').get().val()
            try:
                scienceTime = science['time']
                scienceQuestionNum = science['questioNumber']
            except:
                scienceTime = "Veri Yok"
                scienceQuestionNum = "Veri Yok"

            # Mathematics
            maths = db.child(f'Users/{username}/maths').get().val()
            try:
                mathsTime = maths['time']
                mathsQuestionNum = maths['questioNumber']
            except:
                mathsTime = "Veri Yok"
                mathsQuestionNum = "Veri Yok"
            # Ataturkism
            # kemalism
            ataturkism = db.child(f'Users/{username}/ataturkism').get().val()
            try:
                ataturkismTime = ataturkism['time']
                ataturkismQuestionNum = ataturkism['questioNumber']
            except:
                ataturkismTime = "Veri Yok"
                ataturkismQuestionNum = "Veri Yok"
            # Turkish

            turkish = db.child(f'Users/{username}/turkish').get().val()
            try:
                turkishTime = turkish['time']
                turkishQuestionNum = turkish['questioNumber']
            except:
                turkishTime = "Veri Yok"
                turkishQuestionNum = "Veri Yok"

            # english
            english = db.child(f'Users/{username}/english').get().val()
            try:
                englishTime = english['time']
                englishQuestionNum = english['questioNumber']
            except:
                englishTime = "Veri Yok"
                englishQuestionNum = "Veri Yok"

            # religion
            religion = db.child(f'Users/{username}/religion').get().val()
            try:
                religionTime = religion['time']
                religionQuestionNum = religion['questioNumber']
            except:
                religionTime = "Veri Yok"
                religionQuestionNum = "Veri Yok"
            """End Code"""

            email = username+'@'+emailextention

            auth.sign_in_with_email_and_password(email, pwd)
            try:
                counternumber = db.child(
                    f'Users/{username}/counter').get().val()
                if counternumber == None:
                    counternumber = 0
            except:
                counternumber = 0

            data = {
                'username': username,
                'counter': counternumber+1,

            }
            try:
                db.child('Users').child(username).update(data)
            except:
                pass

            alredyConnected = db.child(f'Users/{username}/connect').get()
            UserTryer = db.child(f'Users/teachers/{username}').get().val()
            if alredyConnected.val() == True and UserTryer == None:
                zoomUsernames = db.child(f'Users/{username}/ZoomConnect').get().val()
                return render_template('UserDashBoard.html', noschool=False, mathsDateAndTime=mathsTime, mathsQuestionNumber=mathsQuestionNum,
                           scienceDateAndTime=scienceTime, scienceQuestionNumber=scienceQuestionNum,
                           ataturkismDateAndTime=ataturkismTime, ataturkismQuestionNumber=ataturkismQuestionNum,
                           turkishDateAndTime=turkishTime, turkishQuestionNumber=turkishQuestionNum,
                           englishDateAndTime=englishTime, englishQuestionNumber=englishQuestionNum,
                           religionDateAndTime=religionTime, religionQuestionNumber=religionQuestionNum,
                           username=username,password=pwd,mailext=emailextention,
                           teachers=zoomUsernames
                           )

            if UserTryer == None:

                return render_template('UserDashBoard.html', noschool=True)
            else:
                try:
                    db.child(f'Users/{username}').remove()
                    print('Deleted')
                except:
                    print('pass')
                return render_template('errorIsTeacher.html')
        except:
            
            return redirect('/index')


"""Student Finish"""


@app.route('/ogretmenKayıt', methods=['POST', 'GET'])
def teacherregister():

    if request.method == "POST":
        emailNotReal = request.form['email']
        password = request.form['password']
        nameis = request.form['FullName']
        schoolLevel = request.form["schoolLevel"]
        email = emailNotReal.lower()
        try:
            for c in unknownChars:
                if c in password:
                    return render_template("teacherRegister.html",passwordCharError=True)
                if c in username[0]:
                    return render_template("teacherRegister.html",userNameCharError=True)
                else:
                    pass
            auth.create_user_with_email_and_password(email, password)
            username = email.split('@')
            data = {
                'username': username[0],
                'email': email,
                'FullName': nameis,
                'School': schoolLevel,
                'Teacher': True
            }
            db.child('Users').child('teachers').child(username[0]).set(data)
            return redirect(f"/ogretmenAndusername='{encrypt(username[0])}'Andpwd='{encrypt(password)}'AndmailService='{encrypt(username[1])}'")
        except Exception as e:
            notify("efeakaroz13@gmail.com",f"""{e} \n Error Time:{time.ctime(time.time())}""","Error")
            return render_template('teacherRegister.html', error=True)

    if request.method == "GET":
        return render_template('teacherRegister.html')


# Teacher

@app.route("/ogretmenAndusername='<usernameN0>'Andpwd='<password0>'AndmailService='<mailservice0>'", methods=['POST', 'GET'])
def teacherDashboard(usernameN0, password0, mailservice0):
    try:
        usernameN = decrypt(usernameN0)
        password = decrypt(password0)
        mailservice = decrypt(mailservice0)
    except:
        usernameN = usernameN0
        password = password0
        mailservice = mailservice0

    username = usernameN.lower()
    if request.method == "POST":
        if request.form['submit'] == "Ekle":

            SchoolNumber = request.form['SchoolNumber']
            students = db.child('Users').child('teachers').child(
                username).child('students').get().val()
            if students == None:
                print('Students Not Found')
                students = []

            new_student_name = request.form['studentUsername']
            existits = db.child('Users').child(
                new_student_name).child('username').get().val()
            if existits == None:
                return render_template('teacherDashboard.html', studentNotFound=True, students=students,
                                       username=username, mailextention=mailservice, password=password)
            else:
                realShoolNumber = db.child(
                    f'Users/{new_student_name}/SchoolNumber').get().val()
                if str(SchoolNumber) == str(realShoolNumber):
                    data = {'username': new_student_name}
                    db.child('Users').child('teachers').child(username).child(
                        'students').child(new_student_name).set(data)
                    return redirect(f"/ogretmenAndusername='{encrypt(username)}'Andpwd='{encrypt(password)}'AndmailService='{encrypt(mailservice)}'")
                else:
                    return redirect(f"/ogretmenAndusername='{encrypt(username)}'Andpwd='{encrypt(password)}'AndmailService='{encrypt(mailservice)}'?schoolNumberIsNotMatching=yes")

        # deleteStudents
        if request.form['submit'] == "Sil":
            student = request.form['HoverStudentIs']
            db.child("Users").child("teachers").child(username).child("students").child(student).remove()
            return redirect(f"/ogretmenAndusername='{encrypt(username)}'Andpwd='{encrypt(password)}'AndmailService='{encrypt(mailservice)}'")

    if request.method == "GET":
        email = f'{username}@{mailservice}'
        UserTryer = db.child(f'Users/{username}/username').get().val()
        if UserTryer == None:
            try:
                auth.sign_in_with_email_and_password(email, password)
                try:
                    fullName = db.child('Users').child('teachers').child(
                        username).child('FullName').get().val()
                    db.child('Users').child('teachers').child(username).get()

                    students = db.child('Users').child('teachers').child(
                        username).child('students').get().val()
                    scNoErrorM = request.args.get("schoolNumberIsNotMatching")
                    if scNoErrorM =="yes":
                        scNoErrorM = True
                    else:
                        scNoErrorM=False
                    
                    if students == None:
                        print('Students Not Found')
                        students = []
                    else:
                        print('student found')

                    studentsWithFullName = []
                    for st in students:
                        FullNameStudent = db.child(f"Users/{st}/FullName").get().val()
                        if FullNameStudent == None:
                            FullNameStudent = st
                        studentsWithFullName.insert(0,FullNameStudent)
                    
                    
                    return render_template('teacherDashboard.html', teachername=fullName, students=students,
                                           username=username, mailext=mailservice, password=password,mailextention=mailservice,encrypt=encrypt,decrypt=decrypt,scNoErrorM=scNoErrorM)
                except:
                    return redirect('/teacherLogin')

            except:
                return redirect('/teacherLogin')

        else:
            return redirect(f"/dashboardUsername='{encrypt(username)}'AndPassword='{encrypt(password)}'Email='{encrypt(mailservice)}'")





"""UPDATE"""
            
@app.route("/AcceptStudentRequest")
def acceptStudentRequest():
    teacherUsername = request.args.get("teacherUsername")
    teacherMailExt = request.args.get("teacherMailExt")
    teacherPassword = request.args.get("teacherPassword")
    studentUsername= request.args.get("studentUsername")
    studentMailExt = request.args.get("studentMailExt")
    
    
    teacherEmail = teacherUsername+"@"+teacherMailExt
    teacherPassword = request.url.split("teacherPassword=")[1]
    try:
        auth.sign_in_with_email_and_password(teacherEmail,teacherPassword)
    except Exception as e:
        notify("efeakaroz13@gmail.com",f"""{e} \n Error Time:{time.ctime(time.time())}""","Error")
        return {"status":"Forbidden","e":str(e)}
        
    data = {
        "username":studentUsername,
        "cameFrom":"requests",
    }
    
    db.child("Users").child("teachers").child(teacherUsername).child("requests").child(studentUsername).remove()
    db.child("Users").child("teachers").child(teacherUsername).child("students").child(studentUsername).set(data)
    notify(studentUsername+"@"+studentMailExt,"Öğrenci isteğiniz kabul edildi","Tebrikler!")
    
    return redirect(f"/ogretmenAndusername='{teacherUsername}'Andpwd='{teacherPassword}'AndmailService='{teacherMailExt}'")
    
    
@app.route("/DenyStudentRequest")
def denyStudentRequest():
    teacherUsername = request.args.get("teacherUsername")
    teacherMailExt = request.args.get("teacherMailExt")
    teacherPassword = request.args.get("teacherPassword")
    studentUsername= request.args.get("studentUsername")
    studentMailExt = request.args.get("studentMailExt")
    teacherPassword = request.url.split("teacherPassword=")[1]
    
    teacherEmail = teacherUsername+"@"+teacherMailExt
    try:
        auth.sign_in_with_email_and_password(teacherEmail,teacherPassword)
    except:
        return {"status":"Forbidden"}
        
    data = {
        "username":studentUsername,
        "cameFrom":"requests",
    }
    
    db.child("Users").child("teachers").child(teacherUsername).child("requests").child(studentUsername).remove()

    notify(studentUsername+"@"+studentMailExt,"Öğrenci isteğiniz reddedildi","Üzgünüz...")
    
    return redirect(f"/ogretmenAndusername='{teacherUsername}'Andpwd='{teacherPassword}'AndmailService='{teacherMailExt}'")
    
    
    

@app.route("/studentRequests")
def studentRequests():
    try:
        username = decrypt(request.args.get("username"))
        mailext = decrypt(request.args.get("mailExt"))
        password = decrypt(request.args.get("password"))
        email = username+"@"+mailext
        data = {
            "username":username,
            "mailext":mailext,
            "password":password,
            "email":email
        }
        requests_ = db.child("Users").child("teachers").child(username).child("requests").get().val()
        if requests_ == None:
            requests_=[]
        auth.sign_in_with_email_and_password(email,password)
        return render_template("StudentRequests.html",username=username,mailext=mailext,password=password,encrypt=encrypt,requests=requests_)
    except:
        return "403"
@app.route("/request",methods=["POST","GET"])
def request_():
    import time
    teacher_username = request.args.get("teacher_username")
    teacher_mailext = request.args.get("mailext")
    teacherData = db.child("Users").child("teachers").child(teacher_username).get().val()
    
    if request.method == "POST":
        email = request.form.get("email")
        password=request.form.get("password")
        username = email.split("@")[0]
        data = {
            "student":username,
            "studentMail":email,
            "teacher":teacher_username,
            "sentTime":time.ctime(time.time()),
            "waiting":True
        }
        try:
            auth.sign_in_with_email_and_password(email,password)
            db.child("Users").child("teachers").child(teacher_username).child("requests").child(username).set(data)
            try:
                notify(teacher_username+"@"+teacher_mailext,f"{str(username)} kullanıcı adlı öğrenci {time.ctime(time.time())} zamanında size öğrenciniz olma talebinde bulundu. Çetele'ye giriş yaptıktan sonra öğrenci istekleri bölümünden gereğini yapabilirisiniz.","Yeni Öğrenci İsteği")
                notify(email,f"Öğrenci isteğinizi öğretmeninize ulaştırdık kabul ve red durumunda sizi bilgilendireceğiz. \n\n Çetele","İşlem başarılı")
                
            except Exception as e:
                return str(e)
            return render_template("SendRequest.html",requestSent=True)
        except:
            return render_template("SendRequest.html",passwordOrEmailNotCorrect=True)
        
    
    if teacherData != None:
            #here 
            teacherName = db.child("Users").child("teachers").child(teacher_username).child("FullName").get().val()
            return render_template("SendRequest.html",teacherName=teacherName)
    else:
        return render_template("SendRequest.html",error="Adres hatalı veya eksik.")
    
 #END UPDATE 

# deleteStudent
@app.route('/DeleteStudent<username>And<password>WillDelete<student>AND<mailservice>', methods=['POST', 'GET'])
def DeleteStudent(username, password, student, mailservice):

    db.child('Users').child('teachers').child(
        username).child('students').child(student).remove()

    return redirect(f"/ogretmenAndusername='{username}'Andpwd='{password}'AndmailService='{mailservice}'")


# teacher Login
@app.route('/teacherLogin', methods=['POST', 'GET'])
def teacherLogin():

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        username = email.split('@')
        try:
            auth.sign_in_with_email_and_password(email, password)
            try:
                db.child('Users').child('teachers').child(
                    username[0]).child('username').get()
                return redirect(f"/ogretmenAndusername='{encrypt(username[0])}'Andpwd='{encrypt(password)}'AndmailService='{encrypt(username[1])}'")
            except:
                return render_template('teacherlogin.html', error=True)

        except:
            return render_template('teacherlogin.html', error=True)

    return render_template('teacherlogin.html')


"""Student Viewer for teachers !!"""

# StudentDashboardViewer


@app.route('/StudentViewer+username=<username>+password=<password>+mailext=<mailextention>+studentUsername=<student>')
def StudentViewer(username, password, mailextention, student):

    try:
        email = username+'@'+mailextention
        auth.sign_in_with_email_and_password(email, password)

    except:
        return redirect('')

    classname = db.child(f'Users/{student}/className').get().val()
    if classname == None:
        classname="Sınıf Girilmemiş"

    else:
        pass


    FullName = db.child(f'Users/{student}/FullName').get().val()
    if FullName == None:
        FullName="İsim Girilmemiş"
    else:
        pass


    try:
        
        
        
        science = db.child(f'Users/{student}/science').get().val()
        try:
            scienceTime = science['time']
            scienceQuestionNum = science['questioNumber']
            scienceMistakes = science['mistakes']
            scienceSource= science['source']

        except:
            scienceSource="Yok"
            scienceTime = "0"
            scienceQuestionNum = "0"
            scienceMistakes = "0"

        # Mathematics
        maths = db.child(f'Users/{student}/maths').get().val()
        try:
            mathsSource= maths['source']

            mathsMistakes = maths['mistakes']
            mathsTime = maths['time']
            mathsQuestionNum = maths['questioNumber']
        except:
            mathsTime = "0"
            mathsQuestionNum = "0"
            mathsMistakes = "0"
            mathsSource="Yok"
        # Ataturkism
        # kemalism
        ataturkism = db.child(f'Users/{student}/ataturkism').get().val()
        try:
            ataturkismMistakes = ataturkism['mistakes']
            ataturkismSource= ataturkism['source']

            ataturkismTime = ataturkism['time']
            ataturkismQuestionNum = ataturkism['questioNumber']
        except:
            ataturkismTime = "0"
            ataturkismQuestionNum = "0"
            ataturkismMistakes = "0"
            ataturkismSource="Yok"
        # Turkish

        turkish = db.child(f'Users/{student}/turkish').get().val()
        try:
            turkishMistakes = turkish['mistakes']
            turkishSource= turkish['source']

            turkishTime = turkish['time']
            turkishQuestionNum = turkish['questioNumber']
        except:
            turkishTime = "0"
            turkishQuestionNum = "0"
            turkishMistakes = "0"
            turkishSource="Yok"
        # english
        english = db.child(f'Users/{student}/english').get().val()
        try:
            englishMistakes = english['mistakes']


            englishSource= english['source']

            englishTime = english['time']
            englishQuestionNum = english['questioNumber']
        except:
            englishTime = "0"
            englishQuestionNum = "0"
            englishMistakes = "0"
            englishSource="Yok"
        # religion
        religion = db.child(f'Users/{student}/religion').get().val()
        try:
            religionMistakes = religion['mistakes']
            religionSource= religion['source']

            religionTime = religion['time']
            religionQuestionNum = religion['questioNumber']
        except:
            religionMistakes = "0"
            religionTime = "0"
            religionQuestionNum = "0"
            religionSource="Yok"
    except:
        print('Error With Second Block(Database)')
    return render_template('TeacherStudentViewer.html', mathsDateAndTime=mathsTime, mathsQuestionNumber=mathsQuestionNum,
                           scienceDateAndTime=scienceTime, scienceQuestionNumber=scienceQuestionNum,
                           ataturkismDateAndTime=ataturkismTime, ataturkismQuestionNumber=ataturkismQuestionNum,
                           turkishDateAndTime=turkishTime, turkishQuestionNumber=turkishQuestionNum,
                           englishDateAndTime=englishTime, englishQuestionNumber=englishQuestionNum,
                           religionDateAndTime=religionTime, religionQuestionNumber=religionQuestionNum,
                           scienceMistakes=scienceMistakes, mathsMistakes=mathsMistakes,
                           turkishMistakes=turkishMistakes, ataturkismMistakes=ataturkismMistakes,
                           englishMistakes=englishMistakes, religionMistakes=religionMistakes,
                           classname = classname,
                           scienceSource= scienceSource,mathsSource= mathsSource,religionSource= religionSource,
                           turkishSource= turkishSource,englishSource= englishSource,
                           ataturkismSource= ataturkismSource,
                           mailextention=mailextention,
                           StudentFullName = FullName

                           )




#Updated

@app.route('/saveToCsv/homeworks/<username>/<password>/<mailext>/<branch>', methods=['GET'])
def saveToCSV(username, password, mailext, branch):
    if request.method == "GET":
        teacherGet = db.child(f"Users/teachers/{username}").get().val()
        if teacherGet != None:
            try:
                email = username+'@'+mailext
                auth.sign_in_with_email_and_password(email, password)

                studentList = db.child(
                    f"Users/teachers/{username}/students").get().val()
                    
                import random
                value = random.randint(5,5000)
                from flask import safe_join
                
                
                
               
                with open(f'files/saved{value}.csv', 'w') as csvfile:
                    cr = csv.reader(csvfile)
                    cw = csv.writer(csvfile, delimiter=',')

                    cw.writerow(['Kullanici adi', 'Sinif', 'Numara',
                                 'Soru Sayisi', 'Hata Sayisi', 'Kaynak','Tarih'])
                    for usr in studentList:
                        studentAccountMain = db.child(
                            f"Users/{usr}").get().val()

                        getGeneralFromBranch = db.child(
                            f"Users/{usr}/{branch}").get().val()

                        FullName = db.child(f"Users/{usr}/FullName").get().val()

                        if FullName ==None:
                            FullName = usr
                        else: 
                            pass

                        try:
                            lister = [FullName, studentAccountMain['className'],
                                    studentAccountMain['SchoolNumber'], getGeneralFromBranch['questioNumber'], 
                                    getGeneralFromBranch['mistakes'], getGeneralFromBranch['source'],getGeneralFromBranch['time']]
                        except:
                            lister = [FullName, studentAccountMain['className'],
                                    studentAccountMain['SchoolNumber'], "0", 
                                    "0", "Yok","00.00"]
                        
                        cw.writerow(lister)
                safe_path = safe_join("./files",f"saved{value}.csv")
                

                return send_file(safe_path,as_attachment=True)
 
            except Exception as e:
                notify("efeakaroz13@gmail.com",f"""{e} \n Error Time:{time.ctime(time.time())}""","Error")
                return "Öğrenciniz bulunmadığı için excel'e dönüştürülemiyor."

        else:
            return "<script>alert('Öğrencilerin yapmasına izin verilmeyen işlemi yapmaktan suçlu bulundunuz!')</script>"





@app.route(f'/studentTable+teacher=<teacherusername>+mailext=<mailext>+userpassword=<password>+branch=<branch>')
def tabler(teacherusername, mailext, password, branch):
    questionisList = []
    datelister = []
    mistaker = []
    studentNamesAre = []
    email = teacherusername + '@' + mailext
    try:
        auth.sign_in_with_email_and_password(email, password)

        TeachersStudentNames = db.child(
            f'Users/teachers/{teacherusername}/students').get().val()
        studentNamesAre.clear()
        datelister.clear()
        mistaker.clear()
        questionisList.clear()
        for st in TeachersStudentNames:
            studentProfile = db.child(f'Users/{st}/username').get().val()

            quenum = db.child(f'Users/{st}/{branch}/questioNumber').get().val()
            date = db.child(f'Users/{st}/{branch}/time').get().val()
            mistake = db.child(f'Users/{st}/{branch}/mistakes').get().val()

            questionisList.insert(0, quenum)
            studentNamesAre.insert(0, st)
            datelister.insert(0, date)

            mistaker.insert(0, mistake)

        return render_template('studentTable.html', studentName=studentNamesAre,
                               questions=questionisList, date=datelister,
                               mistakes=mistaker, mailext=mailext, mailextention=mailext,
                               username=teacherusername, password=password, branch=branch)
    except:
        return render_template('studentTable.html', studentName=[],
                               questions=[], date=[],
                               mistakes=[], mailext=mailext, mailextention=mailext,
                               username=teacherusername, password=password, branch=branch)

    email = teacherusername + '@' + mailext
    try:
        auth.sign_in_with_email_and_password(email, password)

        TeachersStudentNames = db.child(
            f'Users/teachers/{teacherusername}/students').get().val()
        studentNamesAre.clear()
        datelister.clear()
        mistaker.clear()
        questionisList.clear()
        for st in TeachersStudentNames:
            studentProfile = db.child(f'Users/{st}/username').get().val()

            quenum = db.child(f'Users/{st}/{branch}/questioNumber').get().val()
            date = db.child(f'Users/{st}/{branch}/time').get().val()
            mistake = db.child(f'Users/{st}/{branch}/mistakes').get().val()
            
            questionisList.insert(0,quenum)
            studentNamesAre.insert(0,st)
            datelister.insert(0,date)

            mistaker.insert(0,mistake)

        return render_template('studentTable.html',studentName=studentNamesAre,
                                questions=questionisList,date=datelister,mistakes=mistaker,mailext=mailext,mailextention=mailext)
    except:
            return "Onaylanamadı !"
    
    


"""Zoom Stuff"""
@app.route("/ZoomConnect4TeachersAndUsername=<teacherusername>+pwd=<teacherpassword>+mailext=<mailext>",methods=['POST','GET'])
def zoomerForTeachers(teacherusername,teacherpassword,mailext):
    if request.method == "POST":
        username=teacherusername
        zoomLink = request.form['zoomLink']
        
        httpsis = zoomLink.split('https://')
        try:
            httpsis[1]

    
            note = request.form['note']
            alredyStudent = db.child(f'Users/teachers/{username}/students').get().val()
            if alredyStudent == None:
                return "Öğrenci Bulunmamamkta"
            else:
                data={
                    'teacher':username,
                    'zoomLink':zoomLink,
                    'note':note
                    
                }
                for st in alredyStudent:
                    db.child(f'Users').child(st).child('ZoomConnect').child(username).set(data)
                return render_template('zoomer/CreateForTeacher.html',sent=True)
        except:
            return render_template('zoomer/CreateForTeacher.html',sent=False)

        

    email = teacherusername+'@'+mailext
    try:

        auth.sign_in_with_email_and_password(email,teacherpassword)
        return render_template('zoomer/CreateForTeacher.html')
    except:
        return "Dönüş Adresi Alınamadı !"


@app.route('/ZoomConnect4StudentsAndUSERNAME=<username>+pwd=<password>+Mail=<mailext>+teacher=<teacher>')
def zoomerForStudents (username , password,mailext,teacher):
    email = username+'@'+mailext

    
        

    try:
        auth.sign_in_with_email_and_password(email,password)
        zoomLink = db.child(f'Users/{username}/ZoomConnect/{teacher}/zoomLink').get().val()
        if zoomLink== None:
            pass
        else:
            teacherName=db.child(f'Users/teachers/{teacher}/FullName').get().val()
            teacherNote = db.child(f'Users/{username}/ZoomConnect/{teacher}/note').get().val()


            
            return render_template('zoomer/joinStudent.html',teacherNote=teacherNote,ZoomLink=zoomLink,TeacherUsername=teacherName)
    except:
        return "Dönüş Adresi Alınamadı !!"
@app.route('/ZoomTable-username=<username>-pwd=<password>-mail=<mailext>')
def zoomTable(username,password,mailext):




    email = username+'@'+mailext
    try:
        

        zoomUsernames = db.child(f'Users/{username}/ZoomConnect').get().val()
        auth.sign_in_with_email_and_password(email,password)
        return render_template('zoomer/ZoomTable.html',teachers=zoomUsernames,
                                username=username,password=password,mailext=mailext
        )
    except:
        return "Onaylanamadı !! fakedirsup@gmail.com adresine ulaşın !"


"""End Zoom Stuff"""


"""About Page"""
@app.route('/about')
def aboutUs():
    return render_template('aboutUS.html')


"""Download Page"""
@app.route('/downloads')
def downloads():
    return render_template('downloadsCetele.html')

@app.route('/download/<filename>')
def downloadFile(filename):
    try:
        return send_file(f'downloads/{filename}')
    except:
        return render_template('downloadsCetele.html',notFound=True)










RealadminUsername = "efeakaroz13"
RealadminPassword="efeAkaroz123"
"""Admin All Stuff"""
@app.route('/admin',methods=['POST','GET'])
def admin():
    if request.method == "POST":
        print('Method == POST')
        

        formTheUsername=request.form['username']
        formThePass = request.form['password']

        if RealadminUsername != formTheUsername:
            if RealadminPassword != formThePass:
                return render_template('admin/adminLogin.html',UsernameError = True,PasswordError=True)

            else:
                return render_template('admin/adminLogin.html',UsernameError = True)


        else:
            if RealadminPassword != formThePass:
                return render_template('admin/adminLogin.html',UsernameError = False,PasswordError=True)

            else:
                #logged in Successfully!
                return redirect(f'/admin/{formTheUsername}+{formThePass}/main')




    return render_template('admin/adminLogin.html')

@app.route('/admin/<username>+<password>/main')
def adminMain(username,password):
    if RealadminUsername==username:
        if RealadminPassword == password:
            #Logged in success
            viewsOfindex = db.child('KentelAnalitcys/index/count/count').get().val()
            UsersAll = db.child('Users').get().val()
            howMany = len(UsersAll)

            Users_teacher_all = db.child('Users/teachers').get().val()
            howMany_teachers = len(Users_teacher_all)

            return render_template('admin/index.html',IndexViewers=viewsOfindex,
                                    userCounter=howMany-1,teacherCounter=howMany_teachers,username=username,password=password)




        else:
            return render_template('loading.html')
    else:
        return render_template('loading.html')


@app.route('/admin/<username>+<password>/viewUsers')
def viewUsers(username,password):
    StudentUsers=db.child('Users').get().val()

    TeacherUsers = db.child('Users/teachers').get().val()
    

    return render_template('admin/viewUsers.html',students=StudentUsers,teachers=TeacherUsers)



"""Admin END"""

"""View the profile Starts"""
@app.route('/settings/student/<username>/<password>/<mailext>')
def settingsStudent(username,password,mailext):
    email = username+'@'+mailext

    SchoolNum = db.child(f'Users/{username}/SchoolNumber').get().val()
    try: 
        auth.sign_in_with_email_and_password(email,password)



        return render_template('settings/studentSettings.html',username=username,
                                password=password,email=email,
                                schoolNum=SchoolNum,mailext=mailext)
    except:
        return redirect('/')

@app.route('/changepassword/student/<username>/<password>/<mailext>')
def changeStudentPass(username,mailext,password):
    email = username+'@'+mailext
    try:
        auth.sign_in_with_email_and_password(email,password)

        auth.send_password_reset_email(email)
        return render_template('settings/emailSent.html',email=email)

    except:
        return redirect('/')


#Teachers' Settings
@app.route('/settings/teacher/<username>/<password>/<mailext>')
def settingsTeacher(username,mailext,password):
    email = username+'@'+mailext
    try:
        fullname = db.child(f'Users/teachers/{username}/FullName').get().val()
        auth.sign_in_with_email_and_password(email,password)
        return render_template('settings/teacherSettings.html',username=username,
                                email=email,password=password,fullname=fullname,
                                mailext=mailext)

    except:
        return redirect('/')


@app.route('/changepassword/teacher/<username>/<password>/<mailext>')
def changeTeacherPass(username,mailext,password):
    email = username+'@'+mailext
    try:
        auth.sign_in_with_email_and_password(email,password)

        auth.send_password_reset_email(email)
        return render_template('settings/emailSent.html',email=email)

    except:
        return redirect('/')






"""Homeworks"""
@app.route('/SendHomework/<username>/<password>/<mailext>',methods=['POST','GET'])
def SendHomework(username,password,mailext):
    import requests,urllib,json

    if request.method=="POST":
        students = db.child(f'Users/teachers/{username}/students').get().val()

        time = request.form['time']
        titleOfHomework = request.form['titleHomework']

        descHomework = request.form['descHomework']


        
        actualfile = request.files['pdffile']

        import os
        filename = actualfile.filename
        if filename != "":
            actualfile.save(os.path.join('files', actualfile.filename))
            
            filenameSplitter = filename.split('.')
            extfile = filenameSplitter[1]
            File=True

            storage.child(f"pdfs/{username}/{time}.{extfile}").put(f"files/{filename}")
            os.remove(f'files/{filename}')
            #Start
            


            "https://firebasestorage.googleapis.com/v0/b/project-cetele.appspot.com/o/pdfs%2Fefeakaroz1313%2F2021-2-17%209%3A6%3A45.pdf?alt=media&token=ebad88ba-8d41-4778-9a05-cbbd9625c4dd"

            fileAddress = f"https://firebasestorage.googleapis.com/v0/b/project-cetele.appspot.com/o/pdfs%2F{username}%2F{time}.{extfile}?alt=media&token="


        else:
            File=False
            fileAddress = ""

        teacherFullName = db.child(f'Users/teachers/{username}/FullName').get().val()
        schoolLevel = request.form.get("schoolLevel")


        data = {
            'teacher':teacherFullName,
            'title':titleOfHomework,
            'description':descHomework,
            'time':time,
            'filebool':File,
            'fileAdress':fileAddress,
            'schoolLevel':schoolLevel
            
        }
        
        if students == None:
            students = []
        
        for st in students:
            classNo = db.child("Users").child(st).child("ClassNumber").get().val()
            if classNo == None:
                pass
            else:
                if int(classNo) == int(schoolLevel):
                    
                    db.child('Users').child(st).child('homework').child(time).set(data)
                else:
                    pass
                    
                
            
        return render_template('homework/sendHomework.html',succeed=True,usename=username,password=password,mailext=mailext)

    if request.method == "GET":

        email = username+'@'+mailext
        try: 
            auth.sign_in_with_email_and_password(email,password)
            nameTester = db.child(f'Users/teachers/{username}/username').get().val()
            if nameTester==None:
                return "Öğrenciler Kendilerine Ödev yazamazlar!"
            else:

                return render_template('homework/sendHomework.html',username=username,password=password,mailext=mailext)
        except:
            return redirect('/')



@app.route('/homework/<username>/<password>/<mailext>')
def ViewHomeworks(username,password,mailext):
    email = username+'@'+mailext

    try:
        NameTester = db.child(f'Users/teachers/{username}/username').get().val()
        if NameTester == None:
            auth.sign_in_with_email_and_password(email,password)
            homeworks = db.child(f'Users/{username}/homework').get().val()
            if homeworks == None:
                homeworks = ['Ödev Bulunmamakta!']
            return render_template('homework/viewHomeworkAsAlist.html',homeworks=homeworks,username=username,password=password,mailext=mailext)
        
        else:
            return redirect('/')
    except:
        return redirect('/')


@app.route('/view/homework/<username>/<password>/<mailext>/<homeWorkTime>')
def ViewHomeworkTime(username,password,mailext,homeWorkTime):
    email = username+'@'+mailext
    try:
        auth.sign_in_with_email_and_password(email,password)
        homeworkGet = db.child(f'Users/{username}/homework/{homeWorkTime}').get().val()
        filebool = db.child(f'Users/{username}/homework/{homeWorkTime}/filebool').get().val()
        if homeworkGet == None:
            homeworkTitle = ""
            senderTeacher=""
            sendingTime=""
            descHomework=""
            fileAdress=""
            filebool = False


        else:
            homeworkTitle = homeworkGet['title']
            senderTeacher= homeworkGet['teacher']
            sendingTime=homeworkGet['time']
            descHomework=homeworkGet['description']
            if filebool == True:
                filebool=True
                fileAdress = db.child(f'Users/{username}/homework/{homeWorkTime}/fileAdress').get().val()
            else:
                filebool = False
                fileAdress = ""



        return render_template('homework/viewHomework.html',homeworkTitle=homeworkTitle,senderTeacher=senderTeacher,
                                sendingTime=sendingTime,descHomework=descHomework,
                                filebool=filebool,fileAdress=fileAdress)
    except:
        return redirect('/')



"""Terminal"""
@app.route('/terminal',methods=['POST','GET'])
def terminal():
    terminalOut = []
    if request.method == "POST":
        if request.form['submit'] == "Login":
            apiKey = "GRYAZ6513"
            UserApiInp = request.form['apiKey']
            if UserApiInp == apiKey :
                return render_template('admin/terminal/terminal.html' ,loggedin=True)
            else:
                return "<h3>ACCESS DENIED</h3>"



        if request.form['submit'] == "Reload SupervisorCTL":
            import os
            os.system('supervisorctl reload')
            return render_template('admin/terminal/terminal.html',loggedin=True)



    return render_template('admin/terminal/terminal.html',loggedin=False)

"""Book AI"""


@app.route('/book/<username>/<password>/<mailext>',methods=['POST','GET'])
def books(username,password,mailext):
    email = f"{username}@{mailext}"
    try:
        print("")
        auth.sign_in_with_email_and_password(email,password)
        print("logged in")
        r = requests.get("https://www.kitapsec.com/vitrin/edebiyat-5/")


        soup = BeautifulSoup(r.text, 'html.parser')

        newFilmsDiv = soup.find_all("a", {"class": "img"})



        newFilmsDivA = soup.find_all("li", {"class": "trz-tda"})
        return render_template("books/index.html",Div=newFilmsDiv)

    except:
        return redirect("/")































#E N G L I S H 
"""English"""
englishFuncName = "_en"


@app.route('/en')
def index2_en():
    #Competition
    compDataMathsName = db.child("Competition/maths/username").get().val()
    compDataMathsNumber = db.child("Competition/maths/questionNumber").get().val()

    compDataTurkishName = db.child("Competition/turkish/username").get().val()
    compDataTurkishNumber = db.child("Competition/turkish/questionNumber").get().val()

    compDataScienceName = db.child("Competition/science/username").get().val()
    compDataScienceNumber = db.child("Competition/science/questionNumber").get().val()



    oldView = db.child('KentelAnalitcys/index/count').get().val()

    if oldView == None:
        oldView=0
        data={'count':int(oldView['count'])+1}
        db.child('KentelAnalitcys').child('index').child('count').set(data)

    else: 
        data={'count':int(oldView['count'])+1}
        db.child('KentelAnalitcys').child('index').child('count').set(data)
    return render_template('english/index.html',compDataMathsName=compDataMathsName,
                            compDataMathsNumber=compDataMathsNumber,
                            compDataTurkishName=compDataTurkishName,
                            compDataTurkishNumber=compDataTurkishNumber,
                            compDataScienceName=compDataScienceName,
                            compDataScienceNumber=compDataScienceNumber
                            )



@app.route('/en/main')
def index_en():
    #Competition
    compDataMathsName = db.child("Competition/maths/username").get().val()
    compDataMathsNumber = db.child("Competition/maths/questionNumber").get().val()

    compDataTurkishName = db.child("Competition/turkish/username").get().val()
    compDataTurkishNumber = db.child("Competition/turkish/questionNumber").get().val()

    compDataScienceName = db.child("Competition/science/username").get().val()
    compDataScienceNumber = db.child("Competition/science/questionNumber").get().val()



    oldView = db.child('KentelAnalitcys/index/count').get().val()

    if oldView == None:
        oldView=0
        data={'count':int(oldView['count'])+1}
        db.child('KentelAnalitcys').child('index').child('count').set(data)

    else: 
        data={'count':int(oldView['count'])+1}
        db.child('KentelAnalitcys').child('index').child('count').set(data)
    return render_template('english/index.html',compDataMathsName=compDataMathsName,
                            compDataMathsNumber=compDataMathsNumber,
                            compDataTurkishName=compDataTurkishName,
                            compDataTurkishNumber=compDataTurkishNumber,
                            compDataScienceName=compDataScienceName,
                            compDataScienceNumber=compDataScienceNumber
                            )




@app.route('/en/new_user', methods=['POST', 'GET'])
def new_user_en():

    if request.method == "POST":
        password = request.form['password']
        password_again = request.form['password-again']
        emailNotReal = request.form['email']
        email = emailNotReal.lower()
        if password != password_again:
            return render_template('english/new_user.html', notsame=True, email=email)
        if password == password_again:
            try:
                username = email.split('@')
                data = {
                    'username': username[0],
                    'counter': 0,
                    'connect': False
                }

                auth.create_user_with_email_and_password(email, password)

                db.child('Users').child(username[0]).set(data)
                return render_template('english/registered.html')
            except:
                return render_template('english/new_user.html', alredyuser=True)

    return render_template('english/new_user.html')


@app.route('/en/index', methods=['POST', 'GET'])
def PageLoadisTrue_en():
    if request.method == "POST":
        if request.form['submit'] == "Giriş Yap":

            try:
                email = request.form['email']
                password = request.form['password']
                username = email.split('@')
                username0 = username[0]
                emailext = username[1]
                return redirect(f"/en/dashboardUsername='{username0}'AndPassword='{password}'Email='{emailext}'")

            except:
                return render_template('english/login.html', error=True)
        else:
            return redirect('/en')

    if request.method == "GET":
        return render_template('english/login.html')


"""Students Start"""


@app.route("/en/dashboardUsername='<username>'AndPassword='<pwd>'Email='<emailextention>'", methods=['POST', 'GET'])
def dashboard_en(username, pwd, emailextention):
    if request.method == "POST":
        if request.form['submit'] == "Bilgileri Onayla":
            sno = request.form['studentNumber']
            className = request.form['className']
            data = {
                'connect': True,
                'SchoolNumber': int(sno),
                'className':className
            }

            db.child('Users').child(username).update(data)
            return redirect(f"/en/dashboardUsername='{username}'AndPassword='{pwd}'Email='{emailextention}'")

        if request.form['submit'] == "Soru sayısını ekle":


            questionSource = request.form['srcQuest']


            mistakeNumber = request.form['mistakesNumber']


            lessonname = request.form['lesson']


            questionnumber = request.form['questionNumber']


            timeUpdate = request.form['timeis']

            new_data = {
                'lesson': lessonname,
                'questioNumber': questionnumber,
                'time': timeUpdate,
                'mistakes': mistakeNumber,
                'source':questionSource


            }
            db.child('Users').child(username).child(lessonname).set(new_data)
            return redirect(f"/en/dashboardUsername='{username}'AndPassword='{pwd}'Email='{emailextention}'")

    if request.method == "GET":
        try:
            """Try and Except"""
            science = db.child(f'Users/{username}/science').get().val()
            try:
                scienceTime = science['time']
                scienceQuestionNum = science['questioNumber']
            except:
                scienceTime = "0"
                scienceQuestionNum = "0"

            # Mathematics
            maths = db.child(f'Users/{username}/maths').get().val()
            try:
                mathsTime = maths['time']
                mathsQuestionNum = maths['questioNumber']
            except:
                mathsTime = "0"
                mathsQuestionNum = "0"
            # Ataturkism
            # kemalism
            ataturkism = db.child(f'Users/{username}/ataturkism').get().val()
            try:
                ataturkismTime = ataturkism['time']
                ataturkismQuestionNum = ataturkism['questioNumber']
            except:
                ataturkismTime = "0"
                ataturkismQuestionNum = "0"
            # Turkish

            turkish = db.child(f'Users/{username}/turkish').get().val()
            try:
                turkishTime = turkish['time']
                turkishQuestionNum = turkish['questioNumber']
            except:
                turkishTime = "0"
                turkishQuestionNum = "0"

            # english
            english = db.child(f'Users/{username}/english').get().val()
            try:
                englishTime = english['time']
                englishQuestionNum = english['questioNumber']
            except:
                englishTime = "0"
                englishQuestionNum = "0"

            # religion
            religion = db.child(f'Users/{username}/religion').get().val()
            try:
                religionTime = religion['time']
                religionQuestionNum = religion['questioNumber']
            except:
                religionTime = "0"
                religionQuestionNum = "0"
            """End Code"""

            email = username+'@'+emailextention

            auth.sign_in_with_email_and_password(email, pwd)
            try:
                counternumber = db.child(
                    f'Users/{username}/counter').get().val()
                if counternumber == None:
                    counternumber = 0
            except:
                counternumber = 0

            data = {
                'username': username,
                'counter': counternumber+1,

            }
            try:
                db.child('Users').child(username).update(data)
            except:
                pass

            alredyConnected = db.child(f'Users/{username}/connect').get()
            UserTryer = db.child(f'Users/teachers/{username}').get().val()
            if alredyConnected.val() == True and UserTryer == None:
                zoomUsernames = db.child(f'Users/{username}/ZoomConnect').get().val()
                return render_template('english/UserDashBoard.html', noschool=False, mathsDateAndTime=mathsTime, mathsQuestionNumber=mathsQuestionNum,
                           scienceDateAndTime=scienceTime, scienceQuestionNumber=scienceQuestionNum,
                           ataturkismDateAndTime=ataturkismTime, ataturkismQuestionNumber=ataturkismQuestionNum,
                           turkishDateAndTime=turkishTime, turkishQuestionNumber=turkishQuestionNum,
                           englishDateAndTime=englishTime, englishQuestionNumber=englishQuestionNum,
                           religionDateAndTime=religionTime, religionQuestionNumber=religionQuestionNum,
                           username=username,password=pwd,mailext=emailextention,
                           teachers=zoomUsernames
                           )

            if UserTryer == None:

                return render_template('english/UserDashBoard.html', noschool=True)
            else:
                try:
                    db.child(f'Users/{username}').remove()
                    print('Deleted')
                except:
                    print('pass')
                return render_template('english/errorIsTeacher.html')
        except:
            
            return redirect('/en')


"""Student Finish"""


@app.route('/en/ogretmenKayıt', methods=['POST', 'GET'])
def teacherregister_en():

    if request.method == "POST":
        emailNotReal = request.form['email']
        password = request.form['password']
        nameis = request.form['FullName']
        schoolLevel = request.form["schoolLevel"]
        email = emailNotReal.lower()
        try:
            auth.create_user_with_email_and_password(email, password)
            username = email.split('@')
            data = {
                'username': username[0],
                'email': email,
                'FullName': nameis,
                'School': schoolLevel,
                'Teacher': True
            }
            db.child('Users').child('teachers').child(username[0]).set(data)
            return redirect(f"/en/ogretmenAndusername='{username[0]}'Andpwd='{password}'AndmailService='{username[1]}'")
        except:
            return render_template('english/teacherRegister.html', error=True)

    if request.method == "GET":
        return render_template('english/teacherRegister.html')


# Teacher

@app.route("/en/ogretmenAndusername='<usernameN>'Andpwd='<password>'AndmailService='<mailservice>'", methods=['POST', 'GET'])
def teacherDashboard_en(usernameN, password, mailservice):
    username = usernameN.lower()
    if request.method == "POST":
        if request.form['submit'] == "Add":

            SchoolNumber = request.form['SchoolNumber']
            students = db.child('Users').child('teachers').child(
                username).child('students').get().val()
            if students == None:
                print('Students Not Found')
                students = []

            new_student_name = request.form['studentUsername']
            existits = db.child('Users').child(
                new_student_name).child('username').get().val()
            if existits == None:
                return render_template('english/teacherDashboard.html', studentNotFound=True, students=students,
                                       username=username, mailextention=mailservice, password=password)
            else:
                realShoolNumber = db.child(
                    f'Users/{new_student_name}/SchoolNumber').get().val()
                if str(SchoolNumber) == str(realShoolNumber):
                    data = {'username': new_student_name}
                    db.child('Users').child('teachers').child(username).child(
                        'students').child(new_student_name).set(data)
                    return redirect(f"/en/ogretmenAndusername='{username}'Andpwd='{password}'AndmailService='{mailservice}'")
                else:
                    return redirect(f"/en/ogretmenAndusername='{username}'Andpwd='{password}'AndmailService='{mailservice}'")

        # deleteStudents
        if request.form['submit'] == "Remove":
            student = request.form['HoverStudentIs']
            return redirect(f"/en/DeleteStudent{username}And{password}WillDelete{student}AND{mailservice}")

    if request.method == "GET":
        email = f'{username}@{mailservice}'
        UserTryer = db.child(f'Users/{username}/username').get().val()
        if UserTryer == None:
            try:
                auth.sign_in_with_email_and_password(email, password)
                try:
                    fullName = db.child('Users').child('teachers').child(
                        username).child('FullName').get().val()
                    db.child('Users').child('teachers').child(username).get()

                    students = db.child('Users').child('teachers').child(
                        username).child('students').get().val()

                    
                    if students == None:
                        print('Students Not Found')
                        students = []
                    else:
                        print('student found')

                    return render_template('english/teacherDashboard.html', teachername=fullName, students=students,
                                           username=username, mailext=mailservice, password=password,mailextention=mailservice)
                except:
                    return redirect('/en/teacherLogin')

            except:
                return redirect('/en/teacherLogin')

        else:
            return redirect(f"/en/dashboardUsername='{username}'AndPassword='{password}'Email='{mailservice}'")


# deleteStudent
@app.route('/en/DeleteStudent<username>And<password>WillDelete<student>AND<mailservice>', methods=['POST', 'GET'])
def DeleteStudent_en(username, password, student, mailservice):

    db.child('Users').child('teachers').child(
        username).child('students').child(student).remove()

    return redirect(f"/en/ogretmenAndusername='{username}'Andpwd='{password}'AndmailService='{mailservice}'")


# teacher Login
@app.route('/en/teacherLogin', methods=['POST', 'GET'])
def teacherLogin_en():

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        username = email.split('@')
        try:
            auth.sign_in_with_email_and_password(email, password)
            try:
                db.child('Users').child('teachers').child(
                    username[0]).child('username').get()
                return redirect(f"/en/ogretmenAndusername='{username[0]}'Andpwd='{password}'AndmailService='{username[1]}'")
            except:
                return render_template('english/teacherlogin.html', error=True)

        except:
            return render_template('english/teacherlogin.html', error=True)

    return render_template('english/teacherlogin.html')


"""Student Viewer for teachers !!"""

# StudentDashboardViewer


@app.route('/en/StudentViewer+username=<username>+password=<password>+mailext=<mailextention>+studentUsername=<student>')
def StudentViewer_en(username, password, mailextention, student):

    try:
        email = username+'@'+mailextention
        auth.sign_in_with_email_and_password(email, password)

    except:
        return redirect('')

    classname = db.child(F'Users/{student}/className').get().val()
    if classname == None:
        classname="Sınıf Girilmemiş"

    else:
        pass
    try:
        
        
        
        science = db.child(f'Users/{student}/science').get().val()
        try:
            scienceTime = science['time']
            scienceQuestionNum = science['questioNumber']
            scienceMistakes = science['mistakes']
            scienceSource= science['source']

        except:
            scienceSource=""
            scienceTime = ""
            scienceQuestionNum = ""
            scienceMistakes = ""

        # Mathematics
        maths = db.child(f'Users/{student}/maths').get().val()
        try:
            mathsSource= maths['source']

            mathsMistakes = maths['mistakes']
            mathsTime = maths['time']
            mathsQuestionNum = maths['questioNumber']
        except:
            mathsTime = ""
            mathsQuestionNum = ""
            mathsMistakes = ""
            mathsSource=""
        # Ataturkism
        # kemalism
        ataturkism = db.child(f'Users/{student}/ataturkism').get().val()
        try:
            ataturkismMistakes = ataturkism['mistakes']
            ataturkismSource= ataturkism['source']

            ataturkismTime = ataturkism['time']
            ataturkismQuestionNum = ataturkism['questioNumber']
        except:
            ataturkismTime = ""
            ataturkismQuestionNum = ""
            ataturkismMistakes = ""
            ataturkismSource=""
        # Turkish

        turkish = db.child(f'Users/{student}/turkish').get().val()
        try:
            turkishMistakes = turkish['mistakes']
            turkishSource= turkish['source']

            turkishTime = turkish['time']
            turkishQuestionNum = turkish['questioNumber']
        except:
            turkishTime = ""
            turkishQuestionNum = ""
            turkishMistakes = ""
            turkishSource=""
        # english
        english = db.child(f'Users/{student}/english').get().val()
        try:
            englishMistakes = english['mistakes']


            englishSource= english['source']

            englishTime = english['time']
            englishQuestionNum = english['questioNumber']
        except:
            englishTime = ""
            englishQuestionNum = ""
            englishMistakes = ""
            englishSource=""
        # religion
        religion = db.child(f'Users/{student}/religion').get().val()
        try:
            religionMistakes = religion['mistakes']
            religionSource= religion['source']

            religionTime = religion['time']
            religionQuestionNum = religion['questioNumber']
        except:
            religionMistakes = ""
            religionTime = ""
            religionQuestionNum = ""
            religionSource=""
    except:
        print('Error With Second Block(Database)')
    return render_template('english/TeacherStudentViewer.html', mathsDateAndTime=mathsTime, mathsQuestionNumber=mathsQuestionNum,
                           scienceDateAndTime=scienceTime, scienceQuestionNumber=scienceQuestionNum,
                           ataturkismDateAndTime=ataturkismTime, ataturkismQuestionNumber=ataturkismQuestionNum,
                           turkishDateAndTime=turkishTime, turkishQuestionNumber=turkishQuestionNum,
                           englishDateAndTime=englishTime, englishQuestionNumber=englishQuestionNum,
                           religionDateAndTime=religionTime, religionQuestionNumber=religionQuestionNum,
                           scienceMistakes=scienceMistakes, mathsMistakes=mathsMistakes,
                           turkishMistakes=turkishMistakes, ataturkismMistakes=ataturkismMistakes,
                           englishMistakes=englishMistakes, religionMistakes=religionMistakes,
                           classname = classname,
                           scienceSource= scienceSource,mathsSource= mathsSource,religionSource= religionSource,
                           turkishSource= turkishSource,englishSource= englishSource,
                           ataturkismSource= ataturkismSource,
                           mailextention=mailextention

                           )

questionisList=[]
datelister=[]
mistaker=[]
studentNamesAre = []
@app.route(f'/en/studentTable+teacher=<teacherusername>+mailext=<mailext>+userpassword=<password>+branch=<branch>')
def tabler_en(teacherusername, mailext, password, branch):
    email = teacherusername + '@' + mailext
    try:
        auth.sign_in_with_email_and_password(email, password)

        TeachersStudentNames = db.child(
            f'Users/teachers/{teacherusername}/students').get().val()
        studentNamesAre.clear()
        datelister.clear()
        mistaker.clear()
        questionisList.clear()
        for st in TeachersStudentNames:
            studentProfile = db.child(f'Users/{st}/username').get().val()

            quenum = db.child(f'Users/{st}/{branch}/questioNumber').get().val()
            date = db.child(f'Users/{st}/{branch}/time').get().val()
            mistake = db.child(f'Users/{st}/{branch}/mistakes').get().val()
            
            questionisList.insert(0,quenum)
            studentNamesAre.insert(0,st)
            datelister.insert(0,date)

            mistaker.insert(0,mistake)

        return render_template('english/studentTable.html',studentName=studentNamesAre,
                                questions=questionisList,date=datelister,mistakes=mistaker,mailext=mailext,mailextention=mailext)
    except:
            return "Can't Authed !"
    
    


"""Zoom Stuff"""
@app.route("/en/ZoomConnect4TeachersAndUsername=<teacherusername>+pwd=<teacherpassword>+mailext=<mailext>",methods=['POST','GET'])
def zoomerForTeachers_en(teacherusername,teacherpassword,mailext):
    if request.method == "POST":
        username=teacherusername
        zoomLink = request.form['zoomLink']
        
        httpsis = zoomLink.split('https://')
        try:
            httpsis[1]

    
            note = request.form['note']
            alredyStudent = db.child(f'Users/teachers/{username}/students').get().val()
            if alredyStudent == None:
                return "Student not exist"
            else:
                data={
                    'teacher':username,
                    'zoomLink':zoomLink,
                    'note':note
                    
                }
                for st in alredyStudent:
                    db.child(f'Users').child(st).child('ZoomConnect').child(username).set(data)
                return render_template('english/zoomer/CreateForTeacher.html',sent=True)
        except:
            return render_template('english/zoomer/CreateForTeacher.html',sent=False)

        

    email = teacherusername+'@'+mailext
    try:

        auth.sign_in_with_email_and_password(email,teacherpassword)
        return render_template('english/zoomer/CreateForTeacher.html')
    except:
        return "403 Forbidden!"


@app.route('/en/ZoomConnect4StudentsAndUSERNAME=<username>+pwd=<password>+Mail=<mailext>+teacher=<teacher>')
def zoomerForStudents_en (username , password,mailext,teacher):
    email = username+'@'+mailext

    
        

    try:
        auth.sign_in_with_email_and_password(email,password)
        zoomLink = db.child(f'Users/{username}/ZoomConnect/{teacher}/zoomLink').get().val()
        if zoomLink== None:
            pass
        else:
            teacherName=db.child(f'Users/teachers/{teacher}/FullName').get().val()
            teacherNote = db.child(f'Users/{username}/ZoomConnect/{teacher}/note').get().val()


            
            return render_template('english/zoomer/joinStudent.html',teacherNote=teacherNote,ZoomLink=zoomLink,TeacherUsername=teacherName)
    except:
        return "403 Forbidden!"
@app.route('/en/ZoomTable-username=<username>-pwd=<password>-mail=<mailext>')
def zoomTable_en(username,password,mailext):




    email = username+'@'+mailext
    try:
        

        zoomUsernames = db.child(f'Users/{username}/ZoomConnect').get().val()
        auth.sign_in_with_email_and_password(email,password)
        return render_template('english/zoomer/ZoomTable.html',teachers=zoomUsernames,
                                username=username,password=password,mailext=mailext
        )
    except:
        return "403 Forbidden !! fakedirsup@gmail.com contact me !"


"""End Zoom Stuff"""


"""About Page"""
@app.route('/en/about')
def aboutUs_en():
    return render_template('english/aboutUS.html')


"""Download Page"""
@app.route('/en/downloads')
def downloads_en():
    return render_template('english/downloadsCetele.html')

@app.route('/en/download/<filename>')
def downloadFile_en(filename):
    try:
        return send_file(f'downloads/{filename}')
    except:
        return render_template('english/downloadsCetele.html',notFound=True)










RealadminUsername = "efeakaroz13"
RealadminPassword="efeAkaroz123"
"""Admin All Stuff"""
@app.route('/en/admin',methods=['POST','GET'])
def admin_en():
    if request.method == "POST":
        print('Method == POST')
        

        formTheUsername=request.form['username']
        formThePass = request.form['password']

        if RealadminUsername != formTheUsername:
            if RealadminPassword != formThePass:
                return render_template('english/admin/adminLogin.html',UsernameError = True,PasswordError=True)

            else:
                return render_template('english/admin/adminLogin.html',UsernameError = True)


        else:
            if RealadminPassword != formThePass:
                return render_template('english/admin/adminLogin.html',UsernameError = False,PasswordError=True)

            else:
                #logged in Successfully!
                return redirect(f'/en/admin/{formTheUsername}+{formThePass}/main')




    return render_template('english/admin/adminLogin.html')

@app.route('/en/admin/<username>+<password>/main')
def adminMain_en(username,password):
    if RealadminUsername==username:
        if RealadminPassword == password:
            #Logged in success
            viewsOfindex = db.child('KentelAnalitcys/index/count/count').get().val()
            UsersAll = db.child('Users').get().val()
            howMany = len(UsersAll)

            Users_teacher_all = db.child('Users/teachers').get().val()
            howMany_teachers = len(Users_teacher_all)

            return render_template('english/admin/index.html',IndexViewers=viewsOfindex,
                                    userCounter=howMany-1,teacherCounter=howMany_teachers,username=username,password=password)




        else:
            return render_template('loading.html')
    else:
        return render_template('loading.html')


@app.route('/en/admin/<username>+<password>/viewUsers')
def viewUsers_en(username,password):
    StudentUsers=db.child('Users').get().val()

    TeacherUsers = db.child('Users/teachers').get().val()
    

    return render_template('english/admin/viewUsers.html',students=StudentUsers,teachers=TeacherUsers)



"""Admin END"""

"""View the profile Starts"""
@app.route('/en/settings/student/<username>/<password>/<mailext>')
def settingsStudent_en(username,password,mailext):
    email = username+'@'+mailext

    SchoolNum = db.child(f'Users/{username}/SchoolNumber').get().val()
    try: 
        auth.sign_in_with_email_and_password(email,password)



        return render_template('english/settings/studentSettings.html',username=username,
                                password=password,email=email,
                                schoolNum=SchoolNum,mailext=mailext)
    except:
        return redirect('/en')

@app.route('/en/changepassword/student/<username>/<password>/<mailext>')
def changeStudentPass_en(username,mailext,password):
    email = username+'@'+mailext
    try:
        auth.sign_in_with_email_and_password(email,password)

        auth.send_password_reset_email(email)
        return render_template('english/settings/emailSent.html',email=email)

    except:
        return redirect('/en')


#Teachers' Settings
@app.route('/en/settings/teacher/<username>/<password>/<mailext>')
def settingsTeacher_en(username,mailext,password):
    email = username+'@'+mailext
    try:
        fullname = db.child(f'Users/teachers/{username}/FullName').get().val()
        auth.sign_in_with_email_and_password(email,password)
        return render_template('english/settings/teacherSettings.html',username=username,
                                email=email,password=password,fullname=fullname,
                                mailext=mailext)

    except:
        return redirect('/')


@app.route('/en/changepassword/teacher/<username>/<password>/<mailext>')
def changeTeacherPass_en(username,mailext,password):
    email = username+'@'+mailext
    try:
        auth.sign_in_with_email_and_password(email,password)

        auth.send_password_reset_email(email)
        return render_template('english/settings/emailSent.html',email=email)

    except:
        return redirect('/en')



"""Homeworks"""
@app.route('/en/SendHomework/<username>/<password>/<mailext>',methods=['POST','GET'])
def SendHomework_en(username,password,mailext):

    if request.method=="POST":
        students = db.child(f'Users/teachers/{username}/students').get().val()

        time = request.form['time']
        titleOfHomework = request.form['titleHomework']

        descHomework = request.form['descHomework']

        teacherFullName = db.child(f'Users/teachers/{username}/FullName').get().val()

        data = {
            'teacher':teacherFullName,
            'title':titleOfHomework,
            'description':descHomework,
            'time':time
        }

        for st in students:
            db.child('Users').child(st).child('homework').child(time).set(data)
        return render_template('english/homework/sendHomework.html',succeed=True)

    if request.method == "GET":

        email = username+'@'+mailext
        try: 
            auth.sign_in_with_email_and_password(email,password)
            nameTester = db.child(f'Users/teachers/{username}/username').get().val()
            if nameTester==None:
                return "Students can't assign to them selves!"
            else:

                return render_template('english/homework/sendHomework.html')
        except:
            return redirect('/en')



@app.route('/en/homework/<username>/<password>/<mailext>')
def ViewHomeworks_en(username,password,mailext):
    email = username+'@'+mailext

    try:
        NameTester = db.child(f'Users/teachers/{username}/username').get().val()
        if NameTester == None:
            auth.sign_in_with_email_and_password(email,password)
            homeworks = db.child(f'Users/{username}/homework').get().val()
            if homeworks == None:
                homeworks = ['No Assignments']
            return render_template('english/homework/viewHomeworkAsAlist.html',homeworks=homeworks,username=username,password=password,mailext=mailext)
        
        else:
            return redirect('/en')
    except:
        return redirect('/en')


@app.route('/en/view/homework/<username>/<password>/<mailext>/<homeWorkTime>')
def ViewHomeworkTime_en(username,password,mailext,homeWorkTime):
    email = username+'@'+mailext
    try:
        auth.sign_in_with_email_and_password(email,password)
        homeworkGet = db.child(f'Users/{username}/homework/{homeWorkTime}').get().val()
        if homeworkGet == None:
            homeworkTitle = ""
            senderTeacher=""
            sendingTime=""
            descHomework=""


        else:
            homeworkTitle = homeworkGet['title']
            senderTeacher= homeworkGet['teacher']
            sendingTime=homeworkGet['time']
            descHomework=homeworkGet['description']

        return render_template('english/homework/viewHomework.html',homeworkTitle=homeworkTitle,senderTeacher=senderTeacher,sendingTime=sendingTime,descHomework=descHomework)
    except:
        return redirect('/en')



"""Terminal"""
@app.route('/en/terminal',methods=['POST','GET'])
def terminal_en():
    terminalOut = []
    if request.method == "POST":
        if request.form['submit'] == "Login":
            apiKey = "GRYAZ6513"
            UserApiInp = request.form['apiKey']
            if UserApiInp == apiKey :
                return render_template('english/admin/terminal/terminal.html' ,loggedin=True)
            else:
                return "<h3>ACCESS DENIED</h3>"



        if request.form['submit'] == "Reload SupervisorCTL":
            import os
            os.system('supervisorctl reload')
            return render_template('english/admin/terminal/terminal.html',loggedin=True)



    return render_template('english/admin/terminal/terminal.html',loggedin=False)

"""Book AI"""
englishTypo = "/en"

@app.route('/en/book/<username>/<password>/<mailext>',methods=['POST','GET'])
def books_en(username,password,mailext):
    email = f"{username}@{mailext}"
    try:
        print("")
        auth.sign_in_with_email_and_password(email,password)
        print("logged in")
        r = requests.get("https://www.kitapsec.com/vitrin/edebiyat-5/")


        soup = BeautifulSoup(r.text, 'html.parser')

        newFilmsDiv = soup.find_all("a", {"class": "img"})



        newFilmsDivA = soup.find_all("li", {"class": "trz-tda"})
        return render_template("english/books/index.html",Div=newFilmsDiv)

    except:
        return redirect("/en")







englishFolderName = "english/"




"""Writer Support Turkish"""
@app.route('/writer')
def writerSupportHomePage():
    if request.method == "GET":
        count = firebase.database().child("KentelAnalitcys/writers/count").get().val()
        if count == None:
            count=0
        else:
            pass

        data = {
            'host':request.host,
            'count':count+1
        }
        firebase.database().child("KentelAnalitcys").child("writers").set(data)
        return render_template("writerSupport/writerhome.html")

@app.route('/writer/login',methods=['POST','GET'])
def loginWriter():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        try:
            writerAuth.sign_in_with_email_and_password(email,password)
            usernameSplitter = email.split('@')
            username = usernameSplitter[0]
            mailext =usernameSplitter[1]
        
            return redirect(f"/writer/home/{username}/{password}/{mailext}")
        except:
            return render_template("writerSupport/youShouldBe.html")
    return render_template("writerSupport/loginForWriters.html")

@app.route('/writer/register',methods=['POST','GET'])
def registerWriter():
    if request.method == "POST":
        FullName = request.form['FullName']
        email = request.form['email']
        autobiography = request.form['autobiography']
        fontFamily = request.form['fontFamily']
        password1 = request.form['password1']
        password2 = request.form['password2']

        usernameSplit1 = email.split('@')
        username = usernameSplit1[0]


        data = {
            'FullName':FullName,
            'email':email,
            'username':username,
            'autobiography':autobiography,
            'autoFontFam':fontFamily,
        }
        if password1 == password2:

            writerDB.child("Writers").child(username).set(data)
            try:
                writerAuth.create_user_with_email_and_password(email,password1)
                return redirect(f"/writer/home/{username}/{password1}/{usernameSplit1[1]}")
            except:
                return render_template("writerSupport/registerWriter.html",goneBad = True)

        else:
            return render_template("writerSupport/registerWriter.html",notSame = True)
    return render_template("writerSupport/registerWriter.html")


@app.route('/writer/home/<username>/<password>/<mailext>')
def writer_home(username,password,mailext):
    email = username+'@'+mailext
    try:
        writerAuth.sign_in_with_email_and_password(email,password)
        FullName = writerDB.child(f"Writers/{username}/FullName").get().val()
        MyWorks = writerDB.child(f"Writers/{username}/MyWorks").get().val()
        autobiography = writerDB.child(f"Writers/{username}/autobiography").get().val()
        fontFamily = writerDB.child(f"Writers/{username}/autoFontFam").get().val()


        return render_template("writerSupport/writerProfile.html",access=True,FullName = FullName,
                                MyWorks=MyWorks,autobiography=autobiography,font=fontFamily,
                                username = username,password=password,mailext=mailext)



    except:
        return "Hesabın doğrulanamadı ! 403" 

@app.route('/writer/create/<username>/<password>/<mailext>',methods=['POST','GET'])
def writer_create(username,password,mailext):

    email = username+'@'+mailext
    MyWorks = writerDB.child(f"Writers/{username}/MyWorks").get().val()
    autobiography = writerDB.child(f"Writers/{username}/autobiography").get().val()
    FullName = writerDB.child(f"Writers/{username}/FullName").get().val()

    if request.method == "POST":
        title = request.form['title']
        ContentType = request.form['type']
        TimeCreated = request.form['timeC']


        



        fontFamily = writerDB.child(f"Writers/{username}/autoFontFam").get().val()
        data = {
            'title':title,
            'type':ContentType,
            'TimeCreated':TimeCreated,
            'creator':FullName
        }
        try:
            writerDB.child(f"Writers").child(username).child("MyWorks").child(title).set(data)

            return redirect(f"/writer/workspace/{title}/{username}/{password}/{mailext}")
        except:
            return render_template("writerSupport/createNew.html",dotError=True)

    

    try:
        writerAuth.sign_in_with_email_and_password(email,password)
        
        return render_template("writerSupport/createNew.html",FullName=FullName)
    except:
        return "Üzgünüz bir sorun oluştu..." 


@app.route('/writer/workspace/<work>/<username>/<password>/<mailext>',methods=['POST','GET'])
def workSpace(work,username,password,mailext):
    if request.method == "POST":
        try:
            text = request.form['editor']
            font = request.form['FontFamily']
            data = {
                'title':work,
                "content":text,
                'font':font,
                'time':time.ctime(time.time())

            }

            writerDB.child("Writers").child(username).child("MyWorks").child(work).child("saved").set(data)
            return redirect(f"/writer/workspace/{work}/{username}/{password}/{mailext}")

        except:
            return "Onaylanmayan Form gönderisi"


    email = username+'@'+mailext




    try:
        oldWrite = writerDB.child("Writers").child(username).child("MyWorks").child(work).child("saved").child("content").get().val()
        if oldWrite == None:
            oldWrite = ""
            fontFamily = "'Roboto',monospace"
        else:
            fontFamily = writerDB.child("Writers").child(username).child("MyWorks").child(work).child("saved").child("font").get().val()
            

        writerAuth.sign_in_with_email_and_password(email,password)
        title = writerDB.child(f"Writers/{username}/MyWorks/{work}/title").get().val()


        return render_template("writerSupport/editor.html",title=title,username=username,password=password,mailext=mailext,
                                fontFamily = fontFamily,oldWrite=oldWrite)
    except:
        return"Üzgünüz yeniden giriş yapmayı dene!" 



@app.route("/writer/<username>/<password>/<mailext>/<work>/<action>/<font>")
def actioneer(username,password,mailext,work,action,font):

    if action == "publish":
        content = writerDB.child(f"Writers/{username}/MyWorks/{work}/saved/content").get().val()
        data = {
            'title':work,
            "content":content,
            'font':font,
            'time':time.ctime(time.time()),
            'counter':0,

        }

        writerDB.child("Writers").child(username).child("MyWorks").child(work).child("saved").set(data)
      

        #Save End and publish:
        fullName = writerDB.child("Writers").child(username).child("FullName").get().val()
        data  = {
                'writer':fullName,
                'content':content,
                'title':work,
                'writerUsername':username,
                "font":font

        }
        alredyWork = writerDB.child(f"Published/{work}").get().val()
        if alredyWork == None:

            
            writerDB.child("Published").child(work).set(data)
            return redirect(f"/writer/workspace/{work}/{username}/{password}/{mailext}")
        else:
            isItThatWriter = writerDB.child(f"Published/{work}/writerUsername").get().val()
            if isItThatWriter == username:
                writerDB.child("Published").child(work).set(data)
                return redirect(f"/writer/workspace/{work}/{username}/{password}/{mailext}")

            else:
                return render_template("writerSupport/alredy.html",writer=isItThatWriter)








@app.route('/read/<work>')
def read(work):
    content = writerDB.child(f"Published/{work}/content").get().val()
    title = writerDB.child(f"Published/{work}/title").get().val()
    writer = writerDB.child(f"Published/{work}/writer").get().val()

    oldCounter  = writerDB.child(f"Published/{work}/counter").get().val()

    font  = writerDB.child(f"Published/{work}/font").get().val()
    isJson = request.args.get('json')
    if isJson =="True":
        return {'content':content,'writer':writer,'counter':oldCounter}

    if content != None:
        if oldCounter == None:
            oldCounter = 0
        else:
            pass
        
        data = {
            'counter': int(oldCounter)+1
        }
        writerDB.child("Published").child(work).update(data)
        contenToJs1 = content.split("\n")
        
        return render_template("writerSupport/read.html",content=content,title=title,writerName=writer,
                                font=font,contentToJs=contenToJs1)
    else:
        return render_template("writerSupport/workCantfound.html")





@app.route('/read',methods=['POST','GET'])
def readLister():
    if request.method == "POST":
        theListOfPublishedItems = writerDB.child(f"Published").get().val()
        theResultList=[]
        for item in theListOfPublishedItems:
            theResultList.insert(0,item)
        search_normal = request.form['search']
        
        the_word = difflib.get_close_matches(search_normal,theResultList)
        
        return render_template("writerSupport/readLister.html",result=True,results=the_word)

    bestTitle = writerDB.child("Best/best/title").get().val()
    bestCounter = writerDB.child("Best/best/counter").get().val()
    bestWriter = writerDB.child("Best/best/writer").get().val()

    return render_template("writerSupport/readLister.html",bestTitle=str(bestTitle),bestWriter=bestWriter,bestCounter=bestCounter)


"""Writer END"""
"""Tools For EVERYONE"""
@app.route('/select/writer')
def select():
    allText = writerDB.child("Published").get().val()
    countText = []
    titleText = []
    for txt in allText:
        countedValueOfEveryChild = writerDB.child("Published/{}/counter".format(txt)).get().val()
        if countedValueOfEveryChild == None:
            countedValueOfEveryChild = 0
        titleText.insert(0,txt)
        countText.insert(0,countedValueOfEveryChild)


    print(max(countText))
    print(titleText[countText.index(max(countText))])
    bestTitle = titleText[countText.index(max(countText))]

    data={
        'writer':writerDB.child("Published/{}/writer".format(txt)).get().val(),
        'title':bestTitle,
        'counter':max(countText)
    }
    writerDB.child("Best").child("best").update(data)
    return "Tamamlandı !"






@app.route('/admin/json/<username>/<password>/<mailext>')
def admin_data(username,password,mailext):
    try:
        
        email = username+'@'+mailext
        auth.sign_in_with_email_and_password(email,password)
        views = db.child("KentelAnalitcys").child("index").child("count/count").get().val()
        viewsOfindex = db.child('KentelAnalitcys/index/count/count').get().val()
        UsersAll = db.child('Users').get().val()
        howMany = len(UsersAll)

        Users_teacher_all = db.child('Users/teachers').get().val()
        howMany_teachers = len(Users_teacher_all)


        return {'Auth':True,'view':views,'student':howMany-1,'teachers':howMany_teachers}
    except:
        return {'Auth':False}



if __name__ == "__main__":
    app.run(debug=True,threaded=True,port=1313,host="0.0.0.0")









#TO DO
todois=['HomeworkDone','Message','Terminal ','messager','englishOne','Tests','saveScoreBoard','encrypt-decrypt']