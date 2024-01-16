import os
import json

import pytest

from project.gql.parser import check


def load_tests():
    current_dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_dir_path, "../resources/test_parser.json")
    with open(file_path) as json_data:
        data = json.load(json_data)
    return data["test_check"]


@pytest.mark.parametrize(
    "input_, is_ok", map(lambda r: (r["input"], r["is_ok"]), load_tests())
)
def test_check(input_: str, is_ok: bool):
    assert check(input_) == is_ok
