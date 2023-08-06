import mysql.connector

# run docker image command
# docker run -d -p 3306:3306 --name mysql-docker-container -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=testDB -e MYSQL_USER=admin -e MYSQL_PASSWORD=password mysql


class DbConnector:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="password",
            database="testDB"
        )

