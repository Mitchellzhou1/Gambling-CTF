# Import Flask Library
import string, random
from flask import Flask, render_template, request, session, url_for, redirect, make_response
import pymongo

app = Flask(__name__)

# Configure MongoDB 
def get_conn():
    # return pymongo.connect(
        # host="127.0.0.1",
        # user='usrrr',
        # passwd='password',
        # db='email_sqli_ctf',
        # charset='utf8mb4',
        # cursorclass=pymongo.cursors.DictCursor)

    return pymongo.connect(
        host="127.0.0.1",
        user='',
        passwd='',
        db='gambling',
        charset='utf8mb4',
        cursorclass=pymongo.cursors.DictCursor)

# roulette-backend/register 
# roulette-backend/login
# port 8000