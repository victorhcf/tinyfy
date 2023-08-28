import json

from flask import Blueprint
from flask import jsonify
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import flash
from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy import insert
from sqlalchemy import desc
from werkzeug.exceptions import abort
from flask_cors import cross_origin

from flaskr.auth import login_required
from flaskr.models import Url, User, Stats
from .url_service import UrlService

from flaskr import database


bp = Blueprint("url", __name__)


@bp.route("/")
def index():
    """Show all the posts, most recent first."""
    return render_template("url/index.html")
    

@bp.route("/url/my_urls")
@login_required
def my_urls():
    """Show all the posts, most recent first."""
    if g and g.user:
        user_id = g.user['id']
    urls = Url.query.join(Url.user).filter_by(id=user_id).order_by(desc(Url.id))
    return render_template("url/list.html", urls=urls)
    

from sqlalchemy import func

@bp.route("/url/<int:id>")
def view_url(id):
    """Show all the posts, most recent first."""
    url = Url.query.get(id)
    total_views = database.session.query(Stats).filter(Stats.url_id==id).count()
    url = url.to_dict()
    url['total_views'] = total_views
    if 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
        return jsonify({'url': url})
    return render_template("url/view.html", newurl=url)
    

# @bp.route("/list", methods=['GET'])
# @cross_origin()
# def list_urls():
#     """Show all the posts, most recent first."""
#     db = get_db()
#     cursor = db.cursor()
#     cursor.execute(
#         "SELECT id, url_original, url_secret, code, created "
#         " FROM urls "
#         " ORDER BY created DESC"
#     )
#     urls = cursor.fetchall()
        
#     cursor.close()

#     return jsonify(urls)
  

@bp.route("/generate", methods=['GET', 'POST'])
@cross_origin()
def generate():
    """Show all the posts, most recent first."""
    if request.method == "GET":
        return redirect(url_for("index"))    
    elif request.method == "POST":
        url_original = ''
        if 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
             url_original = request.json['url']
        elif 'url' in request.form:
            url_original = request.form["url"]

        url = Url(url_original=url_original)
        UrlService.generate_code(url=url)

        if g and g.user:
            user_id = g.user['id']
            user = User.query.get(user_id)
            url.user = user

        database.session.add(url)
        database.session.commit()

        if 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
            return jsonify({'url': url.to_dict()})
    
        return redirect(url_for("url.view_url", id=url.id))



@bp.route("/<url_code>", methods=['get'])
def redirect_url(url_code):
    url = Url.query.filter_by(code=url_code).first()
    print('URL ... ', url)
    if url and not url.enabled:
        if 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
            return jsonify({'meessage': 'Url not found'}), 404
        else:
            flash("URL não encontrada")
            return redirect(url_for("index"))
    
    if url:
        url_redirect = url.url_original
        sql = "INSERT INTO stats (url_id, code, url_original, ip) VALUES (:url_id, :code, :url_original, :ip)"

        stmt = insert(Stats).values(url_id=url.id, code=url.code, url_original=url.url_original, ip=request.remote_addr)
        
        engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
        with engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()

        print('url_redirect.. ', url_redirect)
        return redirect(url_redirect, code=302)
    else:
        flash("URL não encontrada")
    return redirect(url_for("index"))    



@bp.route("/<int:id>/delete", methods=("GET", "DELETE"))
@login_required
def delete(id):
    """Delete a Url.

    Ensures that the URL exists and that the logged in user is the
    author of the url.
    """
    status_return = 200
    message = "Deletado com sucesso!"
    if g and g.user:
        user_id = g.user['id']
        url = Url.query.get(id)

        if url.user and url.user.id == g.user['id']:
            database.session.delete(url)
            database.session.commit()
        else:
            message = "Somente o dono pode deletar."
            flash(message)
            status_return = 500
   
    if 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
            return jsonify({'message': message}), status_return
    return redirect(url_for("index"))    

    
@bp.route("/<int:id>/update", methods=("GET", "POST", "PATCH"))
@login_required
def update(id):
    """Update a url if the current user is the author."""
    url = Url.query.get(id)
    if request.method == "GET":
        return render_template("url/update.html", url=url)

    if request.method == "POST" or request.method == "PATCH":
        newurl = ""
        newenabled = url.enabled
        if 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
            newurl = request.json['url']
            newenabled = request.json['enabled']
        elif 'url' in request.form:
            newurl = request.form["url"]
            newenabled = "enabled" in request.form
        
        url.url_original = newurl
        url.enabled = newenabled
        database.session.flush()
        database.session.commit()

    return redirect(url_for("url.my_urls"))    




@bp.route("/stats")
@login_required
def stats():
    """Show all stats of the usage."""

    # db = get_db()
    # total_views = db.execute("SELECT count(*) FROM stats").fetchone()[0]
    # total_urls = db.execute("SELECT count(*) FROM urls").fetchone()[0]
    # total_users = db.execute("SELECT count(*) FROM user").fetchone()[0]

    total_views = database.session.query(Stats).count()
    total_urls = database.session.query(Url).count()
    total_users = database.session.query(User).count()
    print('COUNT.. ', total_views)
    # engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
    # with engine.connect() as conn:
    #     conn.execute(stmt)
    #     conn.commit()

    stats = {
        'total_users': total_users,
        'total_urls': total_urls,
        'total_views': total_views
    }
    return render_template("url/stats.html", stats=stats)
    
