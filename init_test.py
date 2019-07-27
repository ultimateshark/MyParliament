from datetime import datetime,timedelta

@app.route("/signup")
def signup():
    try:
        if request.method=="POST":
            name=request.form['name']
            uemail=request.form['email']
            passwd=sha256_crypt.encrypt((request.form['passwd']))
            contact_no=request.form['contact_no']
            user=User_details.query.filter_by(email=uemail).all()
            if len(user)==0:
                new_user=User_details(name=name,email=email,password=passwd,contact_no=contact_no,verified=0)
                db.session.add(new_user)
                db.session.commit()
                msg=Message('From MyParliament',sender='smtp.gmail.com',recipients=[uemail])
                otp=randint(100000,999999)
                msg.body="Your otp for signup: "+str(otp)
                mail.send(msg)
                otp_obj=Otp_details(user_id=new_user.user_id,otp_no=otp,purpose=1,valid_till=(datetime.now()+timedelta(hours=1)))
                return redirect("otp_page.html")
            else:
                flash("Email already used.")
                return redirect("/signup")
        else:
            return redirect("/signup")
 	except Exception as e:
        return render_template("error.html",message="Some Error occured.")


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
