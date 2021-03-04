from django.shortcuts import render
from .models import Notes
from django.http import HttpResponse

# Create your views here.
from datetime import date

def index(req):
    today = date.today().strftime("%Y-%m-%d")
    todays_note = Notes.objects.filter(pub_date=today)
    if(todays_note.count() == 0):
        note = Notes()
        note.pub_date = today
        return render(req,'agenda.html', context={"notes":note})
    else:
        return render(req,'agenda.html', context={"notes":todays_note[0]})


def updateAgenda(req):
    date = req.POST.get('date','')
    notes = req.POST.get('notes','')

    Notes.objects.update_or_create(
        pub_date = date,
        defaults={'notes': notes, 'pub_date': date},
    )

    return HttpResponse(200)

def getDate(req):
    req_date = req.GET.get('date', '')
    note = Notes.objects.filter(pub_date=req_date)

    if(note.count() == 0):
        note = Notes()
        note.pub_date = req_date
        return render(req,'agenda.html', context={"notes":note})
    else:
        return render(req,'agenda.html', context={"notes":note[0]})