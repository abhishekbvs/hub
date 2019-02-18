import datetime
from flask import render_template, flash, redirect, request, url_for, jsonify,json
from app import app, db, api
from config import Config
from app.models import Workshops,Talks,Contests
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from flask_restplus import Resource, Api

events = api.namespace('events', description="Events management")

@events.route('/workshops')
class events_workshops(Resource):

    # API Params: JSON([Standard])
    # Standard: IP, Sender ID
    # Returns: JSON array
    # Sends list of all Workshops
    def get(self):
        try:
            workshops = Workshops.query.all()
            responseObject = []
            for workshop in workshops:
                responseObject.append({
                    'id':workshop.id,
                    'title':workshop.title,
                    'plink':workshop.plink,
                    'short':workshop.short,
                    'department':workshop.department,
                    'fee':workshop.fee
                })
        except Exception as e:
            print(e)
            responseObject = {
                'status':'failure',
                'Message':'Error Occured'
            }
        return jsonify(responseObject)

    # API Params: JSON([Standard])
    # Standard: IP, Sender ID
    # Returns: JSON Status Code
    # Add Workshop
    @api.doc(params = {
        'title':'Title',
        'plink':'Permanent Link',
        'short':'Short Description',
        'about':'Long Description in md',
        'prereq':'Prerequisites in md',
        'department':'Department',
        'theme':'Theme',
        'instructor':'Instructor Name',
        'abins':'About the Lead Instructor',
        'vidurl':'Video URL',
        'company':'Company Name',
        'lead':'Company Lead',
        'contact':'Contact No',
        'incharge':'Incharge V-ID',
        'support':'Supporter V-ID',
        'fee':'Workshop Fee',
        'seats':'No of Seats',
        'companylogo':'Company Logo location',
        'img1':'Image 1 location',
        'img2':'Image 2 location',
        'img3':'Image 3 location',
        })
    def post(self):
        try:
            data = request.get_json()
            workshop = Workshops(
                title = data.get('title'),
                plink = data.get('plink'),
                short = data.get('short'),
                instructor = data.get('instructor'),
                abins = data.get('abins'),
                department = data.get('department'),
                fee = data.get('fee'),
                incharge = data.get('incharge')
            )
            db.session.add(workshop)
            db.session.commit()
            responseObject={
                'status':'success',
                'message':' Workshop Details Succefully Posted'
            }
        except Exception as e:
            print(e)
            # Send email
            responseObject = {
                'status':'fail',
                'message':'Error occured'
            }
        return jsonify(responseObject)

@events.route('/workshops/<int:id>')
class events_workshops_indv(Resource):

    # API Params: JSON([Standard])
    # Standard: IP, Sender ID
    # Returns: JSON Array
    # Send details of the Workshop
    def get(self, id):
        try:
            workshop = Workshops.query.filter_by(id=id).first()
            if workshop is not None:
                responseObject = {
                    'title':workshop.title,
                    'plink':workshop.plink,
                    'short':workshop.short,
                    'instructor':workshop.instructor,
                    'abins':workshop.abins,
                    'department':workshop.department,
                }
            else:
                responseObject ={
                    'status':'fail',
                    'message':'invalid workshop id'
                }
        except Exception as e:
                print(e)
                # Send email
                responseObject = {
                    'status':'fail',
                    'message':'Error occured'
                }
        return jsonify(responseObject)

    # API Params: JSON([Standard])
    # Standard: IP, Sender ID
    # Returns: JSON Status Code
    # Edit details of the Workshop
    @api.doc(params = {
        'title':'Title',
        'plink':'Permanent Link',
        'short':'Short Description',
        'about':'Long Description in md',
        'prereq':'Prerequisites in md',
        'department':'Department',
        'theme':'Theme',
        'instructor':'Instructor Name',
        'abins':'About the Lead Instructor',
        'vidurl':'Video URL',
        'company':'Company Name',
        'lead':'Company Lead',
        'contact':'Contact No',
        'incharge':'Incharge V-ID',
        'support':'Supporter V-ID',
        'fee':'Workshop Fee',
        'seats':'No of Seats',
        'companylogo':'Company Logo location',
        'img1':'Image 1 location',
        'img2':'Image 2 location',
        'img3':'Image 3 location',
        })
    def put(self, id):
        try:
            workshop = Workshops.query.filter_by(id=id).first()
            if workshop is not None:
                data = request.get_json()
                workshop.title=data.get('title')
                workshop.about=data.get('about')
                workshop.company=data.get('company')
                workshop.fee=data.get('fee')
                workshop.instructor=data.get('instructor')
                workshop.abins=data.get('abins')
                db.session.commit()
                responseObject = {
                    'status':'success',
                    'message':'workshop details edited successfully'
                }
            else:
                responseObject = {
                    'status':'failed',
                    'message':'invalid workshop id'
                }
        except Exception as e:
            print(e)
            # Send email
            responseObject = {
                    'status':'fail',
                    'message':'Error occured'
            }
        return jsonify(responseObject)

    # API Params: JSON([Standard])
    # Standard: IP, Sender ID
    # Returns: JSON Status Code
    # Delete Workshop
    def delete(self, id):
        try:
            workshop = Workshops.query.filter_by(id=id).first()
            if workshop is not None:
                db.session.delete(workshop)
                db.session.commit()
                responseObject = {
                    'status':'success',
                    'message':'workshop deleted'
                }
            else:
                responseObject = {
                    'status':'failed',
                    'message':'Invalid workshop id'
                }
        except Exception as e:
            print(e)
            # Send email
            responseObject = {
                    'status':'fail',
                    'message':'Error occured'
            }
        return jsonify(responseObject)

