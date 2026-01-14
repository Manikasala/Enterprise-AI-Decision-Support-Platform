import sqlite3

conn = sqlite3.connect("memory.db")
conn.execute("CREATE TABLE IF NOT EXISTS history(query TEXT, response TEXT)")

def store(q, r):
    conn.execute("INSERT INTO history VALUES (?,?)",(q,r))
    conn.commit()
