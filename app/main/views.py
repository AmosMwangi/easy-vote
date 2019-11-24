from flask import render_template, redirect,request,url_for,abort
from . import main
from flask_login import login_required,current_user
from ..models import User,Pitch,Comment,Upvote,Downvote  
from .forms import UpdateProfile,PitchNow,MyComment,UpVote,DownVote
from .. import db


@main.route('/',methods =['GET','POST'])
def index():
    pitch = Pitch.query.filter_by().first()
    title = 'Welcome to pitch it'
    business_pitch = Pitch.query.filter_by(category='Business')
    production_pitch = Pitch.query.filter_by(category='Production')
    interview_pitch = Pitch.query.filter_by(category='Interview')
    promotion_pitch = Pitch.query.filter_by(category='Promotion')
    sales_pitch = Pitch.query.filter_by(category='Sales')

    upvotes = Upvote.get_all_upvotes(pitch_id=Pitch.id)

    return render_template('home.html',title=title,pitch=pitch,upvotes=upvotes,business_pitch=business_pitch,interview_pitch=interview_pitch,sales_pitch=sales_pitch,production_pitch=promotion_pitch)

@main.route('/pitches/new/',methods=['GET','POST'])
@login_required
def new_pitch():
    form = PitchNow()
    my_upvotes = Upvote.query.filter_by(pitch_id=Pitch.id)
    if form.validate_on_submit():
        description = form.description.data
        title = form.title.data
        owner_id = current_user
        category = form.category.data
        print(current_user.get_current_object().id)
        new_pitch = Pitch(owner_id =current_user._get_current_object().id, title = title,description=description,category=category)
        db.session.add(new_pitch)
        db.session.commit()

        return redirect(url_for('main.index'))
    return render_template('pitch.html',form=form)

@main.route('/comment/new/<int:pitch_id>',methods=['GET','POST'])
@login_required
def new_comment(pitch_id):
    form = MyComment()
    pitch=Pitch.query.get(pitch_id)
    if form.validate_on_submit():
        comment = form.comment.data
        new_comment=Comment(comment=comment,user_id=current_user.get_current_object().id,pitch_id=pitch_id)
        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for('.new_comment',pitch_id=pitch_id))
    display_comments=Comment.query.filter_by(pitch_id=pitch_id).all()
    return render_template('comments.html',form=form,pitch=pitch,display_comments=display_comments)

@main.route('/pitch/upvote/<int:pitch_id>/upvote',methods=['GET','POST'])
@login_required
def upvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch_upvotes= UpVote.query.filter_by(pitch_id=pitch_id)

    if Upvote.query.filter(UpVote.user_id==user.id,UpVote.pitch_id==pitch_id).first():
        return redirect(url_for('main.index'))

    new_upvote = UpVote(pitch_id=pitch_id,user=current_user)
    new_upvote.save_upvotes()
    return redirect(url_for('main.index'))

@main.route('/pitch/downvote/<int:pitch_id>/downvote', methods = ['GET', 'POST'])
@login_required
def downvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch_downvotes = Downvote.query.filter_by(pitch_id= pitch_id)
    
    if Downvote.query.filter(Downvote.user_id==user.id,Downvote.pitch_id==pitch_id).first():
        return  redirect(url_for('main.index'))

    new_downvote = Downvote(pitch_id=pitch_id, user = current_user)
    new_downvote.save_downvotes()
    return redirect(url_for('main.index'))

@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)
    return render_template("profile/profiles.html",user=user)

@main.route('/user/<uname>/update',methods=['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form=form)

@main.route('/user/<uname>/update/pic',methods=['GET','POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path 
        db.session.commit()

    return redirect(url_for('main.profile',uname=uname))