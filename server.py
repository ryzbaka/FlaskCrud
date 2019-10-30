from flask import Flask,render_template,jsonify,request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import os

#app init
app=Flask(__name__)
#db init
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'demo.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    rollno=db.Column(db.String(8),unique=True)
    name=db.Column(db.String(20))
    def __init__(self,rollno,name):
        self.rollno=rollno
        self.name=name
#schema init
ma=Marshmallow(app)
class StudentSchema(ma.Schema):
    class Meta:
        fields=['rollno','name']
student_schema=StudentSchema()
students_schema=StudentSchema(many=True)
#ROUTING#
@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/send_details",methods=['POST'])
def submit_details():
    rollno=request.json["rollno"]
    name=request.json["name"]
    newStudent=Student(rollno,name)
    db.session.add(newStudent)
    db.session.commit()
    return student_schema.jsonify(newStudent)

@app.route("/get_all_students",methods=["GET"])
def get_students():
    students=Student.query.all()
    result=students_schema.dump(students)
    return jsonify(result)

@app.route("/get_student<id>",methods=["GET"])
def get_student(id):
    student=Student.query.get(id)
    return student_schema.jsonify(student)

@app.route("/update_student<id>",methods=["POST"])
def update_student(id):
    student=Student.query.get(id)
    student.rollno=request.json["rollno"]
    student.name=request.json["name"]
    db.session.commit()
    return student_schema.jsonify(student)

@app.route("/delete_student<id>",methods=["DELETE"])
def delete_student(id):
    student=Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return student_schema.jsonify(student)

if __name__=='__main__':
    app.run(port=3000,debug=True)