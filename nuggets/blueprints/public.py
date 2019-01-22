import os
import uuid
import requests
import json
import pymongo

from flask import (Flask, Blueprint, abort, render_template, redirect, request,
                   url_for)
from markdown import markdown
from datetime import datetime
from random import randrange
from bson.objectid import ObjectId

from nuggets import app, mongo
from nuggets.forms.nugget import NuggetForm

public = Blueprint('public', __name__, template_folder='../../templates')
static_folder = os.path.join(os.getcwd(), 'static')

@public.route('/')
def index():
    nuggets = mongo.db.nuggets.find({}).limit(8).sort('created', pymongo.DESCENDING)
    count = mongo.db.nuggets.count()

    return render_template("index.html", nuggets=nuggets, count=count)

@public.route('/keyword/<keyword>')
def keyword_get(keyword):
    kword = keyword.strip().replace('+', ' ')
    nuggets = mongo.db.nuggets.find({ 'keywords': kword }).sort('created', pymongo.DESCENDING)

    return render_template('results_list.html', header_title='Browse by Keyword:', title_var=keyword, results=nuggets)

@public.route('/nugget/<id>')
def nugget_get(id):
    nugget = mongo.db.nuggets.find_one({'_id': ObjectId(id)})

    if not nugget:
        abort(404)

    return render_template('/nugget.html', nugget=nugget)

@public.route('/nugget/<id>/delete')
def nugget_delete(id):
    """
    I hope you know what you're doing if you hit this endpoint
    """
    nugget = mongo.db.nuggets.find_one({'_id': ObjectId(id)})

    if not nugget:
        abort(404)

    mongo.db.nuggets.delete_one({'_id': ObjectId(id)})

    return redirect('/')

@public.route('/nugget/<id>/edit')
def nugget_edit(id):
    nugget = mongo.db.nuggets.find_one({'_id': ObjectId(id)})

    if not nugget:
        abort(404)

    nugget_form = NuggetForm()
    nugget_form.id = nugget['_id']
    nugget_form.title = nugget['title']
    nugget_form.description = nugget['description']
    nugget_form.keywords = ', '.join(nugget['keywords'])

    return render_template('/nugget_edit.html', form=nugget_form)

@public.route('/nugget/<id>/edit', methods=['POST'])
def nugget_edit_update(id):
        nugget = mongo.db.nuggets.find_one({'_id': ObjectId(id)})

        if not nugget:
            abort(404)

        kwords = []
        for k in request.form['keywords'].split(','):
            if k.strip().lower() not in kwords:
                kwords.append(k.strip().lower())

        nid = nugget['_id']
        mongo.db.nuggets.update(
            {'_id': nid},
            {
                '$set': {
                    'title': request.form['title'],
                    'title_md': markdown(request.form['title']),
                    'description': request.form['description'],
                    'description_md': markdown(request.form['description']),
                    'keywords': kwords
                }
            },
            False # upsert
        )

        return redirect('/nugget/{}'.format(nid))

@public.route('/nugget/new')
def nugget():

    return render_template('nugget_edit.html', form=None)

@public.route('/nugget/new', methods=['POST'])
def nugget_post():
    kwords = []
    dnow = datetime.utcnow()

    for k in request.form['keywords'].split(','):
        if k.strip().lower() not in kwords:
            kwords.append(k.strip().lower())

    new_nugget = mongo.db.nuggets.insert_one({
        'title': request.form['title'],
        'title_md': markdown(request.form['title']),
        'description': request.form['description'],
        'description_md': markdown(request.form['description']),
        'keywords': kwords,
        'created': dnow
    }).inserted_id

    return redirect('/')

@public.route('/random')
def random():
    n = mongo.db.nuggets.count()
    random = mongo.db.nuggets.find({})[randrange(0,n)]['_id']

    return redirect('/nugget/{}'.format(random))

@public.route('/search', methods=['POST'])
def search():
    searchtext = request.form['searchtext']

    results = mongo.db.nuggets.find({ '$or': [{'title': {'$regex': searchtext}}, {'description': {'$regex': searchtext}}, {'keywords': {'$regex': searchtext}}] })

    return render_template('/results_list.html', header_title='Search Results for:', title_var=searchtext, results=results)
