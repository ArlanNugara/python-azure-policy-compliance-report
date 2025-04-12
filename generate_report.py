import csv
import sys
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import load_workbook
from modules.generate_excel import create_excel

csv_file_map = ('reports',)

try:
  print("Creating Excel Report")
  
  for files in csv_file_map:
    print("Creating Excel Sheet for ", files)
    create_excel(""+files+".csv",files)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)