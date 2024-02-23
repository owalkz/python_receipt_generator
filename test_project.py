import pytest
from project import file_access
from project import check_exists
from project import fill_pdf


def test_file_access():
    with pytest.raises(SystemExit):
        file_access("random.csv")


def test_check_exists():
    with pytest.raises(SystemExit):
        check_exists("random.pdf")


def test_fill_pdf():
    assert fill_pdf(file_access("dawa.csv"), "13-10-2023") == None
