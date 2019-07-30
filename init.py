from flask import Flask,render_template,url_for,jsonify,request,Response,session,redirect,flash
from dbmodels import *
from passlib.hash import sha256_crypt
from random import randint
from flask_mail import Mail,Message
from datetime import datetime
import bitarray
from static_function import *
from flask_migrate import Migrate
from datetime import datetime,timedelta
from functools import wraps
from ast import literal_eval


app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:mom0511@localhost/myparliament"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
db.app=app
migrate = Migrate(app, db)


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='example@example.com'
app.config['MAIL_PASSWORD']='***********'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		try:
			if session["logged_in"]:
				return f(*args, **kwargs)
			else:
				return redirect("/get/login")
		except:
			return redirect("/get/login")
	return wrap

def admin_login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		try:
			if session["logged_in"] and session["username"]=="manishpandey8858@gmail.com":
				return f(*args, **kwargs)
			else:
				return redirect("/get/login")
		except:
			return redirect("/get/login")
	return wrap


def GetUserInfo():
	current_user=session["username"]
	data=User_details.query.filter_by(email=current_user).first()
	return data


nav_value=["Login","/get/login"]
nav_value_logged_in=["Dashboard","/dashboard"]


def if_login():
	try:
		if session["logged_in"]:
			return nav_value_logged_in
		else:
			return nav_value
	except:
		return nav_value


@app.route("/")
def Home():
	try:
		if session["logged_in"]:
			return redirect(url_for("Dashboard"))
		else:
			return render_template("home.html",nav_value=if_login())
	except:
		return render_template("home.html",nav_value=if_login())


@app.route("/dashboard/my-course")
@login_required
def Dashboard_courses():
	courses=Courses.query.limit(25).all()
	user=GetUserInfo()
	enrolled_course=user.registered_in_courses
	return render_template("dashboard_course.html",enrolled_course=enrolled_course,courses=courses)

@app.route("/dashboard/my-olympiads")
@login_required
def Dashboard_olympiads():
	olympiads=Olympiad_details.query.limit(25).all()
	user=GetUserInfo()
	enrolled_olympiads=user.registered_in_olympiads
	return render_template("dashboard_olympiads.html",enrolled_olympiads=enrolled_olympiads,olympiads=olympiads)

@app.route("/dashboard/my-event")
@login_required
def Dashboard_events():
	events=Event_details.query.limit(25).all()
	user=GetUserInfo()
	enrolled_events=user.registered_in_events
	return render_template("dashboard_event.html",enrolled_events=enrolled_events,events=events)


@app.route("/starttheolympiad/<int:olympiad_id>")
@admin_login_required
def starttheolympiad(olympiad_id):
	olympiad=Olympiad_details.query.filter_by(oly_id=olympiad_id).first()
	olympiad.status=1
	db.session.commit()
	return "Done"


@app.route("/endtheolympiad/<int:olympiad_id>")
@admin_login_required
def endtheolympiad(olympiad_id):
	olympiad=Olympiad_details.query.filter_by(oly_id=olympiad_id).first()
	olympiad.status=2
	db.session.commit()
	return "Done"


@app.route("/courses-all")
def All_Courses():
	courses=Courses.query.limit(25).all()
	return render_template("courses.html",courses=courses,nav_value=if_login())

@app.route("/event-all")
def All_Events():
	events=Event_details.query.limit(25).all()
	return render_template("events.html",events=events,nav_value=if_login())

@app.route("/olympiad-all")
def All_Olympiads():
	olympiads=Olympiad_details.query.limit(25).all()
	return render_template("olympiad.html",olympiads=olympiads,nav_value=if_login())

@app.route("/add-course-page")
@admin_login_required
def get_admin_add_course():
	courses=Courses.query.all()
	olympiads=Olympiad_details.query.all()
	return render_template("admin_add_course.html",courses=courses,olympiads=olympiads)


@app.route("/add-lecture-page",methods=["GET","POST"])
@admin_login_required
def add_lecture_page():
	if request.method=="POST":
		course_id=request.form["course_id"]
		course=Courses.query.filter_by(course_id=course_id).first()
		return render_template("add_lecture.html",course=course)
	else:
		flash("Method Not Allowed")
		return redirect("/")



