import os
import re


def create_path_testfile(original_file_path: str) -> str:
    """
    Generate path of file with tests  
    Args:
        original_file_path (str): The path to the original file.
    Returns:
        str: The path of test file.
    """

    split_path = re.split(r"[\\/]+", original_file_path)

    tests_folder = split_path[:-1]
    tests_folder.append("tests")
    tests_folder = "/".join(tests_folder) + "/"

    if not os.path.isdir(tests_folder):
        os.makedirs(tests_folder)

    test_file_path = "test_" + ".".join(split_path[-1].split(".")[:-1]) + ".py"
    test_file_path = tests_folder + test_file_path

    return test_file_path


def save_file(original_file_path: str, content: str):
    """
    Save the generated content to a file.
    Args:
        original_file_path (str): The path to the original file.
        content (str): The content to save.
    Returns:
        str: The path to the saved test file.
    """

    test_file_path = create_path_testfile(original_file_path)

    with open(test_file_path, "w") as test_file:
        test_file.write(content)
    return test_file_path


def create_conftest(project_directory: str) -> None:
    """
    Create a conftest.py file in the tests folder.
    Args:
        project_directory (str): The path to the project directory root.
    """
    conftest_path = os.path.join(project_directory, "conftest.py")
    if not os.path.isfile(conftest_path):
        with open(conftest_path, "w") as conftest_file:
            conftest_file.write("")
