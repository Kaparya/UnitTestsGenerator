import os


def save_file(original_file_path: str, content: str) -> str:
    """
    Save the generated content to a file.
    Args:
        original_file_path (str): The path to the original file.
        content (str): The content to save.
    Returns:
        str: The path to the saved test file.
    """

    split_path = original_file_path.split('/')

    tests_folder = split_path[:-1]
    tests_folder.append('tests')
    tests_folder = '/'.join(tests_folder) + '/'

    if not os.path.isdir(tests_folder):
        os.makedirs(tests_folder)

    test_file_path = 'test_' + '.'.join(split_path[-1].split('.')[:-1]) + '.py'
    test_file_path = tests_folder + test_file_path

    with open(test_file_path, 'w') as test_file:
        test_file.write(content)
    return test_file_path
