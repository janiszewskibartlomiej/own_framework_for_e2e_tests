from datetime import datetime
from os import makedirs, environ, getenv, remove
from os.path import dirname, join, realpath, abspath, exists
from json import load
import jinja2
from weasyprint import HTML, CSS


WD = dirname(__file__)
TMP_HTML = join(WD, 'tmp.html')
templateLoader = jinja2.FileSystemLoader(searchpath=abspath(WD))
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "report_layout.html"


def generate_report_for_single_test_case(test_case_id, test_steps):
    html = generate_base_html_report(test_case_id, test_steps)
    with open(TMP_HTML, 'w') as html_f:
        html_f.write(html)
    css = get_css()
    HTML(TMP_HTML).write_pdf(stylesheets=[css], target=pdf_report_path(test_case_id))
    remove(TMP_HTML)


def generate_base_html_report(test_case_id, test_steps):
    template = templateEnv.get_template(TEMPLATE_FILE)
    with open(metadata_file(test_case_id)) as json_file:
        metadata = load(json_file)
    test_data = metadata['data']
    test_data['steps'] = test_steps
    testdate = datetime.now().strftime('%Y %B %d %H:%M:%S')
    return template.render(test=test_data, testdate=testdate)


def get_css():
    with open(stylesheet(), 'r') as f:
        return CSS(string=f.read())


def metadata_file(test_case_id):
    return realpath(join(WD, 'tests_metadata/', f'{test_case_id}.json'))


def stylesheet():
    return realpath(join(WD, 'style.css'))


def reports_dir():
    absolute_path = abspath(realpath(join(WD, '../files/reports/')))
    if not exists(absolute_path):
        makedirs(absolute_path)
    return absolute_path


def log_screenshots_dir():
    tst_date = getenv('TESTS_STARTED')
    if tst_date is None:
        dt = file_date()
        environ["TESTS_STARTED"] = dt
        tst_date = dt
    ss_dir = abspath(realpath(join(reports_dir(), tst_date, 'screenshots')))
    if not exists(ss_dir):
        makedirs(ss_dir)
    return ss_dir


def log_ss_path(stamp):
    ss = join(log_screenshots_dir(), f'{stamp}.png')
    return ss

def single_report_path():
    tst_date = getenv('TESTS_STARTED')
    if tst_date is None:
        dt = file_date()
        environ["TESTS_STARTED"] = dt
        tst_date = dt
    pth = join(reports_dir(), tst_date)
    if not exists(pth):
        makedirs(pth)
    return pth

def report_download_dir():
    pth = join(single_report_path(), 'downloads')
    if not exists(pth):
        makedirs(pth)
    return pth

def move_report_download_dir():
    pth = join(single_report_path(), f'{environ["TEST_ID"]}_Attachments')
    if not exists(pth):
        makedirs(pth)
    return pth

def pdf_report_path(test_case_id):
    rp = join(single_report_path(), f"{test_case_id}.pdf")
    if exists(rp):
        rp = join(single_report_path(), f"{test_case_id}_2.pdf")
    return rp


def html_report_path(test_case_id):
    tst_date = getenv('TESTS_STARTED')
    if tst_date is None:
        dt = file_date()
        environ["TESTS_STARTED"] = dt
        tst_date = dt
    pth = join(reports_dir(), tst_date)
    if not exists(pth):
        makedirs(pth)
    return join(pth, f"{test_case_id}.html")


def file_date():
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
