from os import makedirs
from os.path import abspath, realpath, join, exists, dirname

WD = dirname(__file__)


# region OTHER PATHS
def data_folder_path() -> str:
    return abspath(realpath(join(WD, f"../resources/tests_data")))


def attachments_folder_path() -> str:
    return abspath(realpath(join(WD, f"../resources/tests_data/attachments")))


def reports_folder_path() -> str:
    return abspath(realpath(join(WD, f"../test_reports")))


def ddt_test_data_path(test_name) -> str:
    return abspath(realpath(join(WD, f"tests_data/test_data_{test_name}.json")))


def downloads_dir() -> str:
    path = abspath(realpath(join(WD, "files/downloads/")))
    if not exists(path):
        makedirs(path)
    return path


def logs_file_path():
    file_path = f"tests_log_{file_date()}.log"
    dir_path = abspath(realpath(join(WD, "../test_reports/logs/")))
    if not exists(dir_path):
        makedirs(dir_path)
    return realpath(realpath(join(dir_path, file_path)))


def file_date():
    from datetime import datetime

    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
