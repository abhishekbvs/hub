from app import app, db
import datetime
import jwt

class User(db.Model):
    vid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.String(30))
    email = db.Column(db.String(120), unique=True)
    fname = db.Column(db.String(30))
    lname = db.Column(db.String(30))
    ppic = db.Column(db.String(200))
    course = db.Column(db.String(200))
    major = db.Column(db.String(200))
    sex = db.Column(db.Integer)
    year = db.Column(db.Integer)
    college = db.Column(db.Integer)
    institution = db.Column(db.String(100))
    school = db.Column(db.Boolean)
    # In case college is not listed.
    phno = db.Column(db.String(10))
    # Levels: power directly propotional to number
    detailscomp = db.Column(db.Boolean)
    educomp = db.Column(db.Boolean)
    time_created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    lastseen = db.Column(db.DateTime)

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def super(self):
        return self.email=="nandujkishor@gmail.com" or self.email=="aswanth366@gmail.com"

    def encode_auth_token(self):
        # Params: None
        # Returns: JWT
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=10, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'sub': self.vid
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            print(e)
            # Setup emailing to email the occured exception
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        # Params: JWT
        # Returns: UserID / ErrorID (int)
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 1
            # Signature expired. Need to login again.
        except jwt.InvalidTokenError:
            return 2
            # Invalid token. Need to login again.

class BlacklistToken(db.Model):
    # Token Model for storing JWT tokens
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False

class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # caid = db.Column(db.Integer)
    district = db.Column(db.String(50))
    state = db.Column(db.String(50))

    def __repr__(self):
        return '<College {}>'.format(self.name)

class Talks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    plink = db.Column(db.String(30))
    short = db.Column(db.String(200))
    about = db.Column(db.String(3000))
    person = db.Column(db.String(30), nullable=False)
    desig = db.Column(db.String(30))
    # Person designation
    contact = db.Column(db.String(10))
    picurl = db.Column(db.String(260))
    # Picture on the talk, large
    ppicurlsm = db.Column(db.String(260))
    # Picture of the person (small)
    ppicurllr = db.Column(db.String(260))
    # Picture of the person (large)
    fee = db.Column(db.Integer)
    # Amount spent to bring the person
    incharge = db.Column(db.Integer)
    # ID of the internal person incharge

class Workshops(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    plink = db.Column(db.String(30))
    # Permalink (extension only)
    short = db.Column(db.String(200))
    about = db.Column(db.String(3000))
    # about on the workshop (1000 char)
    prereq = db.Column(db.Text) #Content in markdown
    department = db.Column(db.Integer)
    # Need to come up with a numbering for departments
    theme = db.Column(db.String(20))
    # Theme, if any
    vidurl = db.Column(db.String(400))
    # URL for video on the workshop, if any, from Youtube, Vimeo or any other service.
    img1 = db.Column(db.String(200))
    img2 = db.Column(db.String(200))
    img3 = db.Column(db.String(200))
    lead = db.Column(db.String(30))
    org = db.Column(db.String(30))
    # Conducting organisation, if any
    orglogo = db.Column(db.String(200))
    contact = db.Column(db.String(10))
    # Organising organisation contact details
    fee = db.Column(db.Integer)
    incharge = db.Column(db.Integer)
    # V-ID of the internal person incharge
    support = db.Column(db.Integer)
    # Data for timings and count
    duration = db.Column(db.Text)
    seats = db.Column(db.Integer)
    # V-ID of the support person assigned to the event
    pub = db.Column(db.Boolean, default=False)
    # Publish
# Need to build a seperate schema to manage expenses. Each row currosponds to certain payment, with which event for.
# Need to build a tag management system, to associate events in general.

class Contests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    plink = db.Column(db.String(30))
    img1 = db.Column(db.String(300))
    img2 = db.Column(db.String(300))
    img3 = db.Column(db.String(300))
    short = db.Column(db.String(200))
    about = db.Column(db.String(6000))
    rules = db.Column(db.String(6000))
    prereq = db.Column(db.String(6000))
    organiser = db.Column(db.String(40))
    department = db.Column(db.Integer)
    prize1 = db.Column(db.Integer)
    prize2 = db.Column(db.Integer)
    prize3 = db.Column(db.Integer)
    pworth = db.Column(db.Integer)
    # Prizes worth ...
    fee = db.Column(db.Integer)
    # Pricing per team (1 to any)
    team_limit = db.Column(db.Integer, default=1)
    # Max. no of students in a team
    expense = db.Column(db.Integer)
    # For internal use - expenses
    incharge = db.Column(db.Integer)

class Registrations(db.Model):
    regid = db.Column(db.Integer, primary_key=True)
    # Acts as the cart data + registrations
    vid = db.Column(db.Integer)
    #UserID
    cat = db.Column(db.Integer)
    # Event category (Workshop, ...)
    eid = db.Column(db.Integer)
    #EventID
    tid = db.Column(db.Integer)
    #TeamID
    pay_completed = db.Column(db.Boolean)
    # 0 if not paid, 1 if paid.
# Need to rethink registrations

class EventDLog(db.Model):
    # Logs Event dashboard changes
    # 1 for addition of a new event, 2 for edit, 3 for deletion
    vid = db.Column(db.Integer,primary_key=True)
    #UserID
    cat = db.Column(db.Integer, primary_key=True)
    # Event category (Workshop, ...)
    eid = db.Column(db.Integer, primary_key=True)
    #EventID
    action = db.Column(db.Integer)

class Staff(db.Model):
    vid = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(20))
    level = db.Column(db.Integer)
    # 1 for base level volunteer
    # 2 for ...
    # 3 for people with create previlige
    # 4 for core representative
