from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, ticket


class Project:
    db = 'bugTracker'
    def __init__(self, data):
        self.id  = data['id']
        self.name  = data['name']
        self.description  = data['description']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.user_id = data['user_id']
        self.devs = []
        self.users = []
        self.tickets = []
        self.ticketDev = None
        self.projects = []



    @classmethod
    def save(cls, data):
        query = 'INSERT INTO projects ( name, description, createdAt, updatedAt, user_id ) VALUES ( %(name)s, %(description)s, NOW(), NOW(), %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM projects WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def getOneProject(cls, data):
        query = 'SELECT * from projects WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    

    @classmethod
    def update(cls, data):
        query = "UPDATE projects SET name=%(name)s, description=%(description)s, updatedAt=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def add(cls,data): 
        query = "INSERT INTO projectDevs (user_id, project_id) VALUES (%(user_id)s, %(project_id)s);"
        return connectToMySQL(cls.db).query_db( query, data ) 
    
    @classmethod
    def delete(cls,data): 
        query = "DELETE FROM projectDevs WHERE user_id = %(user_id)s;"
        return connectToMySQL(cls.db).query_db( query, data ) 

    @classmethod 
    def getAllJson(cls): 
        query = "SELECT * FROM projects"
        results = connectToMySQL(cls.db).query_db(query) 
        projectList = []
        for data in results: 
            projectList.append(data) 
        return projectList 
    
    @classmethod
    def getLast(cls): 
        query = "SELECT * FROM projects ORDER BY id DESC LIMIT 1;"
        results = connectToMySQL(cls.db).query_db(query) 
        return results[0]
    

    @classmethod 
    def getProjectDevs(cls,data):
        query = "SELECT * FROM projects LEFT JOIN projectDevs ON projectDevs.project_id = projects.id LEFT JOIN users ON projectDevs.user_id = users.id WHERE projects.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        project = cls(results[0]) 
        for row in results: 
            userData = {
                'id': row['users.id'],
                'firstName': row['firstName'],
                'lastName': row['lastName'],
                'email': row['email'],
                'password': row['password'],
                'access': row['access'],
                'createdAt': row['users.createdAt'],
                'updatedAt': row['users.updatedAt']
            }
            project.devs.append(user.User(userData)) 
            project.users.append(userData["id"])
        return project 
    

    @classmethod 
    def getProjectTickets(cls,data):
        query = "SELECT * FROM projects LEFT JOIN tickets ON projects.id = tickets.project_id LEFT JOIN users on users.id = tickets.dev_id  WHERE projects.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        project = cls(results[0])
        for row in results: 
            data = {
                'id': row['tickets.id'],
                'title': row['title'], 
                'type': row['type'],
                'description': row['tickets.description'],
                'priority': row['priority'],
                'status': row['status'],
                'project_id': row['project_id'],
                'user_id': row['user_id'],
                'dev_id': row['dev_id'],
                'createdAt': row['tickets.createdAt'],
                'updatedAt': row['tickets.updatedAt']
            }
            oneTicket = ticket.Ticket(data)
            oneTicket.ticketDev = user.User.getOne({"id": row["users.id"]})
            project.tickets.append(oneTicket) 
        return project

