from django.db import connection


# Returns all rows from a cursor as a dictionary
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]

    # Make a dictionary of the query result set
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return results


# Executes a query on the database connection
def executeQuery(query, args = None):
    with connection.cursor() as cursor:
        cursor.execute(query, args)

        # If it's a retrieval query 
        if cursor.description:
            return dictfetchall(cursor)


def userExists(userId):
    user = executeQuery("SELECT * FROM users WHERE id = %s", [userId])
    if user:
        return True
    else:
        return False    

def registerUser(user):
    query = '''INSERT INTO users (id, email, firstName, lastName, photoUrl)
    VALUES (%s, %s, %s, %s, %s)'''
    args = list(user.values())
    executeQuery(query, args)



# CREATE TABLE users (
#     id TEXT PRIMARY KEY,
#     email TEXT NOT NULL,
#     firstName TEXT NOT NULL,
#     lastName TEXT NOT NULL,
#     photoUrl TEXT NOT NULL
# );