import pytest
from database import table
from database.database import Database
from error import error


@pytest.fixture
def sqlite_database():
    database = Database("sqlite", None, None, ":memory:", None, None)
    table.Base.metadata.create_all(database.engine)
    yield database
    database.conn.close()
    database.session.close()
    database.engine.dispose()


def test_insert_query_and_delete_record(sqlite_database):
    inserted_id = sqlite_database.insert(
        table.DatacampCourse,
        course_name="Course",
        course_instructor="Instructor",
        topic="Topic",
    )

    assert inserted_id == 1
    assert sqlite_database.query_one(table.DatacampCourse, course_name="Course") == [
        {
            "id": 1,
            "course_name": "Course",
            "course_instructor": "Instructor",
            "topic": "Topic",
        }
    ]
    assert sqlite_database.delete(table.DatacampCourse, course_name="Course") == 1


def test_query_one_raises_when_record_is_missing(sqlite_database):
    with pytest.raises(error.DatabaseError) as exc_info:
        sqlite_database.query_one(table.DatacampCourse, course_name="Missing")

    assert "Error Code: 404" in str(exc_info.value)


def test_query_one_returns_empty_list_without_filters(sqlite_database):
    assert sqlite_database.query_one(table.DatacampCourse) == []


def test_query_all_can_log_records(sqlite_database):
    sqlite_database.insert(
        table.DatacampCourse,
        course_name="Course",
        course_instructor="Instructor",
        topic="Topic",
    )

    assert sqlite_database.query_all(table.DatacampCourse, log=True) is None
