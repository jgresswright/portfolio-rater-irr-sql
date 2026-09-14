import duckdb

con = duckdb.connect("/home/claude/sql_portfolio/rater_irr.duckdb")

con.execute("DROP TABLE IF EXISTS raters")
con.execute("DROP TABLE IF EXISTS evaluations")
con.execute("DROP TABLE IF EXISTS ratings")

con.execute("""
    CREATE TABLE raters AS
    SELECT * FROM read_csv_auto('/home/claude/sql_portfolio/data/raters.csv')
""")

con.execute("""
    CREATE TABLE evaluations AS
    SELECT * FROM read_csv_auto('/home/claude/sql_portfolio/data/evaluations.csv')
""")

con.execute("""
    CREATE TABLE ratings AS
    SELECT * FROM read_csv_auto('/home/claude/sql_portfolio/data/ratings.csv')
""")

print(con.execute("SELECT COUNT(*) FROM raters").fetchall())
print(con.execute("SELECT COUNT(*) FROM evaluations").fetchall())
print(con.execute("SELECT COUNT(*) FROM ratings").fetchall())

print("\nSchema check:")
for tbl in ["raters", "evaluations", "ratings"]:
    print(f"\n{tbl}:")
    print(con.execute(f"DESCRIBE {tbl}").fetchdf().to_string(index=False))

con.close()
print("\nSaved to /home/claude/sql_portfolio/rater_irr.duckdb")
