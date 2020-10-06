import ftplib
from ftplib import FTP
import os


def ftp_connect_fnc(ip, port, user_id, pwd, process_type, down_path, file_name):
    # process_type : list_check(0), data_read(1)
    with FTP() as ftp:
        try:
            ftp.connect(ip, port)
            ftp.login(user_id, pwd)
            ftp.cwd('IOCounter/Report')
            report_list = ftp.nlst()

            if process_type == 0:
                return 0, report_list
            else:
                file_path = os.path.join(down_path, file_name)
                with open(file_path, 'wb') as local_file:
                    ftp.retrbinary('RETR %s' % file_name, local_file.write)
                return 0, 0
        except ftplib.all_errors as e:
            return e, 0

