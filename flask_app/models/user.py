from flask_app.config.mysqlconnection import connectToMySQL 
from flask import flash 
from flask_app.models import project, ticket
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User: 
    db = 'bugTracker'
    def __init__(self,data): 
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.email = data['email']
        self.password = data['password']
        self.access = data['access']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.projects = [] 
        self.tickets = []
    


    @staticmethod
    def validate(user):
        isValid = True
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(User.db).query_db(query,user)
        print(results)
        if len(results) >= 1:
            isValid = False
            flash("That email is already taken!", "register")
        if not EMAIL_REGEX.match(user['email']):
            isValid = False
            flash("Invalid email format.", "register")
        if len(user['password']) < 8:
            isValid = False
            flash('Password must be at least 8 characters long', "register")
        if user['password'] != user['confirm']:
            isValid = False
            flash('Passwords do not match', "register")
        return isValid
    

    @classmethod 
    def getOne(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;' 
        results = connectToMySQL(cls.db).query_db(query, data) 
        if len(results) < 1: 
            return False 
        return cls(results[0]) 
        
    @classmethod
    def getAll(cls): 
        query = 'SELECT * FROM users;' 
        results = connectToMySQL(cls.db).query_db(query) 
        users = [] 
        for u in results: 
            users.append(cls(u))
        return users 

    @classmethod 
    def getEmail(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;' 
        results = connectToMySQL(cls.db).query_db(query, data) 
        if len(results) < 1: 
            return False 
        return cls(results[0]) 
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( firstName , lastName, email , password, createdAt, updatedAt ) VALUES ( %(firstName)s , %(lastName)s, %(email)s , %(password)s, NOW() , NOW() );"
        return connectToMySQL(cls.db).query_db( query, data )
    

    @classmethod
    def update(cls,data): 
        query = "UPDATE users SET access=%(access)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db( query, data )
    
    
    
    @classmethod
    def userTickets(cls,data): 
        query = "SELECT * FROM users LEFT JOIN tickets ON users.id = tickets.dev_id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        tickets = []
        for row in results: 
            data = {
                'id': row['tickets.id'],
                'title': row['title'],
                'type': row['type'],
                'status': row['status'],
                'priority': row['priority'],
                'dev_id': row['dev_id'],
                'project_id': row['project_id'],
                'description': row['description'],
                'user_id': row['user_id'],
                'createdAt': row['tickets.createdAt'],
                'updatedAt': row['tickets.updatedAt']
            }
            tickets.append(ticket.Ticket(data)) 
        return tickets 

    @classmethod 
    def userProjects(cls,data):
        query = "Select * from users left join projectDevs on users.id = projectDevs.user_id left join projects ON projects.id = projectDevs.project_id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        projects = [] 
        for row in results: 
            data = {
                'id': row["projects.id"],
                'name': row['name'], 
                'description': row['description'],
                'user_id': row['user_id'], 
                'createdAt': row['projects.createdAt'],
                'updatedAt': row['projects.updatedAt']
            }
            projects.append(project.Project(data))
        return projects 
