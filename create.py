from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# Set up database
engine = create_engine("postgres://moujwumorxinad:e33450750c03940b0a975117ef00e99fde8904e5c7ad9a22c02af11a8b019127@ec2-44-193-150-214.compute-1.amazonaws.com:5432/d4206p5ccjqhor")
db = scoped_session(sessionmaker(bind=engine))



def main():
    
    x = db.execute("CREATE TABLE movies (id serial PRIMARY KEY,name VARCHAR NOT NULL,year INTEGER NOT NULL, description VARCHAR NOT NULL, image VARCHAR);")
    db.commit()

if __name__ == "__main__":
    main()