from lib.parse_raw_file.get_file_modules import get_module_name


def test_get_module_name_absolute():
    linux_abs_path = get_module_name("/Users/test/test_module.py", "/Users/test")
    assert linux_abs_path == "test_module"
    linux_abs_path = get_module_name("/Users/test/test_module.py", "/Users")
    assert linux_abs_path == "test.test_module"


def test_get_module_name_absolute_windows():
    windows_abs_path = get_module_name(
        "C:\\Users\\test\\test_module.py", "C:\\Users\\test"
    )
    assert windows_abs_path == "test_module"
    windows_abs_path = get_module_name("C:\\Users\\test\\test_module.py", "C:\\Users")
    assert windows_abs_path == "test.test_module"


def test_get_module_name_relative_linux():
    linux_rel_path = get_module_name("test_module.py", "/Users/test")
    assert linux_rel_path == "test_module"
    linux_rel_path = get_module_name("test/test_module.py", "/Users/test")
    assert linux_rel_path == "test.test_module"
    linux_rel_path_1 = get_module_name("./test/test_module.py", "/Users/test")
    assert linux_rel_path_1 == "test.test_module"


def test_get_module_name_relative_windows():
    windows_rel_path = get_module_name("test_module.py", "C:\\Users\\test")
    assert windows_rel_path == "test_module"
    windows_rel_path = get_module_name("test\\test_module.py", "C:\\Users\\test")
    assert windows_rel_path == "test.test_module"
    windows_rel_path_1 = get_module_name(".\\test\\test_module.py", "C:\\Users\\test")
    assert windows_rel_path_1 == "test.test_module"
