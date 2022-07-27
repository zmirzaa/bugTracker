from flask_app.config.mysqlconnection import connectToMySQL

class Comment:
    db = 'bugTracker'
    def __init__(self, data):
        self.id  = data['id']
        self.description  = data['description']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.user_id = data['user_id']
        self.ticket_id = data['ticket_id']



    @classmethod
    def save(cls, data):
        query = 'INSERT INTO comments ( description, createdAt, updatedAt, user_id, ticket_id ) VALUES ( %(description)s, NOW(), NOW(), %(user_id)s, %(ticket_id)s );'
        return connectToMySQL(cls.db).query_db(query, data)

