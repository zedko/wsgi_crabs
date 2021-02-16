from mods.singleton import singleton_decorator
from datetime import datetime


@singleton_decorator
class Loggar:
    def __init__(self,
                 file: str = 'basic_log_file.log',
                 level: str = 'info'):
        """
        :param file - provide valid filename where to store the log
        """
        self._file = ''
        self.set_file(file)

        self._level = ''
        self.set_level(level)

        self.message_prefix = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: '

    def set_file(self, file_name: str):
        self._file = file_name

    def set_level(self, level: str):
        """
        :param level - could be 'info' or 'warning'
        """
        allowed_values = {'info', 'warning'}
        if level in allowed_values:
            self._level = level
        else:
            raise ValueError(f'Level should one of {allowed_values} values')

    def info(self, log_message: str):
        if self._level == 'info':
            with open(self._file, 'a') as f:
                f.write(f'{self.message_prefix}{log_message} \n')

    def info(self, log_message: str):
        if self._level in ['info', 'warning']:
            with open(self._file, 'a') as f:
                f.write(f'{self.message_prefix}{log_message} \n')
