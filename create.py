from cs50 import SQL

db = SQL("sqlite:///moovie.db")


def main():
    
    x = db.execute("CREATE TABLE movies (id serial PRIMARY KEY,name VARCHAR NOT NULL,year INTEGER NOT NULL, description VARCHAR NOT NULL, image VARCHAR);")


    print(x)
if __name__ == "__main__":
    main()