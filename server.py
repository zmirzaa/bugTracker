from flask_app import app
from flask_app.controllers import users, projects, tickets, comments


if __name__ == "__main__":
    app.run(debug=True) 