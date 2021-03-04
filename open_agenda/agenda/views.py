from django.shortcuts import render
from .models import Notes
from django.http import HttpResponse

# Create your views here.
from datetime import date
import datetime

def index(req):
    today = date.today().strftime("%d-%m-%Y")
    yesterday = date.today() + datetime.timedelta(days=-1)
    yesterday = yesterday.strftime("%d-%m-%Y")

    tomorrow = date.today() + datetime.timedelta(days=1)
    tomorrow = tomorrow.strftime("%d-%m-%Y")

    todays_note = Notes.objects.filter(pub_date=today)
    if(todays_note.count() == 0):
        note = Notes()
        note.pub_date = today
        return render(req,'agenda.html', context={"notes":note})
    else:
        return render(req,'agenda.html', context={"notes":todays_note[0],"dates":[tomorrow,yesterday]})


def updateAgenda(req):
    date = req.POST.get('date','')
    notes = req.POST.get('notes','')

    Notes.objects.update_or_create(
        pub_date = date,
        defaults={'notes': notes, 'pub_date': date},
    )

    return HttpResponse("success")

# @ get /get-date
def GetDate(req):

    req_date = req.GET.get('date', '')
    note = Notes.objects.filter(pub_date=req_date)

    formatted_date = datetime.datetime.strptime(req_date, '%d-%m-%Y')

    yesterday = formatted_date + datetime.timedelta(days=-1)
    yesterday = yesterday.strftime("%d-%m-%Y")

    tomorrow = formatted_date + datetime.timedelta(days=1)
    tomorrow = tomorrow.strftime("%d-%m-%Y")


    if(note.count() == 0):
        note = Notes()
        note.pub_date = req_date
        return render(req,'agenda.html', context={"notes":note, "dates":[tomorrow,yesterday]})
    else:
        return render(req,'agenda.html', context={"notes":note[0], "dates":[tomorrow,yesterday]})
    
# @ get /weekly
def Weekly(req):
    today = date.today().strftime("%d-%m-%Y")
    days_of_the_week = get_week(today)
    print(days_of_the_week)
    return render(req,'weekly.html',context={"days":days_of_the_week})

def Calendar(req):
    return render(req,'calendar.html')



def get_week(dt):
    week_day= datetime.datetime.now().isocalendar()[2]
    start_date= datetime.datetime.now() - datetime.timedelta(days=week_day)
    dates=[str((start_date + datetime.timedelta(days=i)).date().strftime("%d-%m-%Y")) for i in range(7)]
    return(dates)
