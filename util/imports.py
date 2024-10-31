# imports.py
from fastapi import Depends
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from database.database import engine, db_session
from util.hashing import get_hashed_password, verify_password
from sqlalchemy.orm import Session
import database.models as models
from flask_cors import CORS
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
