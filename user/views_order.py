from django.shortcuts import render
from user.models import *
from django import http
from django.views import View
import json, requests
from django.db.models import Max
from django.db import transaction
from django.db import IntegrityError
from django.db.models import Sum, Count, Max, Min, Avg