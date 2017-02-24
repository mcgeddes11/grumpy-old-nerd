from flask import render_template, flash, redirect, session, url_for, request, g, abort
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, timedelta
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm, ForgotPasswordForm, PasswordResetForm, AddUserForm, PostForm, EditPostForm, ContactMeForm
from .models import User, Post
from emails import send_email
import uuid, json, os, numpy, pandas, logging, traceback
from functools import wraps
import locale
locale.setlocale(locale.LC_ALL, "")
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer

# TODO:  Make classes render properly in the preview window on new and edit post pages
logger = logging.getLogger()

def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):

            if not g.user.is_authenticated:
               return app.login_manager.unauthorized()
            urole = g.user.urole
            if ( (urole != role) and (role != "ANY")):
                return app.login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@lm.unauthorized_handler
def unauthorized():
    return render_template('401.html'), 401

@app.before_request
def before_request():
    g.user = current_user

# Actual views/controllers
@app.route("/", methods=["GET","POST"])
@app.route("/index", methods=["GET","POST"])
def index():
    page = request.args.get("page",1,type=int)
    pagination = Post.query.filter(Post.is_published==True).order_by(Post.timestamp.desc()).paginate(page, per_page=5,error_out=False)
    return render_template("index.html", pagination=pagination)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/file_upload")
@login_required(role="admin")
def file_upload():
    # TODO: display existing files on server
    basedir = os.path.abspath(os.path.dirname(__file__))
    flist = sorted(os.listdir(os.path.join(basedir,"static","uploads")))
    return render_template("file_upload.html",file_list=flist)

@app.route("/contact", methods=["GET","POST"])
def contact():
    # TODO: better feedback on non-email address
    form = ContactMeForm()
    if form.validate_on_submit():
        text_body = form.message.data + "\n\rFrom: " + form.name.data
        template_data = {"content": form.message.data, "name": form.name.data, "email": form.email.data}
        try:
            send_email("[GRUMPYOLDNERD message from " + form.name.data + "]", form.email.data, ["joncocks@hotmail.com"], text_body, render_template("email_contact.html", message=template_data))
        except:
            logger.error(traceback.format_exc())
        form.name.data = ""
        form.email.data = ""
        form.message.data = ""
        return render_template("contact.html", form=form, msg="Message Sent!")
    return render_template("contact.html", form=form, msg="")

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    return render_template("post_base.html", post=post)

@app.route("/edit_posts", methods=["GET","POST"])
@login_required(role="ANY")
def edit_posts():
    form = EditPostForm()
    if form.validate_on_submit():
        post = Post.query.filter_by(id=int(form.id.data)).first()
        post.body = form.body.data
        post.title = form.title.data
        if form.save_draft._value() == "Save Draft (Unpublish)":
            post.is_published = False
        elif form.save_draft._value() == "Save & Publish":
            if post.timestamp is None:
                post.timestamp = datetime.utcnow()
            post.is_published = True
        elif form.save_draft._value() == "Delete Post":
            Post.query.filter_by(id=int(form.id.data)).delete()
        db.session.commit()
        return redirect(url_for('edit_posts'))
    return render_template("edit_posts.html", form=form, msg="")

@app.route("/new_post", methods=["POST","GET"])
@login_required(role="ANY")
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    body=form.body.data,
                    author=g.user)
        if form.save_draft._value() == "Save Draft":
            post.is_published = False
        elif form.save_draft._value() == "Save & Publish":
            if post.timestamp is None:
                post.timestamp = datetime.utcnow()
            post.is_published = True
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("new_post.html", form=form)

@app.route("/search_results", methods=["GET","POST"])
def search_results():
    page = request.args.get("page",1,type=int)
    qry = request.args.get("query","",type=str)
    result = Post.query.whoosh_search(qry, 50).filter(Post.is_published==True).paginate(page, per_page=5,error_out=False)
    return render_template("search_results.html", pagination=result)

# API-style controllers
@app.route("/do_upload", methods=["POST"])
@login_required(role="admin")
def do_upload():
    # TODO:  Hook this up to front end, and have it save to server
    print "Doing stuff"


@app.route("/get_users_posts", methods=["GET"])
@login_required(role="ANY")
def get_users_posts():
    u = g.user
    # Get all posts by this user
    posts = Post.query.filter_by(author=u).order_by(Post.timestamp.desc()).all()
    response = []
    for p in posts:
        response.append({"id": p.id, "title": p.title, "body": p.body, "is_published": p.is_published})
    return json.dumps(response)

