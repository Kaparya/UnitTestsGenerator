import os


def find_all_code_files(folder_path: str) -> list[str]:
    """
    Find all code files in the given folder path.
    Args:
        folder_path (str): А path to the folder to search for code files.
    Returns:
        list[str]: A list of paths to the code files found in the folder.
    """
    code_files = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                code_files.append(os.path.join(root, file))

    return code_files
