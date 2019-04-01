from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from app import db
from app.models import Quote, UserProfile
from app.quotes.forms import QuoteForm

quotes = Blueprint('quotes', __name__)


@quotes.route("/quote/new", methods=['GET', 'POST'])
@login_required
def new_quote():
    form = QuoteForm()
    if form.validate_on_submit():
        quote = Quote(
            author=current_user,
            gallons_requested=form.gallons_requested.data,
            date_requested=form.date_requested.data,
            delivery_address=form.delivery_address.data,
            suggested_price=form.suggested_price.data,
            total_amount_due=form.total_amount_due.data,
        )
        db.session.add(quote)
        db.session.commit()
        flash('Your quote has been requested', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.delivery_address.data = current_user.user_profile.address_one + ', ' + current_user.user_profile.address_two  # current_user.user_profile.address_one
    return render_template('create_quote.html', title='New Quote', form=form)


@quotes.route("/quote/<int:quote_id>")
@login_required
def quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    return render_template('quote.html', title=quote.id, quote=quote)
