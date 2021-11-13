from flask import Blueprint, request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from sqlalchemy.ext import mutable
from werkzeug.utils import append_slash_redirect,secure_filename
from src.database import Country,db
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
import datetime
import os

country = Blueprint("country",__name__,url_prefix="/api/v1/country")


@country.post('/post-cap')
@jwt_required()
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


@country.get('/all-caps')
@jwt_required()
def get_all_country_caps():
    
    page=request.args.get('page',1,type=int)
    per_page = request.args.get('per_page',1,type=int)
    
    all_caps = Country.query.filter().order_by(Country.id.desc()).paginate(page=page,per_page=per_page)
    
    data=[]

    for a_cap in all_caps.items:
        data.append({
            'id': a_cap.id,
            'img': a_cap.img,
            'country_name': a_cap.country_name,
            'climate_goal': a_cap.climate_goal,
            'posted_by': a_cap.posted_by,
            'created_at': a_cap.created_at,
            'updated_at': a_cap.updated_at,
        })
    
    meta={
        "page": all_caps.page,
        "pages": all_caps.page,
        "total_count": all_caps.total,
        "prev_page": all_caps.prev_num,
        "next_page": all_caps.next_num,
        "has_next": all_caps.has_next,
        "has_prev": all_caps.has_prev,
    }
     
    return jsonify({
        "country_caps": data, 
        "meta":meta
    }), HTTP_200_OK
