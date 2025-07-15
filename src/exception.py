import sys
from src.logger import logging


def error_message_details(error, error_detials: sys):
    _, _, exc_tb = error_detials.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = f"Error found in {file_name} file, with line number {line_number}, with error : {str(error)}"
    return error_message

class CustomException(Exception):
    def __init__(self, error, error_details: sys):
        super().__init__(str(error))
        self.error_message = error_message_details(error, error_details)
        logging.error(self.error_message)

    def __str__(self):
        return self.error_message