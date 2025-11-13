import duckdb

con = duckdb.connect("jobs.duckdb")


con.execute("select distinct(company_name) from jobs")
print(con.fetchall())
