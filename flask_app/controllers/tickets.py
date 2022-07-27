from flask_app import app 
from flask import render_template, redirect, session, request, jsonify
from flask_app.models.user import User 
from flask_app.models.ticket import Ticket


@app.route('/allTickets')
def allTickets(): 
    if 'user_id' not in session : 
        return redirect('/logout')
    return render_template("tickets.html", tickets=Ticket.getAll())


@app.route('/addTicket', methods=['POST'])
def addTicket(): 
    if 'user_id' not in session : 
        return redirect('/logout')
    data = {
        "title": request.form['title'],
        "type": request.form['type'],
        "description": request.form['description'],
        "priority": request.form['priority'],
        "status": request.form['status'],
        "project_id": request.form['project_id'],
        "dev_id": request.form['dev_id'],
        "user_id": session['user_id'],
    }
    Ticket.save(data)
    print(data)
    return redirect(f"/show/project/{request.form['project_id']}")



@app.route('/delete/ticket/<int:id>')
def deleteTicket(id):
    if 'user_id' not in session: 
        return redirect('/logout')
    data = {
        "id":id
    }
    Ticket.delete(data)
    return redirect('/allTickets')



@app.route('/show/ticket/<int:id>')
def showTicket(id): 
    if 'user_id' not in session: 
        return redirect('/logout')
    data = {
        'id': id
    }
    userData = {
        "id": session['user_id']
    }
    return render_template('showTicket.html', user=User.getOne(userData), users=User.getAll(), ticket=Ticket.getTicketComments(data), dev=Ticket.getTicketDev(data))


@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' not in session: 
        return redirect('/logout')
    data = {
        "id": id,
    }
    userData = {
        "id": session['user_id']
    }
    return render_template('edit.html', editTicket=Ticket.getOneTicket(data), user=User.getOne(userData), project=Ticket.getTicketProject(data))


@app.route('/update', methods=['POST']) 
def update():
    if 'user_id' not in session:
        return redirect('/logout')

    data = {
        "id": request.form['id'],
        "title": request.form['title'],
        "type": request.form['type'],
        "description": request.form['description'],
        "priority": request.form['priority'],
        "status": request.form['status'],
        "project_id": request.form['project_id'],
        "dev_id": request.form['dev_id'],
        "user_id": session['user_id'],
    }
    Ticket.update(data)
    return redirect(f"/show/ticket/{request.form['id']}")
