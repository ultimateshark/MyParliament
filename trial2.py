#EVENT ALL
@app.route("/add-course-page")
@login_required
def get_admin_add_event():
	return render_template("admin_add_event.html")

@app.route("/add-event",methods=["GET","POST"])
@login_required
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

@app.route("/get-registration-in-event/<int:event_id>")
def Get_registration_in_event(event_id):
	user=GetUserInfo()
	event=Event_details.query.filter_by(event_id=event_id).first()
	registered=Registered_Events.query.filter_by(event_id=event_id,user_id=user.user_id).all()
	if len(registered)>0:
		return jsonify(valid=True,link="#",data="Registered")
	else:
		return jsonify(valid=True,link="/event-register/"+str(event_id),data="Register Now")

@app.route("/event-content/<int:event_id>")
def Event_content(event_id):
	details=Event_details.query.filter_by(event_id=event_id).first()
	return render_template("event_cont.html",event=details)
