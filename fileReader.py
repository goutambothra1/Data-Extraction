import re
import os
from datetime import datetime


def extract_nameANDdate_from_file(file_path:str,inputs:tuple[str,str,str])->tuple[str,datetime,str]:
    reviewerOfsdtmc_stdme,programmerOfotherfiles,reviewerOfotherfiles=inputs
    changelogs=[]
    # print("file_path",file_path)
    if file_path.endswith(".sas"):
            with open(file_path, 'r') as file:
                for line_no,line in enumerate(file,1):
                    lineparser=re.search(r' *Programmer *: *[A-Za-z1-9]+',line)
                    if lineparser is not None: 
                        programmer=lineparser.group()
                    changelog=re.search(r' *Change Log *: *[A-Za-z1-9]+ *(\d{4}\.\d{1,2}\.\d{1,2})*', line)
                    if changelog is not None:
                        #  print(changelog.group())
                         changelogs.append(changelog.group())
                    if changelogs is None:
                        pass
                        # return programmer
                latest_date = None
                latest_date_index = None
                
                for index, log in enumerate(changelogs):
                    parts = log.split()
                    if len(parts) >= 3 :
                        date_str = parts[-1]
                        try:
                            log_date = datetime.strptime(date_str, '%Y.%m.%d')
                            if latest_date is None or log_date > latest_date:
                                latest_date = log_date
                                latest_date_index = index
                        except ValueError:
                            pass    
                if latest_date is not None:
                    # print("Latest Date:", latest_date.strftime('%Y.%m.%d'))
                    # print("Index:", latest_date_index)
                    recentprogrammer=changelogs[latest_date_index].split()[3]
                    reviewer=reviewerOfsdtmc_stdme
                    return recentprogrammer, latest_date.strftime("%d-%b-%y"),reviewer
    else:
            created_date=os.path.getctime(file_path)
            created_date = datetime.fromtimestamp(created_date).strftime("%d-%b-%y")
            recentprogrammer=programmerOfotherfiles
            reviewer=reviewerOfotherfiles
            return recentprogrammer,created_date,reviewer
    
         
       