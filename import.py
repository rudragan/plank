import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker



engine= create_engine("postgres://cdoyvmjekcwbyn:59acc249ea9b6b81917c302f4bcc0e2446069481be237fa2dc90f50c7e48995e@ec2-34-192-173-173.compute-1.amazonaws.com:5432/d7d3i8n279rrqm")
db =scoped_session(sessionmaker(bind=engine))

def main():
    db.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR NOT NULL, password VARCHAR NOT NULL)")
    
   
        
    print("done")            
    db.commit()    







if __name__ == "__main__":
    main()