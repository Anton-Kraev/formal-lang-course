import filecmp
import os

from project.gql.parser import write_to_dot


def test_write_dot():
    current_dir_path = os.path.dirname(os.path.realpath(__file__))
    expected_path = os.path.join(current_dir_path, "../resources/expected_tree.dot")
    actual_path = os.path.join(current_dir_path, "../resources/actual_tree.dot")

    text = 'set a = "A" || "a"\nset b = ("b" || a)*\nprint a .. b\n'
    write_to_dot(text, actual_path)

    assert filecmp.cmp(actual_path, expected_path, shallow=False)
    os.remove(actual_path)
