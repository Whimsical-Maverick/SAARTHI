from flask import Blueprint,render_template

talk_bp = Blueprint('talk',__name__)

@talk_bp.route('/talk',methods=['GET','POST'])
def talk():
    return render_template('chat.html')