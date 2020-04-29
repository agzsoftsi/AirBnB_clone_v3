#!/usr/bin/python3
"""
Module View Places-Reviews
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def all_reviews_by_place(place_id):
    """ GET Method retrieve list of all Reviews by Place objects """
    place = storage.get('Place', place_id)
    if place:
        reviews = place.reviews
        all_reviews = []

        for review in reviews:
            all_reviews.append(review.to_dict())
        return jsonify(all_reviews)
    abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def retrieve_review(review_id):
    """ GET Method to retrieve a particular Review """
    review = storage.get('Review', review_id)
    if review:
        return review.to_dict()
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ DELETE Method delete a Review """
    review = storage.get('Review', review_id)

    if review:
        storage.delete(review)
        storage.save()
        return {}
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ POST Method create a Place by City"""

    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    review_name = request.get_json()

    if not review_name:
        abort(400, {'Not a JSON'})
    if 'user_id' not in review_name:
        abort(400, {'Missing user_id'})
    if 'text' not in review_name:
        abort(400, {'Missing text'})

    user_id = request.get_json()["user_id"]
    user = storage.get('User', user_id)

    if user is None:
        abort(404)

    new_review = Review(**review_name)
    new_review.place_id = place.id
    new_review.user_id = user.id
    storage.new(new_review)
    storage.save()
    return new_review.to_dict(), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ PUT Method update a Review """
    update_attr = request.get_json()
    if not update_attr:
        abort(400, {'Not a JSON'})
    my_review = storage.get('Review', review_id)
    if not my_review:
        abort(404)
    for key, value in update_attr.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(my_review, key, value)
    storage.save()
    return my_review.to_dict()
