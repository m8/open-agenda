from django.shortcuts import render
from .models import Notes
# Create your views here.
from datetime import date

def index(req):
    today = date.today().strftime("%Y-%m-%d")
    todays_note = Notes.objects.filter(pub_date=today)
    
    print(todays_note[0])
    
    return render(req,'agenda.html', context={"notes":todays_note})