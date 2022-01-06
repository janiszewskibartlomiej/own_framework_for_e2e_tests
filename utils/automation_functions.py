import json
import os
import re
import shutil
import smtplib
import sys
import time
from datetime import date, datetime, timedelta
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, formataddr
from json import load, loads, dumps
from os.path import exists, dirname
from pathlib import Path

import easyimap
from dotenv import load_dotenv
from jsonref import JsonRef
from selenium import webdriver
from sty import fg

import utils.constants as constant
from utils.paths_builder import (
    ddt_test_data_path,
    data_folder_path,
)

load_dotenv()


# template of date example >> 20200715
def current_date_str_from_number(sub_day=0) -> str:
    current_date = date.today()
    date_solution = current_date + timedelta(days=sub_day)
    current_date_template = date_solution.strftime("%Y%m%d")
    return current_date_template


def removing_directories_in_reports_by_number_of_day(
        n_day: int = int(os.getenv(key="REMOVING_REPORTS_BY_DAYS", default="7"))
) -> str:
    list_remove_directory = []
    current_date_sub_days = int(current_date_str_from_number(sub_day=-n_day))

    reports_path = get_path_from_directory_name(directory_name=constant.TEST_REPORTS)
    entries = Path(reports_path)

    for entry in entries.iterdir():
        try:
            if int(entry.name) <= current_date_sub_days:
                shutil.rmtree(f"{reports_path}/{entry.name}")
                list_remove_directory.append(entry.name)
        except ValueError:
            continue
    message = (
        f"\n>> Removed directories: {list_remove_directory} <<\n"
        if list_remove_directory
        else ">> Nothing to remove in test reports directory<<\n"
    )
    return message


def run_pytest_html_and_allure_report(by_name) -> list:
    allure_json_path = change_win_sep(
        path=get_path_from_directory_name(directory_name=constant.ALLURE_JSON)
    )

    allure_html_reports_path = change_win_sep(
        path=get_path_from_directory_name(directory_name=constant.ALLURE_HTML_REPORTS)
    )

    reports_path = change_win_sep(
        path=get_path_from_directory_name(directory_name=constant.TEST_REPORTS)
    )

    if not allure_json_path:
        allure_json_path = make_directory(
            location_by_directory_name=constant.TEST_REPORTS,
            creating_of_directory_name=constant.ALLURE_JSON,
        )

    if not allure_html_reports_path:
        allure_html_reports_path = make_directory(
            location_by_directory_name=constant.TEST_REPORTS,
            creating_of_directory_name=constant.ALLURE_HTML_REPORTS,
        )

    current_date = current_date_str_from_number()

    pytest_html_report_path = change_win_sep(
        path=f"{reports_path}{os.sep}{current_date}{os.sep}pytest_AiBuster_report_{int(time.time())}.html"
    )

    flag_and_name = f"-m {by_name}" if by_name else ""

    os.system(
        f"pytest {flag_and_name} -vv --html={pytest_html_report_path} --self-contained-html --alluredir {allure_json_path}"
    )

    os.chdir(allure_html_reports_path)
    os.system(f"allure generate {allure_json_path} --clean")
    allure_index_path = change_win_sep(path=f"{allure_html_reports_path}{os.sep}allure-report")

    allure_zip = shutil.make_archive(
        base_name=allure_index_path, format="zip", root_dir=allure_html_reports_path
    )

    print(allure_zip.title(), " is DONE !")
    allure_zip_path = change_win_sep(path=get_path_from_file_name(file_name="allure-report.zip"))
    return [pytest_html_report_path, allure_zip_path]


def get_path_from_file_name(file_name: str) -> str:
    path_list = [el for el in sys.path if "JetBrains" not in el]
    path = path_list[1]
    if Path(path).suffix == ".zip":
        path = path_list[0]
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == file_name:
                abs_path = os.path.join(root, file)
                return abs_path


