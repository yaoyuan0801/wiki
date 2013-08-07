import logging
import os
def init(path ='/'.join(os.getcwd().split('/')[0 : -1])):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    self.log_file = '/'.join([log_dir, 'log'])
    logging.basicConfig(filename=log_file, level=logging.DEBUG)
    
def write(log_str, to_stdout = True):
    logging.debug(log_str)
    if to_stdout:
        print log_str

def clear():
    open(log_file, 'w').close()
