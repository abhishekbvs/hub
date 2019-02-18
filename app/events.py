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
        'instructor':'Instructor Name',
        'abins':'About the Lead Instructor',
        'department':'Department',
        'fee':'Workshop Fee',
        'incharge':'Incharge V-ID',
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
        'instructor':'Instructor Name',
        'abins':'About the Lead Instructor',
        'department':'Department',
        'fee':'Workshop Fee',
        'incharge':'Incharge V-ID',
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
    @api.doc('Delete Workshop')
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


@events.route('/talks/')
class events_talks(Resource):

    # API Params: JSON([Standard])
    # Standard: IP, Sender ID
    # Returns: JSON Array
    # Send list of all Talks
    @api.doc('List of all talks')
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

@events.route('/contests/')
class events_contests(Resource):
    # API Params: JSON([Standard])
    # Standard: IP, Sender ID
    # Returns: JSON Array
    # Send list of all contests
    @api.doc('List of all Contests')
    def get(self):
        contests = Contests.query.all()
        return jsonify(Contests.serialize_list(contest))

    # API Params: JSON([Standard])
    # Standard: IP, Sender ID
    # Returns: JSON Status
    # Add Talk
    @api.doc('Contest addition')
    def post(self):
        data = request.get_json()
        contest = Contests(title=data.get('title'),
                    about=data.get('description'),
                    task=data.get('task'),
                    pricing=data.get('pricing'),
                    team_limit=data.get('team_limit'),
                    expense=data.get('expense'),
                    incharge=data.get('incharge')
                    )
        db.session.add(contest)
        db.session.commit()
        print(contest)
        return jsonify(201)

@events.route('/contests/<int:id>/')
class events_contests_indv(Resource):

    # API Params: JSON([Standard])
    # Standard: IP, Sender ID
    # Returns: JSON Array
    # Send details of the Contest
    @api.doc('Detials of the Contest')
    def get(self, id):
        contest = Contests.query.filter_by(id=id).first()
        c = {

        }
        return jsonify(contest.serialize())

    # API Params: JSON([Standard])
    # Standard: IP, Sender ID
    # Returns: JSON Status Code
    # Edit details of the Contest
    @api.doc('Edit details of the Contest')
    def put(self, id):
        try:
            data=request.get_json()
            print("Some data: ", data)
            if data is not None:
                contest = Contests.query.filter_by(id=id).first()
                contest.title=data.get('title')
                contest.about=data.get('description')
                contest.task=data.get('task')
                contest.pricing=data.get('pricing')
                contest.team_limit=data.get('team_limit')
                contest.expense=data.get('expense')
                contest.incharge=data.get('incharge')
                db.session.commit()
                responseObject = {
                    'status':'success',
                    'message':'Details successfully modified'
                }
                return jsonify(responseObject), 201
            else:
                responseObject = {
                    'status':'fail',
                    'message':'Invalid data'
                }
                return jsonify(responseObject), 401
        except Exception as e:
            print(e)
            # Send email
            responseObject = {
                'status':'fail',
                'message':'Error occured'
            }
            return jsonify(responseObject), 401

    # API Params: JSON([Standard])
    # Standard: IP, Sender ID
    # Returns: JSON Status Code
    # Delete Contest
    @api.doc('Delete Contest')
    def delete(self, id):
        contest = Contests.query.filter_by(id=id).first()
        if talk is not None:
            db.session.delete(contest)
            db.session.commit()
            return jsonify(200)

        return jsonify(406)
