from flask import Flask,render_template,url_for, redirect,request
import Gmailmain

app = Flask(__name__)


@app.route('/success/<name>/<query>/<date>') 
def success(name,query,date): 
        print(date)
        Gmailmain.main(query,date)
        f = open('Email.txt','r')
        f1 = f.readlines()
        for line in f1:
                print(line)
        return render_template('sucess.html',data= f1)

@app.route('/')
def Home_page():
        return render_template('index.html')

@app.route('/login',methods=['POST','GET'])
def Second_page():
        if request.method=="POST":
                user = request.form['username']
                subject = request.form['Query']
                date = request.form['date']
                return redirect(url_for('success',name = user,query =subject,date = date))

if __name__ == '__main__':
    app.run()
