from flask_app import app 
from flask import render_template, redirect, session, request, jsonify
from flask_app.models.user import User 
from flask_app.models.project import Project



@app.route('/allProjects')
def allProjects(): 
    if 'user_id' not in session : 
        return redirect('/logout')
    
    data = {
        'id': session['user_id']
    }

    return render_template("projects.html", user=User.getOne(data))


@app.route('/addProject', methods=['POST'])
def addProject(): 
    if 'user_id' not in session : 
        return redirect('/logout')
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "user_id": session['user_id'],
    }
    Project.save(data)
    print(data)
    return jsonify(Project.getLast())



@app.route('/delete/project/<int:id>')
def deleteProj(id):
    if 'user_id' not in session: 
        return redirect('/logout')
    data = {
        "id":id
    }
    Project.delete(data)
    return redirect('/dashboard')



@app.route('/show/project/<int:id>')
def showProj(id): 
    if 'user_id' not in session: 
        return redirect('/logout')
    data = {
        'id': id
    }
    userData = {
        "id": session['user_id']
    }
    return render_template('showProject.html', user=User.getOne(userData), users=User.getAll(), project=Project.getProjectTickets(data), devs= Project.getProjectDevs(data))



@app.route("/show/add/<int:id>",  methods=['POST'])
def add(id): 
    data = {
        "project_id": id,
        "user_id": request.form['user_id']
    }
    Project.add(data) 
    return redirect(f"/show/project/{id}")



@app.route('/projects')
def getProjects(): 
    return jsonify(Project.getAllJson())

