import sqlite3


# Connecting to the database file
conn = sqlite3.connect("database/" + "users.db")
c = conn.cursor()


# Create table
c.execute('''CREATE TABLE IF NOT EXISTS Users
            (Username string, Password string)''')


user1 = "admin"
password1 = "21232f297a57a5a743894a0e4a801fc3"


# inserts the results which are stored in the list at that moment in time (Change when adding new city)
def insertinto(user,password):
    c.execute("INSERT INTO Users VALUES (?,?)", (user,password))
    print('commited')
    conn.commit()

#insertinto(user1,password1)


# fetches whats in the database
c.execute('select * from Users')
for fetch in c.fetchall():
    print(fetch)

