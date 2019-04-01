from flask import Blueprint, render_template, request
#from app.models import  Quote

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    # page = request.args.get('page', 1, type=int)
    # user = User.query.filter_by(username=username).first_or_404()
    # quotes = Quote.query.filter_by(author=user).paginate(page=page, per_page=2)
    return render_template('home.html')


@main.route('/about')
def about():
    return render_template('about.html', title='About')
