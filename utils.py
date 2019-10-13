import math

import coloredlogs


def get_colored_value(value, suffix=''):
    value_str = f'{+value:.02f}{suffix}'
    if 0 < abs(value) < 1:
        value_str = f'{+value:.04f}{suffix}'

    if value > 0:
        return coloredlogs.ansi_wrap(value_str, color='green')
    elif value < 0:
        return coloredlogs.ansi_wrap(value_str, color='red')
    return value_str
