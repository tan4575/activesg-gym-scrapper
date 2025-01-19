#!/bin/bash/python3
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
import sqlalchemy as db

if __name__ == "__main__":
    import os, sys
    PATH = "/".join(os.path.realpath(__file__).split("/")[0:-2])
    sys.path.insert(1,PATH)
from logger import logger
from error import error

class database():
    def __init__(self, drivername, username,host, database,password, port):
        self.url = URL.create(
            drivername=drivername,
            username=username,
            host=host,
            database=database,
            password=password,
            port = port
        )
        self.engine         = db.create_engine(self.url)
        self.Session        = sessionmaker(bind=self.engine)
        self.session        = self.Session()
        self.conn           = self.engine.connect()

    def queryAll(self, table, log=False):
        data    = self.session.query(table).all()
        for s in data:
            if log:
                logger.logger.info("%s - %s", __name__ ,s.as_dict())

    def queryOne(self, table,*args, **kwargs):
        for k, v in kwargs.items():
            statement = db.select(table).where((getattr(table,k) == v))
            results = self.conn.execute(statement).fetchall()
            if len(results)==0:
                raise error.DbException("Not Found!", error.ERROR_CODE.NOT_FOUND.value)
            else:
                t = getattr(table,k) == v
                data = self.session.query(table).where((t))
                retData = []
                for s in data:
                    logger.logger.info("%s - %s", __name__ ,s.as_dict())
                    retData.append(s.as_dict())
                return retData

    def delete(self , table ,*args, **kwargs):
        ret = None
        try :
            for k, v in kwargs.items():
                statement = db.select(table).where((getattr(table,k) == v))
                results = self.conn.execute(statement).fetchall()
                if len(results)==0:
                    raise error.DbException("Not Found!", error.ERROR_CODE.NOT_FOUND.value)
                else:
                    t = getattr(table,k) == v
                stmt = db.delete(table).where((t)).returning(table.__table__.columns.id)
                ret = list(self.conn.execute(stmt))[0][0]
                self.conn.commit()
        except Exception as e:
            logger.logger.error("%s - %s", __name__ ,e)
        finally:
            return ret

    def insert(self, table, *args, **kwargs):
        ret = None
        try :
            if len(kwargs):
                stmt = db.insert(table).values(**kwargs).returning(table.__table__.columns.id)
            elif len(args):
                stmt = db.insert(table).values(*args).returning(table.__table__.columns.id)
            ret = list(self.conn.execute(stmt))[0][0]
            self.conn.commit()
        except Exception as e:
            logger.logger.error("%s - %s", __name__ ,e)
        finally:
            return ret


if __name__ == "__main__":
    from table import datacamp_courses

    mydb = database(
            drivername="postgresql",
            username="test",
            host="localhost",
            database="test",
            password="test",
            port = 5432
        )
    
    # mydb.delete(datacamp_courses, course_name= "spongebob Patrix1")
    for i in range(1,10):
        mydb.insert(datacamp_courses, course_name=f"spongebob Patrix{i}", course_instructor=f"Spongebob Squarepants LalaSoup{i}",topic="Sohai 123")
    mydb.queryAll(datacamp_courses)
    mydb.queryOne(datacamp_courses, course_name= "spongebob Patrix2")