def get_path_from_directory_name(directory_name: str) -> str:
    path_list = [el for el in sys.path if "JetBrains" not in el]
    path = path_list[1]
    if Path(path).suffix == ".zip":
        path = path_list[0]
    for root, dirs, files in os.walk(path):
        for dictionary in dirs:
            if dictionary == directory_name:
                abs_path = os.path.join(root, dictionary)
                return abs_path


def load_from_json_file(path: str) -> dict:
    with open(file=path, mode="r", encoding="UTF-8") as json_file:
        return load(json_file)


def data_loader(test_name: str) -> dict:
    return load_from_json_file(ddt_test_data_path(test_name))


def data_generator(test_name: str) -> dict:
    json_data = data_loader(test_name=test_name)
    joined_data = loads(
        dumps(
            JsonRef.replace_refs(json_data, base_uri=f"file://{data_folder_path()}/"),
            default=ref_caster,
        )
    )
    options = []
    names = []
    for item in joined_data:
        options.append(joined_data[item]["data"])
        names.append(item)

    data = {}
    for index, element in enumerate(options):
        for k, v in element.items():
            try:
                exec(v)
                options[index][k] = data[k]
            except Exception:
                pass
    return {"names": names, "data": options}


def ref_caster(o) -> (None, dict, str, list, float, int, bool):
    if isinstance(o, JsonRef):
        if isinstance(o, type(None)):
            return None
        else:
            for json_type in [dict, str, list, float, int, bool]:
                if isinstance(o, json_type):
                    return json_type(o)


def get_screenshot(name: str, driver: webdriver, dictionary_path: str) -> None:
    original_size = driver.get_window_size()
    required_width = driver.execute_script("return document.body.parentNode.scrollWidth")
    required_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    driver.set_window_size(required_width, required_height)

    if not os.path.exists(dictionary_path):
        os.makedirs(dictionary_path)

    t = time.localtime()
    current_time = time.strftime("%H-%M-%S", t)
    path = f"{dictionary_path}{os.sep}screenshot_{name}_{current_time}.png"
    time.sleep(1)
    driver.get_screenshot_as_file(path)
    time.sleep(1)
    driver.set_window_size(original_size["width"], original_size["height"])


def get_date_from_delta_n_day(add_days: int) -> dict:
    today = datetime.today()
    future_date = today + timedelta(days=add_days)
    date_dict = {
        "day": future_date.day,
        "month": future_date.month,
        "year": future_date.year,
    }
    return date_dict


def get_list_of_path_to_attachment(attachment_names: list, list_of_path_to_files=None) -> list:
    if constant.COLON in attachment_names[0]:
        list_of_path_to_files = attachment_names

    if list_of_path_to_files is None:
        list_of_path_to_files = []

        if attachment_names.__len__() > 1:
            for name in attachment_names:
                attachment_path = get_path_from_file_name(name)
                list_of_path_to_files.append(attachment_path)

        elif attachment_names.__len__() == 1:
            attachment_path = get_path_from_file_name(file_name=attachment_names[0])
            list_of_path_to_files.append(attachment_path)

    return list_of_path_to_files


def print_message_in_color(message: str, rgb_color: str) -> None:
    list_of_volume = rgb_color.split(",")
    response = (
            fg(list_of_volume[0], list_of_volume[1], list_of_volume[2])
            + "\n\n"
            + message
            + "\n"
            + fg.rs
    )
    print(response)