@app.route("/add-course",methods=["GET","POST"])
@admin_login_required
def Add_Course():
	try:
		if request.method=="POST":
			name=request.form["name"]
			author=request.form["author"]
			duration=request.form["duration"]
			fees=request.form["fees"]
			demolink=request.form["demolink"]
			description=request.form["description"]
			new_course=Courses(name=name,author=author,duration=duration,fees=fees,demo_link=demolink,description=description)
			db.session.add(new_course)
			db.session.commit()
			return redirect(url_for("get_admin_add_course"))
	except Exception as e:
		return redirect("/")

@app.route("/add-olympiad",methods=["GET","POST"])
@admin_login_required
def Add_Olympiad():
	try:
		if request.method=="POST":
			name=request.form["name"]
			organizer=request.form["organizer"]
			duration=request.form["duration"]
			fees=request.form["fees"]
			rules=request.form["rules"]
			description=request.form["description"]
			new_oly=Olympiad_details(name=name,organiser=organizer,duration=duration,fees=fees,rules=rules,description=description)
			db.session.add(new_oly)
			db.session.commit()
			return redirect(url_for("get_admin_add_course"))
	except Exception as e:
		return redirect("/")
@app.route("/add-event",methods=["GET","POST"])
def Add_event():
	try:
		if request.method=="POST":
			name=request.form["name"]
			organizer=request.form["organizer"]
			duration=request.form["duration"]
			fees=request.form["fees"]
			description=request.form["description"]
			start_date=request.form["start_date"]
			end_date=request.form["end_date"]
			new_event=Event_details(name=name,organiser=organizer,duration=duration,fees=fees,description=description,start_date=start_date,end_date=end_date)
			db.session.add(new_event)
			db.session.commit()
			return redirect(url_for("get_admin_add_course"))
	except Exception as e:
		return redirect("/")

@app.route("/add-question",methods=["GET","POST"])
@admin_login_required
def Add_Question():
	try:
		if request.method=="POST":
			olympiad_id=request.form["olympiad_id"]
			oly=Olympiad_details.query.filter_by(oly_id=olympiad_id).first()
			question=request.form["Question"]
			optA=request.form["optA"]
			optB=request.form["optB"]
			optC=request.form["optC"]
			optD=request.form["optD"]
			correctopt=request.form["correctopt"]
			new_question=Questions(question=question,optA=optA,optB=optB,optC=optC,optD=optD,correctopt=correctopt)
			db.session.add(new_question)
			oly.questions.append(new_question)
			db.session.commit()
			return redirect(url_for("get_admin_add_course"))
	except Exception as e:
		return redirect("/")



@app.route("/add-week",methods=["GET","POST"])
@admin_login_required
def Add_Week():
	try:
		if request.method=="POST":
			title=request.form["title"]
			course_id=request.form["course_id"]
			link=request.form["link"]
			link=link.split("/")[-1]
			description=request.form["description"]
			cour=Courses.query.filter_by(course_id=course_id).first()
			new_week=Week()
			db.session.add(new_week)
			cour.weeks.append(new_week)
			lecture=Lecture_details(title=title,link=link,description=description)
			new_week.lectures.append(lecture)
			db.session.commit()
			return redirect("/add-course-page")
	except Exception as e:
		return redirect("/")


@app.route("/add-lecture/<int:course_id>",methods=["GET","POST"])
@admin_login_required
def Add_Lecture(course_id):
	try:
		if request.method=="POST":
			week_id=request.form["week"]
			title=request.form["title"]
			link=request.form["link"]
			description=request.form["description"]
			link=link.split("/")[-1]
			week=Week.query.filter_by(week_id=week_id).first()
			lecture=Lecture_details(title=title,link=link,description=description)
			week.lectures.append(lecture)
			db.session.commit()
			return redirect("/add-course-page")
	except Exception as e:
		return redirect("/")

@app.route("/pay-now/<string:type>/<int:p_id>")
def Pay_now(type,p_id):
	return render_template("payment.html",type=type,p_id=p_id)

@app.route("/complete-payment/<string:type>/<int:p_id>",methods=["GET","POST"])
def Complete_payment(type,p_id):
	if request.method=="POST":
		file=request.files["proof"]
		flash("Please Wait for verification!!!")
		return redirect("/"+type+"-details/"+str(p_id))
	else:
		flash("Something Went Wrong")
		return redirect("/"+type+"-details/"+str(p_id))


