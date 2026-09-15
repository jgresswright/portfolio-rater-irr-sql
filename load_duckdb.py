import duckdb, os

local_dir = os.path.dirname(__file__)

con = duckdb.connect(local_dir, "db/rater_irr.duckdb")

con.execute("DROP TABLE IF EXISTS raters")
con.execute("DROP TABLE IF EXISTS evaluations")
con.execute("DROP TABLE IF EXISTS ratings")

con.execute("""
    CREATE TABLE raters AS
    SELECT * FROM read_csv_auto(local_dir, 'data/raters.csv')
""")

con.execute("""
    CREATE TABLE evaluations AS
    SELECT * FROM read_csv_auto(local_dir, 'data/evaluations.csv')
""")

con.execute("""
    CREATE TABLE ratings AS
    SELECT * FROM read_csv_auto(local_dir, 'data/ratings.csv')
""")

print(con.execute("SELECT COUNT(*) FROM raters").fetchall())
print(con.execute("SELECT COUNT(*) FROM evaluations").fetchall())
print(con.execute("SELECT COUNT(*) FROM ratings").fetchall())

print("\nSchema check:")
for tbl in ["raters", "evaluations", "ratings"]:
    print(f"\n{tbl}:")
    print(con.execute(f"DESCRIBE {tbl}").fetchdf().to_string(index=False))

con.close()
print("\nSaved to db/rater_irr.duckdb")