@events.route('/contests')
class events_contests(Resource):
    # API Params: JSON([Standard])
    # Standard: IP, Sender ID
    # Returns: JSON Array
    # Send list of all contests
    def get(self):
        try:
            contests = Contests.query.all()
            responseObject = []
            for contest in contests:
                responseObject.append({
                    'id':contest.id,
                    'title':contest.title,
                    'short':contest.short,
                    'pworth':contest.pworth,
                    'team_limit':contest.team_limit,
                    'fee':contest.fee
                })
        except Exception as e:
                print(e)
                # Send email
                responseObject = {
                    'status':'fail',
                    'message':'Error occured'
                }
        return jsonify(responseObject)

    # API Params: JSON([Standard])
    # Standard: IP, Sender ID
    # Returns: JSON Status
    # Add Contest
    @api.doc(params={
        'title':'Title',
        'short':'Short Description',
        'about':'Long Description in md',
        'rules':'Rules',
        'prereq':'Prerequisite in md',
        'organiser':'Organiser Name',
        'prize1':'Prize 1',
        'prize2':'Prize 2',
        'prize3':'Prize 3',
        'pworth':'Total Prize Worth',
        'fee':'Entry Fee',
        'team_limit':'No of Team Members',
        'expense':'Expenses for internal use',
        'incharge':'Incharge V-ID',
    })
    def post(self):
        try:
            data = request.get_json()
            contest = Contests(
                title=data.get('title'),
                short=data.get('short'),
                pworth=data.get('pworth'),
                team_limit=data.get('team_limit'),
                fee=data.get('fee'),
                incharge=data.get('incharge')
            )
            db.session.add(contest)
            db.session.commit()
            responseObject={
                'status':'success',
                'message':' Contest Details Succefully Posted'
            }
        except Exception as e:
            print(e)
            # Send email
            responseObject = {
                'status':'fail',
                'message':'Error occured'
            }
        return jsonify(responseObject)

