from django.shortcuts import render,redirect
from .models import Notes,Project
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
from datetime import date
import datetime

def index(req):
    today = date.today().strftime("%d-%m-%Y")
    return redirect('/get?date='+today)

# @ post /update
def updateAgenda(req):
    date = req.POST.get('date','')
    notes = req.POST.get('notes','')
    project_id = req.POST.get('project_id','')
    
    if(len(project_id)>0):
        project = Project.objects.get(id=project_id)
        project.notes = notes
        project.save()

    else:
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
    
    if(len(req_date)>0):
        note = Notes.objects.filter(pub_date=req_date)

        formatted_date = datetime.datetime.strptime(req_date, '%d-%m-%Y')

        yesterday = formatted_date + datetime.timedelta(days=-1)
        yesterday = yesterday.strftime("%d-%m-%Y")

        tomorrow = formatted_date + datetime.timedelta(days=1)
        tomorrow = tomorrow.strftime("%d-%m-%Y")


        if(note.count() == 0):
            note = Notes()
            note.pub_date = req_date
            return render(req,'agenda.html', context={"notes":note, "dates":[tomorrow,yesterday],"projects": projects})
        else:
            return render(req,'agenda.html', context={"notes":note[0], "dates":[tomorrow,yesterday],"projects": projects})
    
    elif(len(req_project)>0):
        try:
            project = Project.objects.get(id=req_project)
            return render(req,'project.html', context={"notes":project,"projects": projects})
        except ObjectDoesNotExist:        
            return redirect('/')

# @ get /weekly
def Weekly(req):
    projects = Project.objects.all()

    today = date.today().strftime("%d-%m-%Y")
    days_of_the_week = get_week(today)
    print(days_of_the_week)
    return render(req,'weekly.html',context={"days":days_of_the_week,"projects": projects})

def Calendar(req):
    projects = Project.objects.all()

    return render(req,'calendar.html',context={"projects": projects})


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

def get_week(dt):
    week_day= datetime.datetime.now().isocalendar()[2]
    start_date= datetime.datetime.now() - datetime.timedelta(days=week_day) + datetime.timedelta(days=1)
    dates=[str((start_date + datetime.timedelta(days=i)).date().strftime("%d-%m-%Y")) for i in range(7)]
    day_names=[str((start_date + datetime.timedelta(days=i)).date().strftime("%A")) for i in range(7)]
    return(zip(dates,day_names))


