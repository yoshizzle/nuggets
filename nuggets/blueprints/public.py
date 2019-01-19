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
    nugget_form = NuggetForm()
    nuggets = mongo.db.nuggets.find({}).limit(10).sort('created', pymongo.DESCENDING)

    return render_template("index.html", nuggets=nuggets)

@public.route('/keyword/<keyword>')
def keyword_get(keyword):
    kword = keyword.strip().replace('+', ' ')
    nuggets = mongo.db.nuggets.find({ 'keywords': kword }).sort('created', pymongo.DESCENDING)

    return render_template('results_list.html', header_title='Browse by Keyword:', title_var=keyword, results=nuggets)

@public.route('/nugget/<id>')
def nugget_get(id):
    nugget = mongo.db.nuggets.find_one({'_id': ObjectId(id)})

    return render_template('/nugget.html', nugget=nugget)

@public.route('/nugget/new')
def nugget():
    nugget_form = NuggetForm()

    return render_template("nugget_edit.html", form=nugget_form)

@public.route('/nugget/new', methods=['POST'])
def nugget_post():
    nugget_form = NuggetForm()
    kwords = []
    dnow = datetime.utcnow()

    for k in nugget_form.keywords.data.split(','):
        kwords.append(k.strip().lower())

    new_nugget = mongo.db.nuggets.insert_one({
        'title': nugget_form.title.data,
        'title_md': markdown(nugget_form.title.data),
        'description': nugget_form.description.data,
        'description_md': markdown(nugget_form.description.data),
        'keywords': kwords, 'created': dnow
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
