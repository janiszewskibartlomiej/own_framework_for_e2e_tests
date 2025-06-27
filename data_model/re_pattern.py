import re

class RePatterns:
    NUMBER_PATTERN = re.compile(r'\d+')
    PATH_D_VALUE_PATTERN = re.compile(r'd="([^"]{3})')
