from unittest.mock import patch

import pytest
from datetime import date
from most_active_cookie import (
    find_most_active_cookies,
    parse_cookie_log,
    validate_date,
    validate_file
)

import os
import tempfile
import argparse
import subprocess


@pytest.fixture
def sample_log_file():
    content = (
        "cookie,timestamp\n"
        "AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00\n"
        "SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00\n"
        "5UAVanZf6UtGyKVS,2018-12-09T07:25:00+00:00\n"
        "AtY0laUfhglK3lC7,2018-12-09T06:19:00+00:00\n"
        "SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00\n"
        "4sMM2LxV07bPJzwf,2018-12-08T21:30:00+00:00\n"
        "fbcn5UAVanZf6UtG,2018-12-08T09:30:00+00:00\n"
    )
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'w') as tmp:
        tmp.write(content)
    yield path
    os.remove(path)


def test_parse_cookie_log_filters_correct_date(sample_log_file):
    cookies = parse_cookie_log(sample_log_file, date(2018, 12, 9))
    assert 'AtY0laUfhglK3lC7' in cookies
    assert 'SAZuXPGUrfbcn5UA' in cookies
    assert '5UAVanZf6UtGyKVS' in cookies
    assert len(cookies) == 4  # 3 unique cookies, one appears twice


def test_find_not_most_active_cookies_single_max():
    cookies = ['AtY0laUfhglK3lC7', 'AtY0laUfhglK3lC7', 'AtY0laU45hglK3lC7', 'AtY0laU45hglK3l79']
    result = find_most_active_cookies(cookies)
    assert result != ['AtY0laU45hglK3lC7']


def test_find_most_active_cookies_single_max():
    cookies = ['AtY0laUfhglK3lC7', 'AtY0laUfhglK3lC7', 'AtY0laU45hglK3lC7', 'AtY0laU45hglK3l79']
    result = find_most_active_cookies(cookies)
    assert result == ['AtY0laUfhglK3lC7']


def test_find_most_active_cookies_multiple_max():
    cookies = ['AtY0laUfhglK3lC7', 'AtY0laU45hglK3l79', 'AtY0laUfhglK3lC7', 'AtY0laU45hglK3l79']
    result = find_most_active_cookies(cookies)
    assert sorted(result) == ['AtY0laU45hglK3l79', 'AtY0laUfhglK3lC7']


def test_find_most_active_cookies_empty():
    assert find_most_active_cookies([]) == []


def test_parse_cookie_log_handles_malformed_lines():
    bad_content = (
        "cookie,timestamp\n"
        "cookie1,2018-12-09T10:00:00+00:00\n"
        "malformed_line_without_comma\n"
        "cookie2,INVALID_TIMESTAMP\n"
        "cookie3,2018-12-09T20:00:00+00:00\n"
    )
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'w') as tmp:
        tmp.write(bad_content)
    cookies = parse_cookie_log(path, date(2018, 12, 9))
    os.remove(path)
    assert cookies == ['cookie1', 'cookie3']


def test_parse_cookie_log_logs_error_file(caplog):
    with patch("builtins.open", side_effect=IOError("Mocked file read error")):
        with caplog.at_level("ERROR"):
            with pytest.raises(IOError):
                parse_cookie_log("mocked_file.csv", date(2023, 1, 1))

    # Check log message
    assert any("Error reading file mocked_file.csv" in message for message in caplog.text.splitlines())



def test_validate_date_success():
    assert validate_date("2023-12-01") == date(2023, 12, 1)


def test_validate_date_failure():
    with pytest.raises(argparse.ArgumentTypeError):
        validate_date("2023/12/01")  # Incorrect format


def test_validate_file_success():
    fd, path = tempfile.mkstemp()
    os.close(fd)
    assert validate_file(path) == path
    os.remove(path)


def test_validate_file_not_exist():
    with pytest.raises(argparse.ArgumentTypeError):
        validate_file("non_existing.csv")


def test_validate_file_not_readable():
    fd, path = tempfile.mkstemp()
    os.chmod(path, 0o000)  # remove read permissions

    try:
        with pytest.raises(argparse.ArgumentTypeError):
            validate_file(path)
    finally:
        os.chmod(path, 0o644)  # reset permission so it can be deleted
        os.remove(path)


def test_cli_success(sample_log_file):
    result = subprocess.run(
        ['python3', 'most_active_cookie.py', '-f', sample_log_file, '-d', '2018-12-09'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'AtY0laUfhglK3lC7' in result.stdout


def test_cli_no_match(sample_log_file):
    result = subprocess.run(
        ['python3', 'most_active_cookie.py', '-f', sample_log_file, '-d', '2025-01-01'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert result.stdout.strip() == ''
