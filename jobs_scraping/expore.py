import duckdb

con = duckdb.connect("jobs.duckdb")

con.execute("select * from jobs")
print(con.fetchall())
