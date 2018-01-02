import time
emerge_log_dir = '/var/log/emerge.log'

def sec_to_time(seconds): # [days, hours, minutes, seconds]
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24) 
    return [d, h, m, s]

def parseLog(log_dir=emerge_log_dir,  buff_size=8192):
    pass
    
