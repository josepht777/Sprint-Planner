
from sqlite3 import Date
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import *
from . import db
from datetime import datetime, date, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import copy
#a blueprint is something that has a punch of routes inside of it. It is a way to separate the app out

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")


@views.route('/tasks', methods = ['GET', 'POST'])
def tasks():
    db.create_all()
    all_tasks = Task.query.all()

    sorted_tasks = []
    filtered_tasks = []
    if request.method == 'POST':
        tag = request.form.get('tag')
        sort = request.form.get('sort')

        if tag != "None" and sort == "None":
            for task in all_tasks:
                if task.tag == tag:
                    filtered_tasks.append(task)
            if len(filtered_tasks) == 0:
                flash("No tasks with tag exist", category = 'error')
            else:
                return render_template("tasks.html", tasks = filtered_tasks)

        elif tag == "None" and sort == "None":     
            flash("Please select a valid category for filtering or sorting", category = 'error')   
        
        elif tag == "None" and sort == "Name":
            for z in all_tasks:
                print(z.name)
            sorted_tasks=Task.query.order_by(Task.name).all()
            for w in sorted_tasks:
                print(w.name)
            if len(sorted_tasks) == 0:
                flash("No task with name exist", category = 'error')
            else:
                return render_template("tasks.html", tasks = sorted_tasks)

        elif tag == "None" and sort == "Status":
            sorted_tasks=Task.query.order_by(Task.status).all()
            if len(sorted_tasks) == 0:
                flash("No task with status exist", category = 'error')
            else:
                return render_template("tasks.html", tasks = sorted_tasks)


        elif tag != "None" and sort == "Name":
            sorted_tasks=Task.query.order_by(Task.name).all()
            for task in sorted_tasks:
                if task.tag == tag:
                    filtered_tasks.append(task)
            return render_template("tasks.html", tasks = filtered_tasks)


        elif tag != "None" and sort == "Status":
            sorted_tasks=Task.query.order_by(Task.status).all()
            for task in sorted_tasks:
                if task.tag == tag:
                    filtered_tasks.append(task)
            return render_template("tasks.html", tasks = filtered_tasks)



    return render_template("tasks.html", tasks = all_tasks)





@views.route('/create-task', methods = ['GET', 'POST'])
def create_task():
    validData = True
    db.create_all()
    all_users = User.query.all()

    if request.method == 'POST':
        name = request.form.get('name')
        type = request.form.get('type')
        storyPoint = request.form.get('storyPoint')
        tag = request.form.get('tag')
        priority = request.form.get('priority')
        status = request.form.get('status')

        assignee = ''
        listOfName = request.form.get('assignee').split()
        assigneeLastName = listOfName[1].strip()
        for user in all_users:
            if user.lastName.strip() == assigneeLastName:
                assignee = user.id
        if assignee == '':
            flash("assignee cannot be blank", category = 'error')
        if len(all_users) == 0:
            flash("MUST ADD USERS BEFORE CREATING TASKS!", category = 'error')
            validData = False

        description = request.form.get('description')

        if not(storyPoint.isnumeric()):
            flash("Story Point value must be a number!", category = 'error')
            validData = False


        
        
        
        if validData:
            new_task = Task(name=name, type=type, storyPoint = storyPoint, tag = tag, priority = priority,assignee = assignee, status = status, description = description)
            db.session.add(new_task)
            db.session.commit()

            flash('Task Successfully created', category = 'success')
            return redirect(url_for('views.tasks'))
    
    return render_template("create-task.html", users = all_users)



@views.route('/edit_task/<task_ID>', methods = ['GET', 'POST'])
def edit_task(task_ID):
    db.create_all()
    all_users = User.query.all()
    
    task_to_edit = Task.query.get(task_ID)

    if request.method == 'POST':
        

        if request.form.get("name") != task_to_edit.name:
            task_to_edit.name = request.form.get('name')
        if request.form.get("type") != task_to_edit.type:
            task_to_edit.type = request.form.get('type')
        if request.form.get("storyPoint") != task_to_edit.storyPoint:
            task_to_edit.storyPoint = request.form.get('storyPoint')
        if request.form.get('tag') != task_to_edit.tag:
            task_to_edit.tag = request.form.get('tag')
        if request.form.get('priority') != task_to_edit.priority:
            task_to_edit.priority = request.form.get('priority')
        if request.form.get("status") != task_to_edit.status:
            task_to_edit.status = request.form.get('status')
        if request.form.get("assignee") != task_to_edit.assignee:
            task_to_edit.assignee = request.form.get('assignee')
        if request.form.get("description") != task_to_edit.description:
            task_to_edit.description = request.form.get('description')

        db.session.commit()
        flash('Task successfully edited', category = 'success')
        return redirect(url_for('views.tasks'))

    return render_template('edit_task.html', task = task_to_edit, users = all_users)


