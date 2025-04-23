class ApiError:
    def __init__(self,error_msg,status_code,success,err=None):
        self.info = {"error_msg":error_msg,"status_code":status_code,"success":success,"err":err}
    
    def get_info(self):
        return self.info
