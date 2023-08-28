import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis


redis_client = FlaskRedis()
# create the extension
database = SQLAlchemy()
# mysql = MySQL()

def create_app(test_config=None):

    from flaskr.url import views as url_views
    # from flaskr.url import api

    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    #database_path = os.path.join(app.instance_path, "flaskr.sqlite")
    database_path = 'mysql+pymysql://silk:iamsilk@44.202.64.68:3306/tinyfy'

    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
        #REDIS_URL = "redis://:@localhost:6379/0",
        
    )
    app.config['REDIS_HOST'] = 'localhost'
    app.config['REDIS_PORT'] = 6379
    app.config['REDIS_DB'] = 0
    app.config['CORS_HEADERS'] = 'Content-Type'

    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+database_path
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config['MYSQL_HOST'] = '44.202.64.68'
    app.config['MYSQL_USER'] = 'silk'
    app.config['MYSQL_PASSWORD'] = 'iamsilk'
    app.config['MYSQL_DB'] = 'tinyfy'
    

    #CORS(app)
    database.init_app(app)
    redis_client.init_app(app)
    # mysql.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # register the database commands
    #db.init_app(app)
    #create_database(app)
    with app.app_context():
        database.create_all()

    # apply the blueprints to the app
    app.register_blueprint(auth.bp)
    #app.register_blueprint(blog.bp)
    app.register_blueprint(url_views.bp)
    # app.register_blueprint(api.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app


# from os import path
# def create_database(app):
#     # if the database does not exist then we will create it
#     database_path = os.path.join(app.instance_path, "flaskr.sqlite")
    
#     if not path.exists("sqlite:///"+database_path):
#         database.create_all()
#         print('Database created')