@app.route("/dashboard")
@login_required
def Dashboard():
	try:
		user=GetUserInfo()
		courses=user.registered_in_courses
		events=user.registered_in_events
		olympiads=user.registered_in_olympiads
		return render_template("dashboard.html",courses=courses,events=events,olympiads=olympiads,name=user.name)
	except Exception as e:
		return render_template("error.html",message="Some Thing Went Wrong!!!")

@app.route("/course-enroll/<int:course_id>")
def Course_Enrollment(course_id):
	try:
		if session["logged_in"]:
			user=GetUserInfo()
			course=Courses.query.filter_by(course_id=course_id).first()
			register=Registered_Courses()
			db.session.add(register)
			course.subscribers.append(register)
			user.registered_in_courses.append(register)
			db.session.commit()
			flash("Enrolled To This course!!!")
			return redirect("/pay-now/course/"+str(course_id))
		else:
			flash("Please Login!!!")
			return redirect("/course-content/"+str(course_id))
	except:
		flash("Please login!!!")
		return redirect("/course-content/"+str(course_id))

@app.route("/event-enroll/<int:event_id>")
def Event_Enrollment(event_id):
	try:
		if session["logged_in"]:
			user=GetUserInfo()
			event=Event_details.query.filter_by(event_id=event_id).first()
			register=Registered_Events()
			db.session.add(register)
			event.subscribers.append(register)
			user.registered_in_events.append(register)
			db.session.commit()
			flash("Enrolled To This Event!!!")
			return redirect("/pay-now/event/"+str(event_id))
		else:
			flash("Please Login!!!")
			return redirect("/event-details/"+str(event_id))
	except:
		flash("Please login!!!")
		return redirect("/event-details/"+str(event_id))




@app.route("/olympiad-enroll/<int:oly_id>")
def Olympiad_Enrollment(oly_id):
	try:
		if session["logged_in"]:
			user=GetUserInfo()
			olympiad=Olympiad_details.query.filter_by(oly_id=oly_id).first()
			if olympiad.status==1:
				flash("Olympiad Started!!!")
				return redirect("/olympiad-details/"+str(oly_id))
			elif olympiad.status==2:
				flash("Olympiad Over!!!")
				return redirect("/olympiad-details/"+str(oly_id))
			register=Registered_Olympiads()
			db.session.add(register)
			olympiad.subscribers.append(register)
			user.registered_in_olympiads.append(register)
			db.session.commit()
			flash("Enrolled To This Olympiad!!!")
			return redirect("/pay-now/olympiad/"+str(oly_id))
		else:
			flash("Please Login!!!")
			return redirect("/olympiad-details/"+str(oly_id))
	except:
		flash("Please login!!!")
		return redirect("/olympiad-details/"+str(oly_id))



@app.route("/get-enrollment-in-course/<int:course_id>")
def Get_Enrollment_in_course(course_id):
	try:
		if session["logged_in"]:
			user=GetUserInfo()
			course=Courses.query.filter_by(course_id=course_id).first()
			registered=Registered_Courses.query.filter_by(course_id=course_id,user_id=user.user_id).all()
			if len(registered)>0:
				if registered[0].payment_done:
					return jsonify(valid=True,link="#",data="Enrolled")
				else:
					return jsonify(valid=True,link="/pay-now/course/"+str(course_id),data="Pay Now")
			else:
				return jsonify(valid=True,link="/course-enroll/"+str(course_id),data="Enroll Now")
		else:
			return jsonify(valid=False,link="/course-enroll/"+str(course_id),data="Enroll Now")
	except:
		return jsonify(valid=False,link="/course-enroll/"+str(course_id),data="Enroll Now")

@app.route("/get-enrollment-in-olympiad/<int:oly_id>")
def Get_Enrollment_in_olympiad(oly_id):
	try:
		if session["logged_in"]:
			user=GetUserInfo()
			olympiad=Olympiad_details.query.filter_by(oly_id=oly_id).first()
			registered=Registered_Olympiads.query.filter_by(oly_id=oly_id,user_id=user.user_id).all()
			if len(registered)>0:
				if registered[0].payment_done:
					return jsonify(valid=True,link="/start-olympiad-"+str(oly_id)+"-0",data="Enrolled")
				else:
					return jsonify(valid=True,link="/pay-now/olympiad/"+str(oly_id),data="Pay Now")
			else:
				return jsonify(valid=True,link="/olympiad-enroll/"+str(oly_id),data="Enroll Now")
		else:
			return jsonify(valid=False,link="/olympiad-enroll/"+str(oly_id),data="Enroll Now")
	except:
		return jsonify(valid=False,link="/olympiad-enroll/"+str(oly_id),data="Enroll Now")



