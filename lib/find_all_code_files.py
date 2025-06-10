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

    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if not d.startswith((".", "_"))]

        for file in files:
            if file.endswith(".py") and not file.startswith(
                ("test_", "conftest", ".", "_", "main")
            ):
                code_files.append(os.path.join(root, file))

    return code_files
