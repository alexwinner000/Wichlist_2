from flask import render_template, request, redirect, url_for, jsonify
from datetime import datetime
import uuid

from . import wishlist
from app.extensions import db
from app.models import Wishlist, Gift


@wishlist.route('/')
def home():
    return render_template('home.html')


@wishlist.route('/create', methods=['GET', 'POST'])
def create_wishlist():
    if request.method == 'POST':
        title = request.form.get('title')
        event_date = request.form.get('event_date')

        gift_titles = request.form.getlist('gift_title[]')
        gift_links = request.form.getlist('gift_link[]')

        slug = uuid.uuid4().hex

        wishlist_obj = Wishlist(
            title=title,
            event_date=datetime.strptime(event_date, '%Y-%m-%d'),
            created_at=datetime.utcnow(),
            expires_at=datetime.strptime(event_date, '%Y-%m-%d'),
            slug=slug
        )

        db.session.add(wishlist_obj)
        db.session.flush()

        # добавление подарков
        for title, link in zip(gift_titles, gift_links):

            if title.strip():
                gift = Gift(
                    title=title.strip(),
                    link=link.strip() if link else None,
                    wishlist_id=wishlist_obj.id
                )

                db.session.add(gift)

        db.session.commit()

        return redirect(url_for('wishlist.created', slug=slug))

    return render_template('wishlist/create.html')


@wishlist.route('/created/<slug>')
def created(slug):
    wishlist_obj = Wishlist.query.filter_by(slug=slug).first_or_404()

    return render_template(
        'wishlist/created.html',
        wishlist=wishlist_obj
    )


@wishlist.route('/<slug>', methods=['GET', 'POST'])
def detail(slug):

    wishlist = Wishlist.query.filter_by(slug=slug).first_or_404()

    # AJAX бронирование подарка
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        gift_id = request.form.get('gift_id')
        reserved_name = request.form.get('reserved_name')

        if not reserved_name:
            return jsonify({
                'success': False,
                'message': 'Введите имя'
            })

        gift = Gift.query.filter_by(
            id=gift_id,
            wishlist_id=wishlist.id
        ).first_or_404()

        if gift.is_reserved:

            return jsonify({
                'success': False,
                'message': 'Подарок уже забронирован'
            })

        gift.is_reserved = True
        gift.reserved_name = reserved_name

        db.session.commit()

        return jsonify({
            'success': True,
            'title': gift.title,
            'link': gift.link,
            'reserved_name': reserved_name
        })

    return render_template(
        'wishlist/detail.html',
        wishlist=wishlist
    )