def send_email(
        send_to=None,
        send_copy=None,
        subject=None,
        message_content=None,
        files_path=None,
        number_sent_email=None,
) -> dict:
    timestamp = int(time.time() * 1000)
    send_to = send_to or os.environ.get("SEND_TO")

    if not subject:
        subject = " "
    elif subject == constant.REPORTS_OF_TESTS:
        subject = f"{subject}"
    else:
        subject = f"{subject} #{timestamp}#"

    message_content = message_content or constant.MESSAGE

    files_path = files_path or []

    sender_email = os.environ.get("SENDER_EMAIL")
    sender_name = os.environ.get("SENDER_NAME")
    smtp_server = os.environ.get("SMTP_SERVER")
    port = os.environ.get("PORT")
    password = os.environ.get("EMAIL_PASSWORD")

    message = MIMEMultipart()
    message["From"] = formataddr((str(Header(sender_name, "utf-8")), sender_email))
    message["Name"] = sender_name
    message["To"] = send_to
    message["Subject"] = subject
    message["Date"] = formatdate(localtime=True)
    message["Cc"] = send_copy or ""
    message.attach(MIMEText(message_content))

    if files_path:
        set_attachments(
            files_path=get_list_of_path_to_attachment(attachment_names=files_path), message=message
        )

    with smtplib.SMTP_SSL(host=smtp_server, port=port, timeout=30, ) as server:
        server.ehlo()
        server.login(user=sender_email, password=password)
        server.send_message(message)
        number_sent_email = number_sent_email or ""
        number_sent_email_message = f", number sent email = {number_sent_email}"

    print_message_in_color(
        message=f"Send successful email, subject = {subject}{number_sent_email_message if number_sent_email else ''}",
        rgb_color="255,10,10",
    )
    return {"subject": subject, "timestamp": timestamp}


def make_directory(location_by_directory_name: str, creating_of_directory_name: str) -> str:
    location_path = get_path_from_directory_name(directory_name=location_by_directory_name)
    os.makedirs(location_path + os.sep + creating_of_directory_name)
    dictionary_path = get_path_from_directory_name(directory_name=creating_of_directory_name)
    return dictionary_path


def change_win_sep(path: str) -> str:
    if isinstance(path, str):
        return path.replace("\\", "/")


def set_attachments(files_path: list, message: MIMEMultipart) -> None:
    for path in files_path:
        with open(file=path, mode="rb") as file:
            base_name = os.path.basename(path)
            exe = path.split(".")[-1]
            instance = MIMEApplication(_data=file.read(), _subtype=exe, name=base_name)
        instance.add_header(
            _name="Content-Disposition", _value="attachment", filename=base_name,
        )
        message.attach(instance)


def wait(n_seconds=0.5):
    time.sleep(n_seconds)


def get_email_objects(host, user, password, port, mailbox="INBOX", ssl=False, limit=10) -> list:
    imap = easyimap.connect(
        host=host, user=user, password=password, mailbox=mailbox, ssl=ssl, port=port, timeout=30
    )
    list_of_email_objects = imap.listup(limit=limit)
    imap.quit()
    return list_of_email_objects


def save_to_json(data, path) -> None:
    if not exists(dirname(path)):
        os.makedirs(dirname(path))
    with open(file=path, mode="w", encoding="UTF-8") as file:
        json.dump(data, file, indent=4)


def get_path_to_file_in_test_reports_by_current_date(name: str) -> str:
    current_date_template = str(date.today()).replace("-", "")
    test_reports_path = get_path_from_directory_name(directory_name=constant.TEST_REPORTS)
    dir_target = f"{test_reports_path}{os.sep}{current_date_template}"
    file_target = f"{dir_target}{os.sep}{name}"
    if not os.path.exists(dir_target):
        os.makedirs(file_target, mode=0o777)
    return file_target


def check_status_code_in_dict(logs: dict) -> None:
    conditions = [x.__str__() + " " for x in range(400, 600)]
    string_data = " ".join([el.__str__() for el in logs.items()])
    json_dumps = json.dumps(logs, indent=4)
    if any(item in re.findall(pattern="[45]\d\d\s", string=string_data) for item in conditions):
        file_target = get_path_to_file_in_test_reports_by_current_date(
            name=f"console_logs_{int(time.time() * 1000)}.json"
        )
        save_to_json(data=logs, path=file_target)
        raise AssertionError(
            f"\n>>> Error status code in console browser: <<<\n\n{json_dumps}\nPath to json file: {file_target}"
        )
    else:
        print("Console logs:\n", json_dumps)
