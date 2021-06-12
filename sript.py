import requests
import pandas as pd
from xml.etree import ElementTree
import gspread
from gspread_dataframe import set_with_dataframe


chile = 'CHL'
australia = 'AUS'
colombia = 'COL'
estados_unidos = 'USA'
canada = 'CAN'
costa_rica ='CRI'

chile_info = requests.get('http://tarea-4.2021-1.tallerdeintegracion.cl/gho_CHL.xml')

chile_excel_root = ElementTree.fromstring(chile_info.content)

aspectos = chile_excel_root.findall('Fact/GHO/Alcohol')

for country in aspectos:
    print(country.text)
# print(aspectos)
# chile_excel_root.iter('*'):
# for child in chile_excel_root.iter(''):
#     print(child.getchildren().atrri)
# print("hola")
# # ACCES GOOGLE SHEET
# gc = gspread.service_account(
#     filename='taller-tarea-4-315516-d690cdb3da75.json')
# # 'your_google_sheet_ID'
# sh = gc.open_by_key('1FPVgjpA8FentUjEFL-Lnq5gVcL15Eogv8tk7SQ5qhBI')
# # sheet_index_no -> 0 first sheet, 1 second  sheet
# worksheet = sh.get_worksheet(0)

# # APPEND DATA TO SHEET
# your_dataframe = pd.DataFrame()
# # ->This exports your dataframe to the googleSheet
# set_with_dataframe(worksheet, your_dataframe)
