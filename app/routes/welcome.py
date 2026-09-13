from flask import Blueprint, render_template

welcome_bp = Blueprint('welcome', __name__)

@welcome_bp.route('/welcome', methods=['GET', 'POST'])
def detect():
    return render_template("detection.html")