@app.route("/course-details/<int:course_id>")
def Course_Detail(course_id):
	weeks=Courses.query.filter_by(course_id=course_id).first().weeks
	return render_template("course_Det.html",weeks=weeks,course_id=course_id,nav_value=if_login())

@app.route("/olympiad-details/<int:olympiad_id>")
def Olympiad_Detail(olympiad_id):
	olympiad=Olympiad_details.query.filter_by(oly_id=olympiad_id).first()
	return render_template("olympiad_start.html",olympiad=olympiad,nav_value=if_login())

@app.route("/event-details/<int:event_id>")
def Event_Detail(event_id):
	event=Event_details.query.filter_by(event_id=event_id).first()
	return render_template("event_details.html",event=event,nav_value=if_login())


@app.route("/start-olympiad-<int:oly_id>-<int:question_no>")
def Start_olympiad(oly_id,question_no):
	try:
		if session["logged_in"]:
			user=GetUserInfo()
			olympiad=Olympiad_details.query.filter_by(oly_id=oly_id).first()
			if olympiad.status==0:
				flash("Not Yet Started!!!")
				return redirect("/olympiad-details/"+str(oly_id))
			elif olympiad.status==2:
				flash("Olympiad Over!!!")
				return redirect("/olympiad-details/"+str(oly_id))
			registered=Registered_Olympiads.query.filter_by(oly_id=oly_id,user_id=user.user_id).all()
			if len(registered)>0:
				if registered[0].status:
					flash("You Have Already Participated!!!")
					return redirect("/olympiad-details/"+str(oly_id))
				if registered[0].payment_done:
					question=olympiad.questions[question_no]
					return render_template("olympiad_questions.html",score=registered[0].final_score,question=question,next=question_no+1,prev=question_no-1,olympiad=olympiad,nav_value=if_login())
				else:
					flash("Payment Not Done")
					return redirect("/olympiad-details/"+str(oly_id))
			else:
				flash("Not Registered")
				return redirect("/olympiad-details/"+str(oly_id))
		else:
			flash("Please Login")
			return redirect("/olympiad-details/"+str(oly_id))
	except:
		flash("Please Login")
		return render_template("/olympiad-details/"+str(oly_id))

@app.route("/submit-olympiad-<int:oly_id>-<int:question_no>",methods=["GET","POST"])
def Submit_olympiad(oly_id,question_no):
	try:
		if session["logged_in"]:
			user=GetUserInfo()
			olympiad=Olympiad_details.query.filter_by(oly_id=oly_id).first()
			if olympiad.status==0:
				flash("Not Yet Started!!!")
				return redirect("/olympiad-details/"+str(oly_id))
			elif olympiad.status==2:
				flash("Olympiad Over!!!")
				return redirect("/olympiad-details/"+str(oly_id))
			registered=Registered_Olympiads.query.filter_by(oly_id=oly_id,user_id=user.user_id).all()
			if len(registered)>0:
				if registered[0].status:
					flash("You Have Already Participated!!!")
					return redirect("/olympiad-details/"+str(oly_id))
				if registered[0].payment_done:
					ques=request.form["ques"]
					registered[0].answers+=str((str(question_no-1),ques))+","
					question=olympiad.questions[question_no-1]
					if question.correctopt==ques:
						registered[0].final_score+=10
						db.session.commit()
					db.session.commit()
					if question_no==len(olympiad.questions):
						registered[0].status=True
						db.session.commit()
						flash("Complete")
						return redirect("/")
					question=olympiad.questions[question_no]
					return render_template("olympiad_questions.html",score=registered[0].final_score,question=question,next=question_no+1,prev=question_no-1,olympiad=olympiad,nav_value=if_login())
				else:
					flash("Payment Not Done")
					return redirect("/olympiad-details/"+str(oly_id))
			else:
				flash("Not Registered")
				return redirect("/olympiad-details/"+str(oly_id))
		else:
			flash("Please Login")
			return redirect("/olympiad-details/"+str(oly_id))
	except:
		flash("Please Login")
		return render_template("/olympiad-details/"+str(oly_id))



@app.route("/course-content/<int:course_id>")
def Course_content(course_id):
	details=Courses.query.filter_by(course_id=course_id).first()
	return render_template("course_cont.html",course=details)


