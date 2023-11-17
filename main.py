import os
import sys
import time
import shutil
import openpyxl
from datetime import datetime
from addData import addData,removerows
from filechecker import checkfile
from fileReader import extract_nameANDdate_from_file
from constants import EXCELFILENAME,LOGFILENAME,EXCELTEMPLATENAME


def create_xslx(document_path:str)->str:
  """Creates an Excel sheet named `EXCELFILENAME` in the "document" folder."""
  template_file = os.path.join(document_path,EXCELTEMPLATENAME)
  excel_file_path = os.path.join(document_path, EXCELFILENAME)
  if not os.path.exists(excel_file_path):
    # Destination file path (where you want to create a copy with a new name)
    shutil.copy(template_file, excel_file_path)
    
  return excel_file_path

def find_folder(project_path:str,directory:str)->str:
  """Finds the folder in the project path recursively."""
  for root, directories, files in os.walk(project_path):
    # print("root:",root,"directories:",directories,"files",files)
    if directory in directories:
      return os.path.join(root, directory)

  raise ValueError("The project path does not contain {} folder".format(directory))

def parse_files(folder_path:str,excel_file_path:str,inputs:tuple[str,str,str])->list:
        # Search for files  with in folder
  files=[f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
  files_in_folder=[]
  changes_detected=False
  for file in files:
    varcheckfile =checkfile(file)
    if varcheckfile is not None:
      file_type,levelofreview,filename=varcheckfile
      files_in_folder.append(filename)
      file_path= os.path.join(folder_path,file)
      result = extract_nameANDdate_from_file(file_path,inputs)
      if result is not None:
        recent_programmer,recent_date,reviewer = result
      changes_in_file=addData(excel_file_path,filename,file_type,levelofreview,recent_programmer,recent_date,reviewer)
      changes_detected=changes_detected|changes_in_file
  return files_in_folder,changes_detected


def main(project_path,reviewer_sdtmc_sdtme,programmer_sdtm_domain ,reviewer_sdtm_domain)->str:
  starttime=time.time()
 
  inputs=reviewer_sdtmc_sdtme,programmer_sdtm_domain ,reviewer_sdtm_domain
 
  try: 
    
    if not os.path.exists(project_path):
      raise ValueError("{} path does not exist.".format(project_path))
    else:
      document_path = find_folder(project_path,"document")
      macros_path=find_folder(project_path,"macros")
      xprt_path = find_folder(project_path,"xprt")
      acrf_path=os.path.join(document_path,"acrf")
      # excel_file_path = os.path.join(document_path, EXCELFILENAME)
      excel_file_path=create_xslx(document_path)
      if not os.path.exists(excel_file_path):
        raise ValueError("Create a copy of template Excel file and save as 'sdtm-programming-plan.xlsx'.\nThe {} does not contain {} file".format(document_path,EXCELFILENAME))
      workbook = openpyxl.load_workbook(excel_file_path)
      workbook.save(excel_file_path)
      with open(os.path.join(document_path,LOGFILENAME),'a')as file:
        today = datetime.today()
        formatted_datetime = today.strftime("%d-%b-%y %H:%M:%S")
        file.write(f"\n************************ LOG CREATED ON {formatted_datetime}*************************** \n")
        file.close()
      #finding  Custom Program and STDM HOTFIXES
      files_in_macros,changes1=parse_files(macros_path,excel_file_path,inputs) 
      # finding STDM domain and define.xml
      files_in_xprt,changes2=parse_files(xprt_path,excel_file_path,inputs) 
      #finding arcf file and adding to excel
      files_in_acrf,changes3=parse_files(acrf_path,excel_file_path,inputs)
      # parse_files(acrf_path,excel_file_path,inputs,FILETYPE4)
      
      #finding sdrg file and adding to excel
      files_in_document,changes4=(parse_files(document_path,excel_file_path,inputs))
      files_in_folders=files_in_macros+files_in_xprt+files_in_acrf+files_in_document
      changes5=removerows(excel_file_path,files_in_folders)
      changes_detected=changes1|changes2|changes3|changes4|changes5
      if changes_detected==False:
        with open(os.path.join(document_path,LOGFILENAME),'a')as file:
          file.write("*************************** NO CHANGES HAVE BEEN MADE ******************************* \n\n")
          file.close()
      
      with open(os.path.join(document_path,LOGFILENAME),'a')as file:
          file.write("**************************************END******************************************** \n\n")
          file.close()
      endtime=time.time()
      totaltime=endtime-starttime
      print("time",totaltime)  
      return (f"Excel saved sucessfully at {excel_file_path}")

          
  except Exception as e:
        if isinstance(e, PermissionError):
           return (f"Excel file is open! Save the excel and run again.\n{str(e)} ")
        else:
          return( f"{str(e)}")
  

if __name__ =="__main__":
   print(main(r'C:\Deep\novonordisk\nn1234-1234',"Deep","Nitish","Gautam"))