@events.route('/contests/<int:id>')
class events_contests_indv(Resource):

    # API Params: JSON([Standard])
    # Standard: IP, Sender ID
    # Returns: JSON Array
    # Send details of the Contest
    def get(self, id):
        try:
            contest = Contests.query.filter_by(id=id).first()
            if contest is not None:
                responseObject = {
                    'title':contest.title,
                    'short':contest.short,
                    'pworth':contest.pworth,
                    'team_limit':contest.team_limit,
                    'fee':contest.fee,
                    'incharge':contest.incharge
                }
            else:
                responseObject ={
                    'status':'fail',
                    'message':'invalid contest id'
                }
        except Exception as e:
                print(e)
                # Send email
                responseObject = {
                    'status':'fail',
                    'message':'Error occured'
                }
        return jsonify(responseObject)

    # API Params: JSON([Standard])
    # Standard: IP, Sender ID
    # Returns: JSON Status Code
    # Edit details of the Workshop
    @api.doc(params={
        'title':'Title',
        'short':'Short Description',
        'about':'Long Description in md',
        'rules':'Rules',
        'prereq':'Prerequisite in md',
        'organiser':'Organiser Name',
        'prize1':'Prize 1',
        'prize2':'Prize 2',
        'prize3':'Prize 3',
        'pworth':'Total Prize Worth',
        'fee':'Entry Fee',
        'team_limit':'No of Team Members',
        'expense':'Expenses for internal use',
        'incharge':'Incharge V-ID',
    })
    def put(self, id):
        try:
            contest = Contests.query.filter_by(id=id).first()
            if contest is not None:
                data = request.get_json()
                contest.title=data.get('title')
                contest.short=data.get('short')
                contest.pworth=data.get('pworth')
                contest.fee=data.get('fee')
                contest.incharge=data.get('incharge')
                contest.team_limit=data.get('team_limit')
                db.session.commit()
                responseObject = {
                    'status':'success',
                    'message':'Contest details edited successfully'
                }
            else:
                responseObject = {
                    'status':'failed',
                    'message':'invalid workshop id'
                }
        except Exception as e:
            print(e)
            # Send email
            responseObject = {
                    'status':'fail',
                    'message':'Error occured'
            }
        return jsonify(responseObject)

    # API Params: JSON([Standard])
    # Standard: IP, Sender ID
    # Returns: JSON Status Code
    # Delete Workshop
    @api.doc('Delete Contest')
    def delete(self, id):
        try:
            contest = Contests.query.filter_by(id=id).first()
            if contest is not None:
                db.session.delete(contest)
                db.session.commit()
                responseObject = {
                    'status':'success',
                    'message':'contest deleted'
                }
            else:
                responseObject = {
                    'status':'failed',
                    'message':'Invalid contest id'
                }
        except Exception as e:
            print(e)
            # Send email
            responseObject = {
                    'status':'fail',
                    'message':'Error occured'
            }
        return jsonify(responseObject)

@events.route('/talks')
class events_talks(Resource):

    # API Params: JSON([Standard])
    # Standard: IP, Sender ID
    # Returns: JSON Array
    # Send list of all Talks
    def get(self):
        talks = Talks.query.all()
        return jsonify(Talks.serialize_list(talks))

    # API Params: JSON([Standard])
    # Standard: IP, Sender ID
    # Returns: JSON Status Code
    # Add Talk
    @api.doc('Talk addition')
    def post(self):
        data = request.get_json()
        talk = Talks(title=data.get('title'),
                    descr=data.get('description'),
                    person=data.get('person'),
                    amt=data.get('amount')
                    )
        db.session.add(talk)
        db.session.commit()
        print(talk)
        return jsonify(201)

@events.route('/talks/<int:id>/')
class events_talks_indv(Resource):

    # API Params: JSON([Standard])
    # Standard: IP, Sender ID
    # Returns: JSON Array
    # Send details of the Talk
    @api.doc('Detials of the talk')
    def get(self, id):
        talk = Talks.query.filter_by(id=id).first()
        return jsonify(talk.serialize())

    # API Params: JSON([Standard])
    # Standard: IP, Sender ID
    # Returns: JSON Status Code
    # Edit details of the Talk
    @api.doc('Edit details of the Talk')
    def put(self, id):
        data=request.get_json()
        talk = Talks.query.filter_by(id=id).first()
        talk.title=data.get('title')
        talk.descr=data.get('description')
        talk.person=data.get('person')
        talk.amt=data.get('amount')
        db.session.commit()
        return jsonify(200)

    # API Params: JSON([Standard])
    # Standard: IP, Sender ID
    # Returns: JSON Status Code
    # Delete Talk
    @api.doc('Delete Talk')
    def delete(self, id):
        talk = Talks.query.filter_by(id=id).first()
        if talk is not None:
            db.session.delete(talk)
            db.session.commit()
            return jsonify(200)

        return jsonify(406)
