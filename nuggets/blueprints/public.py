import os
import uuid
import requests
import json

from flask import (Flask, Blueprint, abort, render_template, redirect, request,
                   url_for)
from markdown import markdown
from datetime import datetime

from nuggets import app, mongo

from nuggets.forms.category import CategoryForm
from nuggets.forms.template import TemplateForm

public = Blueprint('public', __name__, template_folder='../../templates')
static_folder = os.path.join(os.getcwd(), 'static')

@public.route('/')
def index():
    online_users = mongo.db.users.find({"online": True})
    return render_template("index.html",
        online_users=online_users)
