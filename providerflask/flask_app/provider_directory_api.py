from flask import jsonify,request,redirect,url_for,send_from_directory
from flask_app import app
from flask import Flask
from flask_cors import CORS
import string
import shutil
import csv
import os
import datetime
import pandas as pd
import json
import requests
import app.fhirinfo as fhir


UNAUTHORIZED={"error:":"unauthorized","STATUS CODE":401}
BADREQUEST={"error:":"bad request","STATUS CODE":400}
NOTFOUND={"error:":"NOT FOUND","STATUS CODE":404}


@app.errorhandler(401)
def error401(e):
    return jsonify(UNAUTHORIZED),401

@app.errorhandler(400)
def error400(e):
    return jsonify(BADREQUEST),400

@app.errorhandler(404)
def error404(e):
    return jsonify(NOTFOUND),404


@app.route('/')
def root():
    return jsonify({"message":"FHIR API USING HEALTH SAMARAI"})

@app.route('/api/fhir/practitionersearch',methods=['POST'])
def practitionersearch():
    
    if not request.json or 'provider' not in request.json or 'searchby' not in request.json:
        return jsonify(BADREQUEST),400

    providername=request.json['provider']
    searchby=request.json['searchby']    
    
    
    fhir_provider=fhir.get_providers(providername,searchby)
    #print(fhir_provider)
    if isinstance(fhir_provider,str)==True:
        print('String true')
        return fhir_provider

    else:
        print('String False')
        return jsonify(fhir_provider)


@app.route('/api/fhir/practitionerall',methods=['GET'])
def practitionerall(): 

    fhir_provider=fhir.get_all_providers()

    return fhir_provider

    