@views.route('/delete_task/<task_ID>')
def delete_task(task_ID):
    task_to_delete = Task.query.get(task_ID)
    db.session.delete(task_to_delete)
    db.session.commit()
    flash("Task Successfully Deleted", category = 'success')
    return redirect(url_for('views.tasks'))


@views.route('/start_sprint/<sprint_ID>')
def start_sprint(sprint_ID):
    db.create_all()
    all_sprints = Sprint.query.all()
    validSprint = True
    db.create_all()
    this_sprint = Sprint.query.get(sprint_ID)
    if len(this_sprint.tasks)==0:
        flash("Must select tasks before starting sprint!", category='error')
        validSprint = False

    numberOfCurrentSprints = 0
    for sprint in all_sprints:
        if sprint.status == 'current':
            numberOfCurrentSprints +=1
    if numberOfCurrentSprints>0:
        flash("Only 1 sprint can be started at at a time!", category='error')
        validSprint = False


    if validSprint:
        this_sprint.status = 'current'
        db.session.commit()
    return redirect(url_for('views.sprints'))



@views.route('/sprints')
def sprints():
    db.create_all()
    all_users = User.query.all()
    db.create_all()
    all_sprints = Sprint.query.all()

    return render_template("sprints.html", sprints = all_sprints, users = all_users)



@views.route('/create-sprint', methods = ['GET', 'POST'])
def create_sprint():
    validData = True
    if request.method == 'POST':
        name = request.form.get('name')
        start_date = request.form.get('start_date', type = toDate)
        end_date = request.form.get('end_date', type = toDate)
        if start_date > end_date or start_date == end_date:
            flash('Start date must be before end date!', category = 'error')
            validData = False

        if validData:
            new_sprint = Sprint(name=name, start_date = start_date, end_date = end_date)
            db.session.add(new_sprint)
            db.session.commit()
            flash('Sprint Successfully created', category = 'success')
            return redirect(url_for('views.sprints'))

    return render_template("create-sprint.html")




@views.route('/add_tasks/<sprint_ID>', methods = ['GET', 'POST'])
def add_tasks(sprint_ID):
    
    db.create_all()
    all_tasks = Task.query.all()
    this_sprint = Sprint.query.get(sprint_ID)

    

    if request.method == 'POST':
        task_id_list = request.form.getlist('checklist')

        for task in all_tasks:
            if (task.is_added == False) or (task in this_sprint.tasks):
                task_to_change = Task.query.get(task.id)            
                if str(task.id) in task_id_list:
                    task_to_change.sprint_id = sprint_ID
                    task_to_change.is_added = True
                else:
                    task_to_change.sprint_id = None
                    task_to_change.is_added = False
                
        db.session.commit()
        return redirect(url_for('views.sprints'))
    
    return render_template("select-task.html", tasks = all_tasks, this_sprint = this_sprint)


@views.route('/add_time/<sprint_ID>/<task_ID>', methods = ['GET', 'POST'])
def add_time(sprint_ID,task_ID):
    validData = True
    db.create_all()
    all_users = User.query.all()

    db.create_all()
    this_sprint = Sprint.query.get(sprint_ID)
    task_list = Task.query.all()
    this_task = None

    for task in task_list:
        if int(task_ID) == task.id:
            this_task = task
            break

    if request.method == 'POST':

        time_spent = request.form.get("time")
        date = request.form.get('date', type = toDate)
        if date <this_sprint.start_date or date > this_sprint.end_date:
            validData = False
            flash("Date must be during the sprint period", category='error')

        user_id = ''
        listOfName = request.form.get('assignee').split()
        assigneeLastName = listOfName[1].strip()
        for user in all_users:
            if user.lastName.strip() == assigneeLastName:
                user_id = user.id
        if user_id == '':
            flash("PLEASE CONTACT DEVELOPER! ERROR CODE AREA51", category = 'error')
        task_id = this_task.id

        if validData:
            new_Workstamp = Workstamp(hours = time_spent, user_id = user_id, date = date, task_id = task_id)
            db.session.add(new_Workstamp)
            db.session.commit()
        
            this_task.total_time += float(time_spent)
            db.session.commit()
            return redirect(url_for('views.sprints'))


    return render_template("add_time.html", users = all_users, task = this_task)


def toDate(dateString): 
    return datetime.strptime(dateString, "%Y-%m-%d").date()

