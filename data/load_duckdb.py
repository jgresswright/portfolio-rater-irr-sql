import duckdb, os

local_dir = os.path.dirname(__file__)
db_path = os.path.join(local_dir, "db", "rater_irr.duckdb")
os.makedirs(os.path.dirname(db_path), exist_ok=True)

con = duckdb.connect(db_path)

con.execute("DROP TABLE IF EXISTS raters")
con.execute("DROP TABLE IF EXISTS evaluations")
con.execute("DROP TABLE IF EXISTS ratings")

raters_csv = os.path.join(local_dir, "data", "raters.csv")
evaluations_csv = os.path.join(local_dir, "data", "evaluations.csv")
ratings_csv = os.path.join(local_dir, "data", "ratings.csv")

con.execute(f"""
    CREATE TABLE raters AS
    SELECT * FROM read_csv_auto('{raters_csv}')
""")

con.execute(f"""
    CREATE TABLE evaluations AS
    SELECT * FROM read_csv_auto('{evaluations_csv}')
""")

con.execute(f"""
    CREATE TABLE ratings AS
    SELECT * FROM read_csv_auto('{ratings_csv}')
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
