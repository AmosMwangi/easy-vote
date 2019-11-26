from flask import render_template, redirect,request,url_for,abort
from . import main
from .forms import UpdateProfile,PitchNow,MyComment
from ..models import User,Pitch,Comment
from flask_login import login_required,current_user
from .. import db,photos


@main.route('/',methods =['GET','POST'])
def index():
    pitch = Pitch.query.filter_by().first()
    title = 'Pitch Hub'
    business_pitch = Pitch.query.filter_by(category='Business')
    production_pitch = Pitch.query.filter_by(category='Production')
    interview_pitch = Pitch.query.filter_by(category='Interview')
    promotion_pitch = Pitch.query.filter_by(category='Promotion')
    sales_pitch = Pitch.query.filter_by(category='Sales')
    return render_template('home.html',title=title,pitch=pitch,business_pitch=business_pitch,interview_pitch=interview_pitch,sales_pitch=sales_pitch,production_pitch=promotion_pitch)

@main.route('/pitches/new/',methods=['GET','POST'])
@login_required
def new_pitch():
    form = PitchNow()

    if form.validate_on_submit():
        description = form.description.data
        title = form.title.data
        owner_id = current_user
        category = form.category.data
        new_pitch = Pitch(owner_id =current_user._get_current_object().id, title = title,description=description,category=category)
        db.session.add(new_pitch)
        db.session.commit()

        return redirect(url_for('main.index'))
    return render_template('pitches.html',form=form)

@main.route('/comment/new/<int:pitch_id>',methods=['GET','POST'])
@login_required
def new_comment(pitch_id):
    form = MyComment()
    pitch=Pitch.query.get(pitch_id)
    if form.validate_on_submit():
        comment = form.comment.data
        new_comment=Comment(description=comment,user_id=current_user.id,pitch_id=pitch_id)
        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for('.new_comment',pitch_id=pitch_id))
    display_comments=Comment.query.filter_by(pitch_id=pitch_id).all()
    return render_template('comments.html',form=form,pitch=pitch,comments=display_comments)

# @main.route('/user/<uname>')
# @login_required
# def profile(uname):
#     user = User.query.filter_by(username = uname).first()

#     if user is None:
#         abort(404)
#     return render_template("profile/profiles.html",user=user)

# @main.route('/user/<uname>/update',methods=['GET','POST'])
# @login_required
# def update_profile(uname):
#     user = User.query.filter_by(username = uname).first()
#     if user is None:
#         abort(404)

#     form = UpdateProfile()

#     if form.validate_on_submit():
#         user.bio = form.bio.data

#         db.session.add(user)
#         db.session.commit()

#         return redirect(url_for('.profile',uname=user.username))

#     return render_template('profile/update.html',form=form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))