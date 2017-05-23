import sqlite3

# Connecting to the database file
conn = sqlite3.connect("database/" + "motiondb.db")
c = conn.cursor()


# Create table
c.execute('''CREATE TABLE IF NOT EXISTS Motions
            (Date float, Time int)''')


# inserts the results which are stored in the list at that moment in time (Change when adding new city)
def insertinto(motion):
    c.execute("INSERT INTO Motions VALUES (?,?)", motion)
    print('commited')
    conn.commit()

# fetches whats in the database
#c.execute('select * from Motions')
#for fetch in c.fetchall():
    #print(fetch)

