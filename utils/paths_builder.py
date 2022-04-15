from os.path import realpath, join, dirname, exists, abspath
from os import makedirs, getenv, environ
from platform import platform

WD = dirname(__file__)


def file_date():
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

def screenshots_dir():
    absolute_path = abspath(realpath(join(WD, '../../files/screenshots/')))
    if not exists(absolute_path):
        makedirs(absolute_path)
    return absolute_path

def test_logs_file_path():
    file_path = f'pims_test_run_{file_date()}.log'
    dir_path = abspath(realpath(join(WD, '../../files/reports/')))
    if not exists(dir_path):
        makedirs(dir_path)
    return realpath(realpath(join(dir_path, file_path)))

def screen_shot_path(filename):
    tst_date = getenv('TESTS_STARTED')
    if tst_date is None:
        dt = file_date()
        environ["TESTS_STARTED"] = dt
        tst_date = dt
    pth = join(screenshots_dir(), tst_date)
    if not exists(pth):
        makedirs(pth)
    return join(pth, f"{filename}.png")

def test_data_path(test_id):
    return join(abspath(realpath(join(WD, f'../../testdata/test_data_{test_id}.json'))))

def logo_path():
    return join(abspath(realpath(join(WD, f'../../testdata/logo.png'))))

def user_example_image_path(image):
    return join(abspath(realpath(join(WD, f'../../testdata/{image}'))))

def txt_file_path():
    return join(abspath(realpath(join(WD, f'../../testdata/textfile.txt'))))

def jpg_file_path():
    return join(abspath(realpath(join(WD, f'../../testdata/jpgfile.jpg'))))

def xls_raport_path(raport_name):
    return abspath(realpath(join(WD, f'../../files/downloads/{raport_name}.xlsx')))

def xlsx_report_file_path(report_name):
    return join(abspath(realpath(join(WD, f'../../testdata/xlsxdatafiles/{report_name}.xlsx'))))

def batch_data_path():
    return join(abspath(realpath(join(WD, f'../../testdata/chart_batches.xlsx'))))

def get_os():
    plat = platform().lower()
    if plat.startswith('darwin') or plat.startswith('macos'):
        return 'mac'
    elif plat.startswith('linux'):
        return 'linux'
    elif plat.startswith('win'):
        return 'win'

def downloads_dir():
    p = abspath(realpath(join(WD, '../../files/downloads/')))
    if not exists(p):
        makedirs(p)
    return p

def logs_path():
    dir_path = abspath(realpath(join(WD, '../../files/reports/')))
    return dir_path

def chromedriver_path():
    return realpath(join(drivers_dir(), 'chromedriver'))

def geckodriver_path():
    return realpath(join(drivers_dir(), 'geckodriver'))

def chromium_path():
    return join(chromedriver_path().replace('chromedriver', f'chrome-{get_os()}'))

def chromium_executable_path():
    os = get_os()
    if os == 'mac':
        return realpath(join(drivers_dir(), 'chrome-mac/Chromium.app/Contents/MacOS/Chromium'))
    elif os == 'linux':
        return realpath(join(drivers_dir(), 'chrome-linux/chrome'))

def firefox_executable_path():
    os = get_os()
    if os == 'mac':
        return realpath(join(drivers_dir(), 'Firefox.app/Contents/MacOS/firefox'))
    elif os == 'linux':
        return realpath(join(drivers_dir(), 'firefox/firefox'))

def gecko_path():
    return realpath(join(drivers_dir(), 'geckodriver'))

def gecko_zip_path(fname):
    return realpath(join(drivers_dir(), fname))

def firefox_dmg_path(version):
    return realpath(join(drivers_dir(), f'Firefox{version}.dmg'))

def firefox_tar_gz_path(version):
    return realpath(join(drivers_dir(), f'firefox-{version}.tar.bz2'))

def drivers_dir():
    pth = realpath(join(WD, '../../driver/'))
    if not exists(pth):
        makedirs(pth)
    return pth

from os import makedirs
from os.path import abspath, realpath, join, exists, dirname

WD = dirname(__file__)


def chromedriver_path():
    return realpath(join(WD, '../driver/chromedriver'))


def firefox_path():
    return realpath(join(WD, '../driver/geckodriver'))


def sub_tests_json_path():
    return realpath(join(WD, '../subtests.json'))


def schema_path(schema):
    return realpath(join(WD, '../schemas/{f}.json'.format(f=schema)))


def test_files_dir():
    absolute_path = abspath(realpath(join(WD, '../files/utils/')))
    if not exists(absolute_path):
        makedirs(absolute_path)
    return absolute_path


def test_emails_path():
    return join(test_files_dir(), f"mails-{file_date()}.csv")


def tmp_result_dir():
    absolute_path = abspath(realpath(join(WD, '../files/tmp/')))
    if not exists(absolute_path):
        makedirs(absolute_path)
    return absolute_path


def report_schema_path():
    absolute_path = abspath(realpath(join(WD, '../files/report/')))
    return join(absolute_path, "reportschema.html")


def tmp_result_file(filename):
    return join(tmp_result_dir(), f"{filename} {file_date()}.html")


def test_result_file_path():
    absolute_path = abspath(realpath(join(WD, '../files/report/')))
    if not exists(absolute_path):
        makedirs(absolute_path)
    return join(absolute_path, f"{file_date()}-report.html")


def file_date():
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


def downloads_dir():
    p = abspath(realpath(join(WD, '../files/downloads/')))
    if not exists(p):
        makedirs(p)
    return p


def downloaded_xlsx(filename):
    return join(downloads_dir(), f'{filename}.xlsx')


def downloaded_pdf(filename):
    return join(downloads_dir(), f'{filename}.pdf')


def config_path():
    return abspath(realpath(join(WD, '../pims_params.yaml')))

