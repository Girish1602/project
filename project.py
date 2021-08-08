from flask import Flask,request,render_template,session,url_for,redirect,flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

app.secret_key="flask testing"
app.permanent_session_lifetime = timedelta(minutes=5)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


class users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(20), unique=True, nullable=False)
    mail_id = db.Column(db.String(20),unique=True,nullable=False)
    contact_num = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(20),nullable=False)

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/adduser', methods =["POST","GET"])
def adduser():
    if request.method == 'POST':
        email= request.form["email"]
        name= request.form["name"]
        pass1 = request.form["password"]
        pass2 = request.form["password-repeat"]
        num = request.form["number"]
        found_user = users.query.filter_by(mail_id = email).first()
        if found_user:
            flash("this email is already registred")
            return render_template("adduser.html")
        else:
            if pass1 == pass2 :
                usr = users(Username=name,mail_id = email,password= pass1, contact_num=num)
                db.session.add(usr)
                db.session.commit()
                session.permanent = True
                session["name"]=name
                session["mail_id"]= email
                return render_template("user.html",name=name)
            else:
                flash("passwords do not match")
                return render_template("adduser.html")
    return render_template("adduser.html")


@app.route("/login", methods=[ "POST","GET" ] )
def login():
    if request.method == "POST":
        email = request.form["email"]
        psw = request.form["password"]
        user = users.query.filter_by(mail_id = email).first()
        if user:
            psw_temp = user.password
            if psw == psw_temp:
                session["user"] = user.Username
                return render_template("user.html",name=user.Username)
            else:
                flash("incorrect password!")
                return render_template("login.html")
        else:
            flash("email not found!")
            return render_template("login.html")
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)