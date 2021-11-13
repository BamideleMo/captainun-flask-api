from flask import Blueprint, request,jsonify
from sqlalchemy.ext import mutable
from werkzeug.utils import append_slash_redirect,secure_filename
from src.database import Country,db
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
import datetime
import os

country = Blueprint("country",__name__,url_prefix="/api/v1/country")


@country.post('/post-cap')
def post_cap():
    img=request.json['img']
    country_name=request.json['country_name']
    climate_goal=request.json['climate_goal']
    posted_by=request.json['posted_by']

    country = Country(img=img,country_name=country_name,climate_goal=climate_goal,posted_by=posted_by)
    db.session.add(country)
    db.session.commit()

    return jsonify({
        'message': "CAP Posted",
        'user': {
            'climate_goal': climate_goal, 'country_name': country_name
        }
    }), HTTP_201_CREATED