@app.route("/getlecture/<int:lecture_id>-<int:course_id>")
def Get_Lecture(lecture_id,course_id):
	try:
		if session["logged_in"]:
			user=GetUserInfo()
			course=Courses.query.filter_by(course_id=course_id).first()
			registered=Registered_Courses.query.filter_by(course_id=course_id,user_id=user.user_id).all()
			if len(registered)>0:
				if registered[0].payment_done:
					details=Lecture_details.query.filter_by(lecture_id=lecture_id).first()
					return render_template("lecture_cont.html",lecture=details)
				else:
					flash("Please Complete Your Payment")
					return redirect("/course-content/"+str(course_id))
			else:
				flash("Not Enrolled PLEASE Enroll To This course!!!")
				return redirect("/course-content/"+str(course_id))
		else:
			flash("Please login!!!")
			return redirect("/course-content/"+str(course_id))
	except:
		flash("Please Login!!!")
		return redirect("/course-content/"+str(course_id))

@app.route("/signup",methods=["GET","POST"])
def signup():
	try:
		if request.method=="POST":
			name=request.form['name']
			email=request.form['email']
			passwd=sha256_crypt.encrypt((request.form['passwd']))
			if len(User_details.query.filter_by(email=email).all())>0:
				#flash("This Email Is Already Registered!!!")
				return redirect("/get/sign")
			new_user=User_details(name=name,email=email,password=passwd,contact_no=53,verified=False)
			db.session.add(new_user)
			msg=Message('From MyParliament',sender='myparliament@myparliament.org',recipients=[email])
			while True:
				otp=randint(100000,999999)
				if len(Otp_details.query.filter_by(otp_no=otp).all())==0:
					break
			msg.body="Your otp for signup: "+str(otp)
			otp_obj=Otp_details(user_id=new_user.user_id,otp_no=otp,purpose=1,valid_till=datetime.now()+timedelta(hours=1))
			db.session.add(otp_obj)
			#mail.send(msg)
			db.session.commit()
			return render_template("otp_verify.html",uid=new_user.user_id)
		else:
			return redirect("/signup")
	except Exception as e:
		return render_template("error.html",message="Some Error occured.")

@app.route("/verify/<int:uid>",methods=["GET","POST"])
def Verify(uid):
	try:
		if request.method=="POST":
			otp=int(request.form["otp"])
			user_verify=Otp_details.query.filter_by(user_id=uid).first()
			if user_verify.valid_till>datetime.now() and user_verify.purpose==1 and user_verify.otp_no==otp:
				user=User_details.query.filter_by(user_id=uid).first()
				user.verified=True
				db.session.commit()
				db.session.delete(user_verify)
				db.session.commit()
				session['logged_in']=True
				session['username']=user.email
				return redirect(url_for("Dashboard"))
			else:
				return "No"
				flash("Wrong OTP or OTP Expired!!!")
				return render_template("otp_verify.html",uid=uid)
		else:
			flash("Method Not Allowed")
			return render_template("home.html")
	except Exception as e:
		return render_template("error.html",message="Some error occured!!!")

@app.route("/dashboard/courses/register/<int:cid>")
@login_required
def register_course(cid):
	try:
		user=GetUserInfo()
		course=Courses.query.filter_by(course_id=cid).first()
		course.subscribed_cusers.append(user)
		db.session.commit()
		flash("Registered for "+course.name)
		return redirect("/dashboard/courses/course_home/"+cid)
	except Exception as e:
		return render_template("error.html",message="Some Error occured.")

@app.route("/dashboard/registered_courses")
@login_required
def registered_courses():
	user=GetUserInfo()
	courses=user.courses
	return render_template("registered.html",courses)


@app.route("/dashboard/olympiads/register/<int:oid>")
@login_required
def register_olympiad(oid):
	try:
		user=GetUserInfo()
		olympiad=Olympiad_details.query.filter_by(oly_id=oid).first()
		olympiad.participated_by.append(user)
		db.session.commit()
		flash("Registered for the "+olympiad.name)
		return redirect("/dashboard/olympiads/olympiad_home/"+oid)
	except Exception as e:
		return render_template("error.html",message="Some Error occured.")

@app.route("/dashboard/registered_olympiads")
@login_required
def registered_olympiads():
	user=GetUserInfo()
	olympiad=user.olympiads
	return render_template("registered.html",olympiad)


