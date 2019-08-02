from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Registered_Courses(db.Model):
    __tablename__="registered_courses"
    reg_id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user_details.user_id"))
    course_id=db.Column(db.Integer,db.ForeignKey("courses.course_id"))
    courses=db.relationship("Courses",backref=db.backref('subscribers'))
    payment_done=db.Column(db.Boolean,default=0)

class Registered_Events(db.Model):
    __tablename__="registered_events"
    reg_id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user_details.user_id"))
    event_id=db.Column(db.Integer,db.ForeignKey("event_details.event_id"))
    selected=db.Column(db.Boolean,nullable=True)
    events=db.relationship("Event_details",backref=db.backref('subscribers'))
    payment_done=db.Column(db.Boolean,default=0)

class Registered_Olympiads(db.Model):
    __tablename__="registered_olympiads"
    reg_id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user_details.user_id"))
    oly_id=db.Column(db.Integer,db.ForeignKey("olympiad_details.oly_id"))
    answers=db.Column(db.String(6000),default="")
    final_score=db.Column(db.Integer,default=0)
    olympiads=db.relationship("Olympiad_details",backref=db.backref('subscribers'))
    payment_done=db.Column(db.Boolean,default=0)
    status=db.Column(db.Boolean)

class Progress(db.Model):
    __tablename__="progress"
    p_id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user_details.user_id"))
    lecture_id=db.Column(db.Integer,db.ForeignKey("lecture_details.lecture_id"))
    status=db.Column(db.Boolean)

class Solved_Assignments(db.Model):
    __tablename__="solved_assignments"
    sol_id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user_details.user_id"))
    week_assignment=db.Column(db.Integer,db.ForeignKey("week.week_id"))
    answers=db.Column(db.String(6000),nullable=True)
    final_score=db.Column(db.Integer,nullable=True)
    assignments=db.relationship("Week",backref=db.backref('subscribers'))


class Courses(db.Model):
    __tablename__="courses"
    course_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    author=db.Column(db.String(50))
    duration=db.Column(db.String(20))
    fees=db.Column(db.Integer)
    description=db.Column(db.String(1000))
    demo_link=db.Column(db.String(1000))
    weeks=db.relationship("Week",backref=db.backref('course'))
    announce=db.relationship("Announcements",backref=db.backref('of_course'))

class Announcements(db.Model):
    __tablename__="announcements"
    a_id=db.Column(db.Integer,primary_key=True)
    course_id=db.Column(db.Integer,db.ForeignKey("courses.course_id"),nullable=True)
    title=db.Column(db.String(60),nullable=True)
    decription=db.Column(db.String(600),nullable=True)

class Week(db.Model):
    __tablename__="week"
    week_id=db.Column(db.Integer,primary_key=True)
    lectures=db.relationship("Lecture_details",backref=db.backref('week'))
    assignment=db.Column(db.String(6000),nullable=True)
    course_id=db.Column(db.Integer,db.ForeignKey("courses.course_id"),nullable=True)
    questions=db.relationship("Questions",backref=db.backref("olympiad"))


class Lecture_details(db.Model):
    __tablename__="lecture_details"
    lecture_id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200))
    link=db.Column(db.String(1000))
    description=db.Column(db.String(5000),nullable=True)
    week_id=db.Column(db.Integer,db.ForeignKey("week.week_id"),nullable=True)

class Questions(db.Model):
    __tablename__="questions"
    q_id=db.Column(db.Integer,primary_key=True)
    question=db.Column(db.String(500))
    optA=db.Column(db.String(200))
    optB=db.Column(db.String(200))
    optC=db.Column(db.String(200))
    optD=db.Column(db.String(200))
    correctopt=db.Column(db.String(1))
    olympiad_id=db.Column(db.Integer,db.ForeignKey("olympiad_details.oly_id"),nullable=True)
    week_id=db.Column(db.Integer,db.ForeignKey("week.week_id"),nullable=True)

