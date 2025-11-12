import duckdb

con = duckdb.connect("jobs.duckdb")

con.execute("select * from dim_date")
print(con.fetchall())