@views.route('/add_user', methods = ['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        
        new_user = User(firstName = firstName, lastName = lastName, email = email)
        db.session.add(new_user)
        db.session.commit()
        
        
        flash('User Successfully added', category = 'success')
        
        return redirect(url_for('views.users'))

    return render_template("add_user.html")

@views.route('/delete_user/<user_ID>')
def delete_user(user_ID):
    user_to_delete = User.query.get(user_ID)
    db.session.delete(user_to_delete)
    db.session.commit()
    flash("User Successfully Deleted")
    return redirect(url_for('views.users'))

@views.route('/users', methods = ['GET', 'POST'])
def users():
    ListOfRGBColors = ['rgb(255, 51, 51)','rgb(255, 153, 51)','rgb(255, 255, 51)', 'rgb(51, 255, 51)', 'rgb(51, 51, 255)', 'rgb(153, 51, 255)', 'rgb(255, 51, 51)', 'rgb(255, 51, 255)','rgb(255, 51, 153)' ]
    db.create_all()
    all_users = User.query.all()
    db.create_all()
    all_sprints = Sprint.query.all()
    this_sprint = None
    for sprint in all_sprints:
        if sprint.status == 'current':
            this_sprint = sprint
            break
    if this_sprint != None:

        for sprint in all_sprints:
            if sprint.status == 'current':
                this_sprint = sprint
                break


        #getting total story point to calculate estimated hours needed sprint
        totalStoryPoints = 0
        for task in this_sprint.tasks:
            totalStoryPoints += task.storyPoint
        totolHoursNeededForSprint = totalStoryPoints*4
        totolHoursPerPerson = totolHoursNeededForSprint/len(all_users)
        

        #intiate all needed vaiables
        listOfAllDates = []
        start_date = copy.deepcopy(this_sprint.start_date)
        listOfAllDates.append(start_date)
        end_date = this_sprint.end_date
        
        #extract everyday from first date till end of sprint
        while not(start_date > end_date or start_date == end_date):
            listOfAllDates.append(start_date)
            start_date = start_date + timedelta(days=1)
        
        listOfAllDates2 = []
        for date in listOfAllDates:
            listOfAllDates2.append(date.isoformat())
        
        
        #collect all ids of tasks for this_sprint
        listOfTaskIds = []
        for task in this_sprint.tasks:
            listOfTaskIds.append(task.id)
        


        db.create_all()
        all_workstamps = Workstamp.query.all()
        
        #each person should have their own stamps
        listsOfData = []

        for user in all_users:
            personsStamps = []
            for stamp in all_workstamps:
                if stamp.task_id in listOfTaskIds and stamp.user_id == user.id:
                    personsStamps.append(stamp)

            data = []
            todaysHours = 0
            for date in listOfAllDates:
                lstOfSamedayStamps = []
                for stamp in personsStamps:
                    if stamp.date.isoformat() == date.isoformat():
                        lstOfSamedayStamps.append(stamp)
                if len(lstOfSamedayStamps) == 1:
                    todaysHours += lstOfSamedayStamps[0].hours
                if len(lstOfSamedayStamps) > 1:
                    for stamp in lstOfSamedayStamps:
                        todaysHours += stamp.hours
                value = (todaysHours)
                data.append(value)
        
            listsOfData.append((user,data))

            #NOT DONE ---------------
        
        

        

        # data = [("01-01-2020", 1597),("01-01-2020", 1456),("02-01-2020", 1908),("03-01-2020", 896),("04-01-2020", 755),("05-01-2020", 453),("07-01-2020", 1100),("08-01-2020", 1235),("09-01-2020", 1478)]
        # labels =[row[0] for row in data]
        # values =[row[1] for row in data]
    

        
        increment = totolHoursPerPerson/len(listOfAllDates)
        values2 =[]
        tempo = increment
        for _ in range(len(listOfAllDates)):
            values2.append(tempo)
            tempo += increment

        listsOfUserData = []
        for user in all_users:
            userData = []
            userId = user.id
            userData.append(userId)

            #get names of each user
            name = user.firstName +" " + user.lastName
            userData.append(name)

            assignedTasks = ''
            #get name of assigned task(s) of each user
            for task in this_sprint.tasks:
                if task.assignee == user.id and assignedTasks == '':
                    assignedTasks += task.name
                elif task.assignee == user.id:
                    assignedTasks += ', '+task.name
            if assignedTasks == '':
                assignedTasks = 'None'
            userData.append(assignedTasks)
            
            #get total hours of each user
            person_hours = 0
            for stamp in all_workstamps:
                if stamp.task_id in listOfTaskIds and stamp.user_id == user.id:
                    person_hours += stamp.hours 
            userData.append(person_hours)

            listsOfUserData.append(userData)
        
        
        return render_template("users.html", users = all_users, data = listsOfData, values2 = values2, this_sprint = this_sprint, table = True, labels = listOfAllDates2,ListOfRGBColors=ListOfRGBColors,listsOfUserData=listsOfUserData)
    else:return render_template("users.html", users = all_users, table = False)




@views.route('/view_sprint_board/<sprint_ID>', methods = ['GET', 'POST'])
def view_sprint_board(sprint_ID):
    db.create_all()
    this_sprint = Sprint.query.get(sprint_ID)
    return render_template("sprint_board.html", sprint = this_sprint)

@views.route('/view_burndown_chart/<sprint_ID>', methods = ['GET', 'POST'])
def view_burndown_chart(sprint_ID):
    db.create_all()
    this_sprint = Sprint.query.get(sprint_ID)

    #getting total story point to calculate estimated hours needed sprint
    totalStoryPoints = 0
    for task in this_sprint.tasks:
        totalStoryPoints += task.storyPoint
    totolHoursNeededForSprint = totalStoryPoints*4
    

    #intiate all needed vaiables
    listOfAllDates = []
    start_date = copy.deepcopy(this_sprint.start_date)
    listOfAllDates.append(start_date)
    end_date = this_sprint.end_date
    
    #extract everyday from first date till end of sprint
    while not(start_date > end_date or start_date == end_date):
        listOfAllDates.append(start_date)
        start_date = start_date + timedelta(days=1)
    

    #collect all ids of tasks
    listOfTaskIds = []
    for task in this_sprint.tasks:
        listOfTaskIds.append(task.id)
    

    #collect all workstamps for sprint
    db.create_all()
    listOfSprintWorkstamps = []
    all_workstamps = Workstamp.query.all()
    for stamp in all_workstamps:
        if stamp.task_id in listOfTaskIds:
            listOfSprintWorkstamps.append(stamp)

    data = []
    todaysHours = 0
    for date in listOfAllDates:
        lstOfSamedayStamps = []
        for stamp in listOfSprintWorkstamps:
            if stamp.date.isoformat() == date.isoformat():
                lstOfSamedayStamps.append(stamp)
        if len(lstOfSamedayStamps) == 1:
            todaysHours += lstOfSamedayStamps[0].hours
        if len(lstOfSamedayStamps) > 1:
            for stamp in lstOfSamedayStamps:
                todaysHours += stamp.hours
        coordinate = (date.isoformat(),todaysHours)
        data.append(coordinate)

    # data = [("01-01-2020", 1597),("01-01-2020", 1456),("02-01-2020", 1908),("03-01-2020", 896),("04-01-2020", 755),("05-01-2020", 453),("07-01-2020", 1100),("08-01-2020", 1235),("09-01-2020", 1478)]
    labels =[row[0] for row in data]
    values =[row[1] for row in data]

    
    increment = totolHoursNeededForSprint/len(listOfAllDates)
    values2 =[]
    tempo = increment
    for _ in range(len(listOfAllDates)):
        values2.append(tempo)
        tempo += increment

    

    return render_template("burndown_chart.html", labels = labels, values = values, values2 = values2, this_sprint = this_sprint)



@views.route('/progress_task/<sprint_ID>/<task_ID>', methods = ['GET', 'POST'])
def progress_task(sprint_ID,task_ID):
    db.create_all()
    all_users = User.query.all()
    db.create_all()
    all_sprints = Sprint.query.all()
    db.create_all()
    all_tasks = Task.query.all()
    db.create_all()
    this_sprint = Sprint.query.get(sprint_ID)
    this_task = Task.query.get(task_ID)

    lstOfSprintIDs = []
    if all_sprints:
        for sprint in all_sprints:
            lstOfSprintIDs.append(sprint.id)
    lstOfTaskIDs = []
    if all_tasks:
        for task in all_tasks:
            lstOfTaskIDs.append(task.id)

    if sprint_ID in lstOfSprintIDs:
        flash(str(sprint_ID) +"passes")

    # if sprint_ID in lstOfSprintIDs or task_ID in lstOfTaskIDs:
    if sprint_ID != this_task.sprint_id:
        if this_task.status == "Not Started":
            this_task.status = 'On Going'
            db.session.commit()
        elif this_task.status == 'On Going':
            this_task.status = 'Completed'
            db.session.commit()
        elif this_task.status == 'Completed':
            flash("Cannot progress task that is completed", category = 'error')
    #     else:
    #         flash("invalid url", category = 'error')
    # else:flash("invalid sprint ID or task ID to render this page", category = 'error')

    for sprint in all_sprints:
        if 'current' == sprint.status:
            fullyCompleted = True
            for task in sprint.tasks:
                if task.status != 'Completed':
                    fullyCompleted = False
            if fullyCompleted:
                sprint.status = 'completed'
                db.session.commit()
                
                return redirect(url_for("views.sprints"))
    
    return render_template("sprint_board.html", sprint = this_sprint)