@app.route("/dashboard/events/register/<int:eid>")
@login_required
def register_event(eid):
	try:
		user=GetUserInfo()
		event=Event_details.query.filter_by(event_id=eid).first()
		event.subscribed_eusers.append(user)
		db.session.commit()
		flash("Registered for the "+event.name)
		return redirect("/dashboard/events/event_home/"+eid)
	except Exception as e:
		return render_template("error.html",message="Some Error occured.")

@app.route("/dashboard/registered_events")
@login_required
def registered_events():
	user=GetUserInfo()
	event=user.events
	return render_template("registered.html",event)

#Events
@app.route("/add-course-page")
@admin_login_required
def get_admin_add_event():
	return render_template("admin_add_event.html")

@app.route("/add-event",methods=["GET","POST"])
@admin_login_required
def Add_Event():
	try:
		if request.method=="POST":
			name=request.form["name"]
			organiser=request.form["organiser"]
			duration=request.form["duration"]
			start_date=request.form["start_date"]
			end_date=request.form["end_date"]
			fees=request.form["fees"]
			description=request.form["description"]
			new_event=Event_details(name=name,organiser=organiser,duration=duration,start_date=start_date,end_date=end_date,fees=fees,description=description)
			db.session.add(new_event)
			db.session.commit()
			flash("Event Added")
			return redirect("/add-event")
	except Exception as e:
		return redirect("/")

#events start


@app.route("/event-register/<int:event_id>")
def Event_Register(event_id):
	try:
		if session["logged_in"]:
			user=GetUserInfo()
			event=Event_details.query.filter_by(event_id=event_id).first()
			register=Registered_Events()
			db.session.add(register)
			event.subscribers.append(register)
			user.registered_in_events.append(register)
			db.session.commit()
			flash("Registered To This Event!!!")
			return redirect("/event-content/"+str(event_id))
		else:
			flash("Please Login!!!")
			return redirect("/event-content/"+str(event_id))
	except:
		flash("Please login!!!")
		return redirect("/event-content/"+str(event_id))

@app.route("/get-enrollment-in-event/<int:event_id>")
def Get_registration_in_event(event_id):
	try:
		if session["logged_in"]:
			user=GetUserInfo()
			event=Event_details.query.filter_by(event_id=event_id).first()
			registered=Registered_Events.query.filter_by(event_id=event_id,user_id=user.user_id).all()
			if len(registered)>0:
				if registered[0].payment_done:
					return jsonify(valid=True,link="#",data="Enrolled")
				else:
					return jsonify(valid=True,link="/pay-now/event/"+str(event_id),data="Pay Now")
			else:
				return jsonify(valid=True,link="/event-enroll/"+str(event_id),data="Enroll Now")
		else:
			return jsonify(valid=True,link="/event-enroll/"+str(event_id),data="Enroll Now")
	except:
		return jsonify(valid=True,link="/event-enroll/"+str(event_id),data="Enroll Now")

#Events Ends

@app.route("/logout")
@login_required
def logout():
	try:
		client_email=session['username']
		session.pop('username',None)
		session['logged_in']=False
		return redirect(url_for("Home"))
	except:
		flash("ALREADY LOGGED OUT")
		return redirect(url_for("Home"))

@app.route("/login",methods=["GET","POST"])
def login():
	try:
		if request.method=="POST":
			email=request.form["email"]
			chpassword=request.form["passwd"]
			user=User_details.query.filter_by(email=email).all()
			if len(user)==0:
				return render_template("login.html")
			user=user[0]
			if sha256_crypt.verify(chpassword,user.password):
				session['logged_in']=True
				session['username']=user.email
				return redirect(url_for("Home"))
			else:
				flash("Wrong Credential!!!")
				return redirect(url_for("Home"))
		else:
			return render_template(url_for("Home"))
	except:
		return "SORRY WE HAVE SOME TROUBLE!!!!! PLEASE TRY AGAIN!"

@app.route("/forgot-password-page")
def forget_password_page():
	return render_template("forgotpass.html")

@app.route("/change-password-page")
def change_password_page():
	user=GetUserInfo()
	return render_template("change_pass.html",uid=user.user_id,purpose=0)

