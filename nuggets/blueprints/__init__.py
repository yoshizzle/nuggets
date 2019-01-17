from nuggets import app

from nuggets.blueprints.public import public

app.register_blueprint(public)
