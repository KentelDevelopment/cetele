from flask import Flask ,render_template,request,redirect
import pyrebase


app = Flask(__name__)



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



app = Flask(__name__)

RealadminUsername = "efeakaroz13"
RealadminPassword="efeAkaroz123"

@app.route('/',methods=['POST','GET'])
def index():
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

@app.route('/SendHomework/<username>/<password>/<mailext>',methods=['POST','GET'])
def SendHomework(username,password,mailext):

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
        return render_template('homework/sendHomework.html',succeed=True)

    if request.method == "GET":

        email = username+'@'+mailext
        try: 
            auth.sign_in_with_email_and_password(email,password)
            nameTester = db.child(f'Users/teachers/{username}/username').get().val()
            if nameTester==None:
                return "Öğrenciler Kendilerine Ödev yazamazlar!"
            else:

                return render_template('homework/sendHomework.html')
        except:
            return redirect('/')





    
app.run(debug=True,port="80")