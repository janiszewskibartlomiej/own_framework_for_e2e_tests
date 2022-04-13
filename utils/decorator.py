from os import getenv
from selenium.common.exceptions import UnexpectedAlertPresentException
from time import time

from reporting.reporting_tool import log_ss_path
from testrunner.log import loggable_step, Logger


def step(name, expected='', srs='N/A', screenshot=True, can_fail=False, no=None):
    if screenshot:
        screenshot = ('TRUE' in getenv('SCREENSHOTS', 'FALSE'))

    def decorator(function):
        def wrapper(self, *args, **kwargs):
            number = len(self.STEPS_LIST) + 1
            logger = Logger.get_logger()
            extended_name = f'{name} {kwargs.get("name_info", "")}'
            extended_expected = f'{expected} {kwargs.get("expected_info", "")}'
            result = {'description': f'{extended_name}', 'actual': '', 'message': '',
                      'expected': f'{extended_expected}', 'srs': srs, 'screenshot': ''}
            if screenshot:
                stamp = time()
                ss = log_ss_path(stamp)
            logger.info(f'Step # {number}: {extended_name}')
            try:
                function(self, *args, **kwargs)
                if screenshot:
                    try:
                        self.parent.CURRENT_PAGE.wait_for_loader()
                        self.DRIVER.save_screenshot(filename=ss)
                    except UnexpectedAlertPresentException:
                        pass
                    except AttributeError:
                        pass
                    result['screenshot'] = f'{ss}'
                result['actual'] = 'passed'
                self.STEPS_LIST.append(result)
            except Exception as e:
                if screenshot:
                    try:
                        self.parent.CURRENT_PAGE.wait_for_loader()
                        self.DRIVER.save_screenshot(filename=ss)
                    except UnexpectedAlertPresentException:
                        pass
                    except AttributeError:
                        pass
                    result['screenshot'] = f'{ss}'
                result['actual'] = 'failed'
                result['message'] = str(e)
                if not can_fail:
                    if e.__class__.__name__ == "WebDriverException":
                        if 'chrome' in self.DRIVER.name:
                            logger = Logger.get_logger()
                            browser_logs = self.DRIVER.get_log('driver')
                            for a in browser_logs:
                                logger.info(f'Browser logs: {a}')
                    self.STEPS_LIST.append(result)
                    raise e
            return result

        return wrapper

    return decorator
