import io

from django.shortcuts import render,redirect
from .models import Notes,Project
from django.http import HttpResponse, FileResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from datetime import date
import datetime

from django.core import serializers
import json
# UTC Timezone + 3
timezone = 3

def index(req):
    utc_converted = datetime.datetime.now() +  datetime.timedelta(hours=timezone)
    return redirect('/get?date='+utc_converted.strftime("%Y-%m-%d"))

# @ post /update
def updateAgenda(req):
    notes = req.POST.get('notes','')
    project_id = req.POST.get('project_id','')
    if(len(project_id)>0):
        project = Project.objects.get(id=project_id)
        project.notes = notes
        project.save()

    else:
        date = datetime.datetime.strptime(req.POST.get('date',''), '%Y-%m-%d')
        Notes.objects.update_or_create(
            pub_date = date,
            defaults={'notes': notes, 'pub_date': date},
        )

    return HttpResponse("success")

# @ get /get-date
def GetDate(req):

    req_date = req.GET.get('date', '')
    req_project = req.GET.get('project','')
    print(len(req_date),len(req_project))
    projects = Project.objects.all()
    
    print("req date",req_date)

    if(len(req_date)>0):
        note = Notes.objects.filter(pub_date=req_date)

        today = datetime.datetime.strptime(req_date, '%Y-%m-%d')

        yesterday = (today + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")

        tomorrow = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        if(note.count() == 0):
            note = Notes()
            note.pub_date = today.strftime("%Y-%m-%d")
            return render(req,'agenda.html', context={"notes":note, "dates":[tomorrow,yesterday,today],"projects": projects})
        else:
            return render(req,'agenda.html', context={"notes":note[0], "dates":[tomorrow,yesterday,today],"projects": projects})
    
    elif(len(req_project)>0):
        try:
            project = Project.objects.get(id=req_project)
            return render(req,'project.html', context={"notes":project,"projects": projects})
        except ObjectDoesNotExist:        
            return redirect('/')

# @ get /weekly
def Weekly(req):
    projects = Project.objects.all()

    today = date.today().strftime("%Y-%m-%d")
    days_of_the_week = get_week(today)
    print(days_of_the_week)
    return render(req,'weekly.html',context={"days":days_of_the_week,"projects": projects})

def Calendar(req):
    
    
    projects = Project.objects.all()


    return render(req,'calendar.html',context={"projects": projects})


def CalendarSource(req):
    start_date = datetime.datetime.strptime(req.GET.get('start', '').split('T')[0],'%Y-%m-%d')
    end_date =  datetime.datetime.strptime(req.GET.get('end','').split('T')[0],'%Y-%m-%d')
    print(start_date)
    
    notes = Notes.objects.filter(pub_date__range=(start_date,end_date))
    print(len(notes))
    response_obj = []
    for k in notes:
        for l in k.notes.splitlines():
            if(l.startswith('!!')):
                response_data = {}
                response_data['title'] = l[3:]
                response_data['start'] = k.pub_date.strftime("%Y-%m-%d")
                response_data['end'] = k.pub_date.strftime("%Y-%m-%d")
                if(l[2] == 'R'):
                    response_data['color'] = '#eb4034'
                elif(l[2] == 'G'):
                    response_data['color'] = '#32ba20' 
                else:
                    response_data['color'] = '#3788D8'


                response_obj.append(response_data)

    print(response_obj)
    print(start_date)
    print(end_date)
    return HttpResponse(json.dumps(response_obj),content_type="application/json")



def dateModifier(datestring):
    datestring = datestring.split('T')
    datestring = datestring[0].split('-')
    datestring = datestring[2] + '/' + datestring[1] + '/' + datestring[0]
    return datestring

# @ post /update
def AddProject(req):
    title = req.POST.get('title','')
    icon = req.POST.get('icon','')

    Project.objects.update_or_create(
        name = title,
        defaults={'name': title, 'icon': icon, 'notes':''},
    )

    return redirect('/')

def Delete(req):
    project_id = req.GET.get('project', '')
    try:
        project = Project.objects.get(id=project_id)
        project.delete()
        return redirect('/')
    except:
        return redirect('/')

def Settings(req):
    return render(req,'settings.html',context={})


def get_week(dt):
    week_day= datetime.datetime.now().isocalendar()[2]
    start_date= datetime.datetime.now() - datetime.timedelta(days=week_day) + datetime.timedelta(days=1)
    dates=[str((start_date + datetime.timedelta(days=i)).date().strftime("%Y-%m-%d")) for i in range(7)]
    day_names=[str((start_date + datetime.timedelta(days=i)).date().strftime("%A")) for i in range(7)]
    return(zip(dates,day_names))



def DownloadNotes(req):
    data = serializers.serialize('json', Notes.objects.all())
    return HttpResponse(data, content_type='application/json')