@app.route("/get_post_text", methods=["GET"])
def get_post_text():
    # Get all posts from db that have been published
    posts = Post.query.filter(Post.is_published==True).order_by(Post.timestamp.desc()).all()
    # Build a list of 'documents' to pass to the CountVectorizer (sklearn)
    vect_text = []
    for p in posts:
        post_body = p.body
        # Use BeautifulSoup to strip the hmtl
        cleanbody = BeautifulSoup(post_body, "lxml").text
        vect_text.append(p.title + " " + cleanbody)
    # Count words, excluding English stop-words
    count_vect = CountVectorizer(stop_words='english')
    counts = count_vect.fit_transform(vect_text)
    count_sum = numpy.sum(counts,axis=0).astype(float).tolist()[0]
    # Simple max-count normalization to get the size factor for each word
    count_normalized = (numpy.array(count_sum) / numpy.max(count_sum)).tolist()
    # Build response to send to front-end
    response = []
    for word in count_vect.vocabulary_.keys():
        count_val = count_normalized[count_vect.vocabulary_[word]]
        response.append({"word": word, "count_normalized": count_val})
    w = [x["word"] for x in response]
    c = [x["count_normalized"] for x in response]
    df = pandas.DataFrame({"word": w, "count_normalized": c})
    df = df.sort_values(by="count_normalized", ascending=False)
    # Sort by descending scale factor, so we get the most common words first
    response = []
    for ix, r in df.iterrows():
        response.append({"word": r["word"], "count_normalized": r["count_normalized"]})
    return json.dumps(response)


# Login, logout and password recovery controllers
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    msg=""
    if form.validate_on_submit():
        # Login and validate the user.
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            msg = "User not found"
            return render_template('login.html', form=form, msg=msg)
        elif user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = url_for('index')
        else:
            msg = "Login unsuccessful - incorrect password"
            return render_template('login.html', form=form, msg=msg)
        if next:
            return redirect(next)

    return render_template('login.html', form=form, msg=msg)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/forgot_password", methods=["POST","GET"])
def forgot_password():
    form = ForgotPasswordForm()
    msg=""
    if form.validate_on_submit():
        # 1. Get user from DB corresponding to email address in form
        user = db.session.query(User).filter(User.email==form.email.data).first()
        if user is None:
            msg = "User not found"
            return render_template('forgot_password.html', form=form, msg=msg)
        # 2. Create pw_reset_guid in the DB for password reset
        user.pw_reset_guid = str(uuid.uuid4())
        # 3. Update pw_reset_expiry in DB (24 hours)
        user.pw_reset_expiry = datetime.utcnow() + timedelta(days=1)
        db.session.commit()
        # 4. Send email with link to page+guid
        send_email(subject="[GRUMPYOLDNERD Password Reset Request]",sender="joncocks@hotmail.com",recipients=[user.email],text_body=url_for("reset_password",reset_guid=user.pw_reset_guid,_external=True),html_body=render_template('email_password_reset.html', user=user))
        return redirect(url_for('login'))
    return render_template('forgot_password.html',form=form,msg=msg)


@app.route("/reset_password/<string:reset_guid>", methods=["POST","GET"])
def reset_password(reset_guid):
    form = PasswordResetForm()
    msg = ""
    # 1. Get user corresponding to this guid
    user = db.session.query(User).filter(User.pw_reset_guid == reset_guid).first()
    if user is None:
        msg = "Invalid password token!"
    if form.validate_on_submit():
        # 2. If link hasn't expired, update their password to new password, reset pw_reset_* fields
        if datetime.utcnow() < user.pw_reset_expiry:
            user.password = form.password.data
            user.pw_reset_guid = None
            user.pw_reset_expiry = None
            db.session.commit()
            # 3. Redirect to login page
            return redirect(url_for('login'))
        else:
            msg = "Token expired, request new token"

    return render_template('reset_password.html',form=form,msg=msg)

@app.route("/add_user", methods=["POST","GET"])
@login_required(role="admin")
def add_user():
    form = AddUserForm()
    msg = ""
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            msg = "User already exists"
            return render_template('add_user.html', form=form, msg=msg)
        user = User(form.email.data)
        user.password = form.password.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.urole = form.urole.data
        if form.urole.data not in ["admin","user"]:
            msg = "User role must be one of 'admin', 'user'."
            return render_template('add_user.html', form=form, msg=msg)
        db.session.add(user)
        db.session.commit()
        #TODO Send confirmation email to new user, inviting them to change their password
        return redirect(url_for('add_user'))

    return render_template('add_user.html',form=form,msg=msg)

