from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

from banker.banker import parse_result, format_query, FormatException


def test_format_query_expected_output():
    args = "first_name", "last_name"
    expected_result = 'SELECT first_name,last_name from Info'
    assert format_query(args).upper() == expected_result.upper()


def test_format_query_invalid_parameter():
    args = "middle_name", "last_name"
    try:
        format_query(args)
        assert False, "Expected exception to be raised!"
    except FormatException as e:
        assert e.reason == FormatException.invalid_paramters().reason
    except Exception as e:
        assert False, "Expected specific exception!"

def test_format_query_no_parameters():
    args = []
    try:
        format_query(args)
        assert False, "Expected exception to be raised!"
    except FormatException as e:
        assert e.reason == FormatException.no_parameters().reason
    except Exception as e:
        assert False, "Expected specific exception!"


def test_parse_result_expected_output_single_result():
    args = [('first','last','pass')]
    expected_output = [b'first,last,pass\n',]
    assert parse_result(args) == expected_output

def test_parse_result_expected_output_many_result():
    args = [('first','last','pass')] * 3
    expected_output = [b'first,last,pass\n',] * 3
    assert parse_result(args) == expected_output

def test_parse_result_expected_output_empty():
    args = []
    expected_output = []
    assert parse_result(args) == expected_output
