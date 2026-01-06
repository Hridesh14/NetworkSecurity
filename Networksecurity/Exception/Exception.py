import sys
from Networksecurity.logging import logger


class networkSecurity(Exception):
    def __init__(self,error_message,error_detail:sys):
        self.error_message = error_message
        _,_,exe_tb = error_detail.exc_info()

        self.line_no = exe_tb.tb_lineno
        self.file_name = exe_tb.tb_frame.f_code.co_filename
    
    def __str__(self):
        return 'Error occur in python script[{0}] in line Number [{1}] error mesage [{2}]'.format(
            self.line_no,self.file_name,str(self.error_message)
        )

if __name__=='__main__':
    logger.logging.info('we entered into the Try block')
    try:
        
        a=1/0
        print('this cant be printed',a)
    except Exception as e:
        raise networkSecurity(e,sys)

        