from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, project, comment

class Ticket:
    db = 'bugTracker'
    def __init__(self, data):
        self.id  = data['id']
        self.title  = data['title']
        self.type  = data['type']
        self.description  = data['description']
        self.priority  = data['priority']
        self.status  = data['status']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.user_id = data['user_id']
        self.project_id = data['project_id']
        self.dev_id = data['dev_id']
        self.comments = []
        self.commenter = None
        self.ticketDev = None
        self.ticketProj = None
        self.tickets = []
        self.users = []
        self.devs = []


    @classmethod
    def save(cls, data):
        query = 'INSERT INTO tickets (title, type, description, priority, status, createdAt, updatedAt, user_id, project_id, dev_id ) VALUES ( %(title)s, %(type)s, %(description)s, %(priority)s, %(status)s, NOW(), NOW(), %(user_id)s, %(project_id)s, %(dev_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM tickets WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def getOneTicket(cls, data):
        query = 'SELECT * from tickets WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    

    @classmethod
    def update(cls, data):
        query = "UPDATE tickets SET title=%(title)s, type=%(type)s, description=%(description)s, status=%(status)s, priority=%(priority)s, dev_id=%(dev_id)s, updatedAt=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    


    @classmethod
    def getAll(cls):
            query ="SELECT * FROM tickets;"
            results = connectToMySQL(cls.db).query_db(query)
            tickets = []

            for t in results:
                tickets.append(cls(t))
            return tickets 
    

    @classmethod 
    def getTicketComments(cls,data):
        query = "SELECT * FROM tickets LEFT JOIN comments ON tickets.id = comments.ticket_id LEFT JOIN users on users.id = comments.user_id WHERE tickets.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        ticket = cls(results[0])
        for row in results: 
            commentData = {
                'id': row['comments.id'],
                'description': row['comments.description'],
                'ticket_id': row['ticket_id'],
                'user_id': row['user_id'],
                'createdAt': row['comments.createdAt'],
                'updatedAt': row['comments.updatedAt']
            }
            oneComment = comment.Comment(commentData)
            oneComment.commenter = user.User.getOne({"id": row["users.id"]})
            ticket.comments.append(oneComment) 
        return ticket
    
    @classmethod
    def getTicketDev(cls,data):
        query = "SELECT * FROM tickets LEFT JOIN users on users.id = tickets.dev_id WHERE tickets.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        ticket = cls(results[0])
        for row in results: 
            devData = {
                'id': row['users.id'],
                'firstName': row['firstName'],
                'lastName': row['lastName'],
                'email': row['email'],
                'password': row['password'],
                'access': row['access'],
                'createdAt': row['users.createdAt'],
                'updatedAt': row['users.updatedAt']
            }
            ticket.ticketDev = (user.User(devData)) 
            ticket.users.append(devData["id"])
        return ticket 
    
    @classmethod
    def getTicketProject(cls,data): 
        query="SELECT * FROM tickets LEFT JOIN projects on projects.id = tickets.project_id LEFT JOIN projectDevs on projectDevs.project_id = projects.id LEFT JOIN users on users.id = projectDevs.user_id WHERE tickets.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        oneProject = cls(results[0])
        for row in results: 
            data = {
                'id': row["projects.id"],
                'name': row['name'], 
                'description': row['description'],
                'user_id': row['user_id'], 
                'createdAt': row['projects.createdAt'],
                'updatedAt': row['projects.updatedAt']
            }
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
            oneProject.ticketProj = (project.Project(data))
            oneProject.tickets.append(data["id"])
            oneProject.devs.append(user.User(userData)) 
            oneProject.users.append(userData["id"])
        return oneProject 
            



    
