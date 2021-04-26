# open-agenda
Simple markdown agenda for taking notes. Simple and easy to configure. Written with python.

## Features
- Take note with markdown
- Calendar view
- Add projects
- Event Rendering
- Ical Import

![Agenda 1](images/2021-03-05-14-46-55.png)
![Agenda 3](images/2021-04-03-01-51-59.png)

## Event Rendering
- To render event you should start with `!!` in line. It is going to render as an event. Color references:
    * `!!R EventA` renders as red
    * `!!G EventA` renders as green
    * `!!B EventA` renders as blue

## Framework
- Django

## Requirements
- Icalendar


## Installation
```shell
git clone https://github.com/m8/open-agenda
cd open-agenda
pip3 install icalendar
python3 open-agenda/manage.py runserver
```

## To-Do
- [x] Projects
- [ ] Settings Page
- [ ] Export agenda