@app.route("/forgotpassword",methods=["GET","POST"])
def forget_password():
	try:
		if request.method=="POST":
			email=request.form['email']
			user=User_details.query.filter_by(email=email).all()
			if len(user)>0:
				user=user[0]
				# msg=Message('From MyParliament',sender='smtp.gmail.com',recipients=[uemail])
				otp=randint(100000,999999)
				# msg.body="Your otp for change password: "+str(otp)+". Valid for 1 hour."
				otp_obj=Otp_details(user_id=user.user_id,otp_no=otp,purpose=0,valid_till=(datetime.now()+timedelta(hours=1)))
				db.session.add(otp_obj)
				# mail.send(msg)
				db.session.commit()
				return render_template("change_pass.html",uid=user.user_id,purpose=1)
			else:
				flash("Couldn't find your account with this email.")
				return redirect("/forget-password")
		else:
			flash("Something went wrong.")
			return redirect("/forget_password")
	except Exception as e:
		return render_template("error.html",message="Some Error occured.")

@app.route("/change-password/<int:purpose>-<int:uid>",methods=["GET","POST"])
def change_password(purpose,uid):
	try:
		if request.method=="POST":
			if purpose==1:
				otp=request.form["otp"]
				user_verify=Otp_details.query.filter_by(user_id=uid).first()
				if user_verify.valid_till<datetime.now() and user_verify.purpose==0 and user_verify.otp_no==int(otp):
					user=User_details.query.filter_by(user_id=uid).first()
					newp=request.form["newpasswd"]
					user.password=sha256_crypt.encrypt(newp)
					db.session.delete(user_verify)
					db.session.commit()
					session['logged_in']=True
					session['username']=user.email
					return redirect(url_for("Dashboard"))
				else:
					flash("Wrong OTP or OTP Expired!!!")
					return render_template("sign.html")
			elif purpose==0:
				oldpass=request.form["oldpasswd"]
				newpasswd=sha256_crypt.encrypt(request.form["newpasswd"])
				user=GetUserInfo()
				if sha256_crypt.verify(oldpass,user.password):
					user.password=newpasswd
					db.session.commit()
					return redirect("/")
				else:
					flash("Wrong Password")
					return redirect("/")
		else:
			flash("Something went wrong.")
			return redirect("/")
	except Exception as e:
		return render_template("error.html",message="Some Error occured.")

@app.route("/update_profile")
@login_required
def update_profile():
	try:
		if request.method=="POST":
			user=GetUserInfo()
			name=request.form["name"]
			oldp=sha256_crypt.encrypt(request.form["oldpwd"])
			change_p=request.form['change_p']
			if change_p:
				newp=sha256_crypt.encrypt(request.form["newpwd"])
				if oldp==user.password:
					updated_user_details=User_details(password=newp)
				else:
					flash("Wrong password entered.")
					return redirect("/myprofile")
			newp=sha256_crypt.encrypt(request.form["newpwd"])
			add1=request.form['add1']
			add2=request.form['add2']
			add3=request.form['add3']
			city=request.form['city']
			state=request.form['state']
			pincode=request.form['pincode']
			updated_add=Address(add1,add2,add3,city,state,pincode)
			updated_user_details.address_id=updated_add
			updated_user_details=User_details(name=name)
			db.session.commit()
			return redirect(url_for("Dashboard"))
		else:
			flash("Method not allowed")
			return render_template("/myprofile")
	except Exception as e:
		return render_template("error.html",message="Some Error occured.")

@app.route("/get/<string:page>")
def get_blog_name(page):
	nav_data=if_login()
	return render_template(page+".html",nav_value=nav_data)



@app.route("/update/address")
@login_required
def Address_update():
	try:
		user=GetUserInfo()
		if request.method=="POST":
			add1=request.form['add1']
			add1=request.form['add2']
			add1=request.form['add3']
			city=request.form['city']
			state=request.form['state']
			pincode=request.form['pincode']
			new_add=Address(add1,add2,add3,city,state,pincode)
			db.session.add(new_add)
			db.session.commit()
			user.address_id=new_add
			db.session.commit()
			flash("Address Updated Successfully")
			return redirect("/")
		else:
			raise f'Wrong Method Used.'
	except Exception as e:
		return render_template("error.html",message=str(e))


@app.route("/submit-contact-form",methods=["GET","POST"])
def submit_contact_form():
	name=request.form["name"]
	email=request.form["email"]
	mob_no=request.form["mob_no"]
	msg=request.form["msg"]
	new_comp=Contact(mail=email,name=name,contact_no=mob_no,message=msg)
	db.session.add(new_comp)
	db.session.commit()
	return redirect("/")





app.secret_key = "this is nothing but a secret key"


if __name__ == '__main__':
	app.run(debug=True)
