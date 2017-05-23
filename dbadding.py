import sqlite3

# Connecting to the database file
conn = sqlite3.connect("database/" + "motiondb.db")
c = conn.cursor()


c.execute("INSERT INTO Motions VALUES ('16.04.2017', 23)")
conn.commit()
