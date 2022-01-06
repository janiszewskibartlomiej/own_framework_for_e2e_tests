from utils.log import Logger


def step(name: str, use_args: bool = False, use_return: bool = False):
    def decorator(function):
        def wrapper(self, *args, **kwargs):
            extended_name = None
            number = len(self.driver.STEPS_LIST) + 1
            logger = Logger.get_logger()
            result = function(self, *args, **kwargs)
            if use_args:
                extended_name = name.format(*args)
            if use_return:
                extended_name = name.format(result)
            logger.info(f'Step # {number}: {extended_name or name}')
            self.STEPS_LIST.append(result)
            return result

        return wrapper

    return decorator
