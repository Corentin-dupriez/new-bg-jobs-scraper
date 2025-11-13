import duckdb

con = duckdb.connect("jobs.duckdb")


con.execute("select * from fact_listings limit 1")
print(con.fetchall())
