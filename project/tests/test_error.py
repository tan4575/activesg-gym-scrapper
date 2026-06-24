from error.error import DatabaseError, ErrorCode, ScrapingError


def test_database_error_includes_error_code():
    error = DatabaseError("Not Found!", ErrorCode.NOT_FOUND.value)

    assert str(error) == "Not Found! Error Code: 404"


def test_scraping_error_includes_error_code():
    error = ScrapingError("Driver Error!", ErrorCode.DRIVER_ERROR.value)

    assert str(error) == "Driver Error! Error Code: 100"
