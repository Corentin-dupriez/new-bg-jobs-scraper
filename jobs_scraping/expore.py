import duckdb

con = duckdb.connect("jobs.duckdb")


con.execute("select * from jobs limit 1")
print(con.fetchall())

con.execute("select count(*) from jobs")
print(con.fetchall())
