#!/usr/bin/python3
import sqlalchemy as db
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

if __name__ == "__main__":
    import os
    import sys

    PATH = "/".join(os.path.realpath(__file__).split("/")[0:-2])
    sys.path.insert(1, PATH)
from error import error
from logger import logger


class Database:
    def __init__(self, drivername, username, host, database_name, password, port):
        self.url = URL.create(
            drivername=drivername,
            username=username,
            host=host,
            database=database_name,
            password=password,
            port=port,
        )
        self.engine = db.create_engine(self.url)
        self.session_factory = sessionmaker(bind=self.engine)
        self.session = self.session_factory()
        self.conn = self.engine.connect()

    def query_all(self, table, log=False):
        records = self.session.query(table).all()
        for record in records:
            if log:
                logger.logger.info("%s - %s", __name__, record.as_dict())

    def query_one(self, table, **kwargs):
        for key, value in kwargs.items():
            statement = db.select(table).where(getattr(table, key) == value)
            results = self.conn.execute(statement).fetchall()
            if len(results) == 0:
                raise error.DatabaseError("Not Found!", error.ErrorCode.NOT_FOUND.value)

            predicate = getattr(table, key) == value
            data = self.session.query(table).where(predicate)
            results = []
            for record in data:
                logger.logger.info("%s - %s", __name__, record.as_dict())
                results.append(record.as_dict())
            return results

        return []

    def delete(self, table, **kwargs):
        deleted_id = None
        try:
            for key, value in kwargs.items():
                statement = db.select(table).where(getattr(table, key) == value)
                results = self.conn.execute(statement).fetchall()
                if len(results) == 0:
                    raise error.DatabaseError(
                        "Not Found!", error.ErrorCode.NOT_FOUND.value
                    )

                predicate = getattr(table, key) == value
                stmt = (
                    db.delete(table)
                    .where(predicate)
                    .returning(table.__table__.columns.id)
                )
                deleted_id = list(self.conn.execute(stmt))[0][0]
                self.conn.commit()
        except Exception as e:
            logger.logger.error("%s - %s", __name__, e)
        finally:
            return deleted_id

    def insert(self, table, *args, **kwargs):
        inserted_id = None
        try:
            if len(kwargs):
                stmt = (
                    db.insert(table)
                    .values(**kwargs)
                    .returning(table.__table__.columns.id)
                )
            elif len(args):
                stmt = (
                    db.insert(table).values(*args).returning(table.__table__.columns.id)
                )
            inserted_id = list(self.conn.execute(stmt))[0][0]
            self.conn.commit()
        except Exception as e:
            logger.logger.error("%s - %s", __name__, e)
        finally:
            return inserted_id


database = Database


if __name__ == "__main__":
    from table import DatacampCourse

    mydb = Database(
        drivername="postgresql",
        username="test",
        host="localhost",
        database_name="test",
        password="test",
        port=5432,
    )

    # mydb.delete(DatacampCourse, course_name="spongebob Patrix1")
    for i in range(1, 10):
        mydb.insert(
            DatacampCourse,
            course_name=f"spongebob Patrix{i}",
            course_instructor=f"Spongebob Squarepants LalaSoup{i}",
            topic="Sohai 123",
        )
    mydb.query_all(DatacampCourse)
    mydb.query_one(DatacampCourse, course_name="spongebob Patrix2")