class Images(db.Model):
    __tablename__="images"
    image_id=db.Column(db.Integer,primary_key=True)
    file_name=db.Column(db.String(100))
    event_id=db.Column(db.Integer,db.ForeignKey("event_details.event_id"))
    oly_id=db.Column(db.Integer,db.ForeignKey("olympiad_details.oly_id"))
    course_id=db.Column(db.Integer,db.ForeignKey("courses.course_id"))

class Rel_questions_images(db.Model):
    __tablename__="rel_questions_images"
    r_id=db.Column(db.Integer,primary_key=True)
    q_id=db.Column(db.Integer,db.ForeignKey("questions.q_id"))
    image_id=db.Column(db.Integer,db.ForeignKey("images.image_id"))

class Olympiad_details(db.Model):
    __tablename__="olympiad_details"
    oly_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    organiser=db.Column(db.String(50))
    duration=db.Column(db.String(20))
    fees=db.Column(db.Integer)
    description=db.Column(db.String(300))
    rules=db.Column(db.String(1000))
    status=db.Column(db.Integer,default=0)
    questions=db.relationship("Questions",backref=db.backref("olympiad"))


class Event_details(db.Model):
    __tablename__="event_details"
    event_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    organiser=db.Column(db.String(50))
    duration=db.Column(db.String(20))
    start_date=db.Column(db.String(10))
    end_date=db.Column(db.String(10))
    fees=db.Column(db.Integer)
    description=db.Column(db.String(300))
    venue=db.Column(db.String(50))
    user_id=db.Column(db.Integer,db.ForeignKey("user_details.user_id"),nullable=True)
    schedule=db.relationship("Schedule",backref=db.backref("of_event"))

class Schedule(db.Model):
    __tablename__="schedule"
    s_id=db.Column(db.Integer,primary_key=True)
    event_id=db.Column(db.Integer,db.ForeignKey("event_details.event_id"),nullable=True)
    day=db.Column(db.Integer)
    start_time=db.Column(db.DateTime)
    end_time=db.Column(db.DateTime)
    description=db.Column(db.String(50))

class Address(db.Model):
    __tablename__="address"
    address_id=db.Column(db.Integer,primary_key=True)
    add1=db.Column(db.String(50))
    add2=db.Column(db.String(50),nullable=True)
    add3=db.Column(db.String(50),nullable=True)
    city=db.Column(db.String(25),nullable=True)
    state=db.Column(db.String(20),nullable=True)
    pincode=db.Column(db.Integer)

    def __init__(self,add1,add2,add3,city,state,pincode):
        self.add1=add1
        self.add2=add2
        self.add3=add3
        self.city=city
        self.state=state
        self.pincode=pincode


class Otp_details(db.Model):
    __tablename__="otp_details"
    otp_id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user_details.user_id"))
    otp_no=db.Column(db.Integer,nullable=False)
    purpose=db.Column(db.Boolean)        #password change=0   verification=1
    valid_till=db.Column(db.DateTime)     #store time and date upto which otp is valid_till

class User_details(db.Model):
    __tablename__="user_details"
    user_id=db.Column(db.Integer,primary_key=True)
    account_type=db.Column(db.Boolean)      #0=tutor   1=student
    name=db.Column(db.String(100))
    email=db.Column(db.String(50),unique=True,nullable=False)
    contact_no=db.Column(db.Integer,nullable=True)
    password=db.Column(db.String(200),nullable=False)
    verified=db.Column(db.Boolean)              #1=yes or 0=no (id is verified with otp or not)
    profile_updated=db.Column(db.Boolean)
    class_type=db.Column(db.String(2))      #l1, l2, l3, l4, l5
    instituton=db.Column(db.String(50))
    profile_pic=db.Column(db.LargeBinary)
    address_id=db.Column(db.Integer,db.ForeignKey("address.address_id"),nullable=True)
    registered_in_courses=db.relationship("Registered_Courses",backref=db.backref('subscribed_by'))
    registered_in_events=db.relationship("Registered_Events",backref=db.backref('subscribed_by'))
    solved_assignments=db.relationship("Solved_Assignments",backref=db.backref('subscribed_by'))
    registered_in_olympiads=db.relationship("Registered_Olympiads",backref=db.backref('subscribed_by'))
    prgrss=db.relationship("Progress",backref=db.backref('of_user'))
