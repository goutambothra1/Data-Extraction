import re
from constants import FILETYPE1,FILETYPE2,FILETYPE3,FILETYPE4, PATTERNDEFINEXML,PATTERN_SDTMC,PATTERN_SDTME,PATTERN_SDTMDOMAIN,PATTERN_SDRG,PATTERN_ACRF,LEVEL_OFREVIEW1,LEVEL_OFREVIEW2,LEVEL_OFREVIEW3
def checkfile(file_name:str)-> tuple[str,str,str]:
    try:   
        if re.match(PATTERN_SDTMC, file_name):
                return FILETYPE1,LEVEL_OFREVIEW1,file_name
        elif(re.match(PATTERN_SDTME,file_name)):
                return FILETYPE2,LEVEL_OFREVIEW2,file_name
        elif( re.match(PATTERN_SDTMDOMAIN,file_name) ):
                file_name=file_name.split(".")
                file_name=file_name[0].upper()
                return FILETYPE3 ,LEVEL_OFREVIEW2,file_name
        elif(any(re.match(pattern,file_name) for pattern in PATTERNDEFINEXML)):
                file_name1=file_name.capitalize()
                return FILETYPE4,LEVEL_OFREVIEW3,file_name1
        elif(re.match(PATTERN_ACRF,file_name) ):
                file_name= file_name[0].lower() + file_name[1:].upper()
                file_name=file_name.split(".")
                return FILETYPE4 ,LEVEL_OFREVIEW3,file_name[0]
        elif(re.match(PATTERN_SDRG,file_name) ):
                file_name=file_name.split(".")
                file_name=file_name[0].upper()
                return FILETYPE4 ,LEVEL_OFREVIEW3,file_name
    except Exception as e:
        print(f"Error: {str(e)}")

