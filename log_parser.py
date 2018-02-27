import time
import re
import portage_env

emerge_log_dir = portage_env.EMERGE_LOG_DIR

def sec_to_time(seconds): # [days, hours, minutes, seconds]
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24) 
    return [d, h, m, s]

def parseLog(log_dir=emerge_log_dir, buff_size=8192):
    pass

def parseTime(log_line):
    return re.match('[0-9]*', log_line).group(0) 
