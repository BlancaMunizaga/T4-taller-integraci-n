import requests
import pandas as pd
from xml.etree import ElementTree
import gspread
from gspread_dataframe import set_with_dataframe

# https://medium.com/@robertopreste/from-xml-to-pandas-dataframes-9292980b1c1c 
# def parse_XML(xml_file, df_cols):  
#     """Parse the input XML file and store the result in a pandas 
#     DataFrame with the given columns. 
    
#     The first element of df_cols is supposed to be the identifier 
#     variable, which is an attribute of each node element in the 
#     XML data; other features will be parsed from the text content 
#     of each sub-element. 
#     """
    
#     xtree = et.parse(xml_file)
#     xroot = xtree.getroot()
#     rows = []
    
#     for node in xroot: 
#         res = []
#         res.append(node.attrib.get(df_cols[0]))
#         for el in df_cols[1:]: 
#             if node is not None and node.find(el) is not None:
#                 res.append(node.find(el).text)
#             else: 
#                 res.append(None)
#         rows.append({df_cols[i]: res[i] 
#                      for i, _ in enumerate(df_cols)})
    
#     out_df = pd.DataFrame(rows, columns=df_cols)
        
#     return out_df


chile = 'CHL'
australia = 'AUS'
colombia = 'COL'
estados_unidos = 'USA'
canada = 'CAN'
costa_rica ='CRI'

indicadores = ['Number of deaths', 'Number of infant deaths', 'Number of under-five deaths',
'Mortality rate for 5-14 year-olds (probability of dying per 1000 children aged 5-14 years)','Adult mortality rate (probability of dying between 15 and 60 years per 1000 population)',
'Estimates of number of homicides','Crude suicide rates (per 100 000 population)','Mortality rate attributed to unintentional poisoning (per 100 000 population)',
'Number of deaths attributed to non-communicable diseases, by type of disease and sex', 'Estimated road traffic death rate (per 100 000 population)', 'Estimated number of road traffic deaths',
'Mean BMI (kg/m&#xb2;) (crude estimate)','Mean BMI (kg/m&#xb2;) (age-standardized estimate)',  'Prevalence of obesity among adults, BMI &GreaterEqual; 30 (age-standardized estimate) (%)', 
'Prevalence of obesity among children and adolescents, BMI > +2 standard deviations above the median (crude estimate) (%)', 'Prevalence of overweight among adults, BMI &GreaterEqual; 25 (age-standardized estimate) (%)',
'Prevalence of overweight among children and adolescents, BMI > +1 standard deviations above the median (crude estimate) (%)','Prevalence of underweight among adults, BMI < 18.5 (age-standardized estimate) (%)', 'Prevalence of thinness among children and adolescents, BMI < -2 standard deviations below the median (crude estimate) (%)',
'Alcohol, recorded per capita (15+) consumption (in litres of pure alcohol)', 'Estimate of daily cigarette smoking prevalence (%)', 'Estimate of daily tobacco smoking prevalence (%)', 'Estimate of current cigarette smoking prevalence (%)', 
'Estimate of current tobacco smoking prevalence (%)', 'Mean systolic blood pressure (crude estimate)','Mean fasting blood glucose (mmol/l) (crude estimate)', 'Mean Total Cholesterol (crude estimate)' ]

indicadores_muertes = ['Number of deaths', 'Number of infant deaths', 'Number of under-five deaths',
'Mortality rate for 5-14 year-olds (probability of dying per 1000 children aged 5-14 years)','Adult mortality rate (probability of dying between 15 and 60 years per 1000 population)',
'Estimates of number of homicides','Crude suicide rates (per 100 000 population)','Mortality rate attributed to unintentional poisoning (per 100 000 population)',
'Number of deaths attributed to non-communicable diseases, by type of disease and sex', 'Estimated road traffic death rate (per 100 000 population)', 'Estimated number of road traffic deaths']
indicadores_peso =['Mean BMI (kg/m&#xb2;) (crude estimate)','Mean BMI (kg/m&#xb2;) (age-standardized estimate)', 
'Prevalence of obesity among adults, BMI &GreaterEqual; 30 (age-standardized estimate) (%)', 
'Prevalence of obesity among children and adolescents, BMI > +2 standard deviations above the median (crude estimate) (%)',
'Prevalence of overweight among adults, BMI &GreaterEqual; 25 (age-standardized estimate) (%)',
'Prevalence of overweight among children and adolescents, BMI > +1 standard deviations above the median (crude estimate) (%)',
'Prevalence of underweight among adults, BMI < 18.5 (age-standardized estimate) (%)', 
'Prevalence of thinness among children and adolescents, BMI < -2 standard deviations below the median (crude estimate) (%)']
otros_indicadores = ['Alcohol, recorded per capita (15+) consumption (in litres of pure alcohol)', 'Estimate of daily cigarette smoking prevalence (%)', 'Estimate of daily tobacco smoking prevalence (%)', 'Estimate of current cigarette smoking prevalence (%)', 
'Estimate of current tobacco smoking prevalence (%)', 'Mean systolic blood pressure (crude estimate)','Mean fasting blood glucose (mmol/l) (crude estimate)', 'Mean Total Cholesterol (crude estimate)']

chile_info = requests.get('http://tarea-4.2021-1.tallerdeintegracion.cl/gho_CHL.xml')
australia_info = requests.get('http://tarea-4.2021-1.tallerdeintegracion.cl/gho_AUS.xml')
colombia_info = requests.get('http://tarea-4.2021-1.tallerdeintegracion.cl/gho_COL.xml')
estados_unidos_info = requests.get('http://tarea-4.2021-1.tallerdeintegracion.cl/gho_USA.xml')
canada_info = requests.get('http://tarea-4.2021-1.tallerdeintegracion.cl/gho_CAN.xml')
costa_rica_info = requests.get('http://tarea-4.2021-1.tallerdeintegracion.cl/gho_CRI.xml')

chile_excel_root = ElementTree.fromstring(chile_info.content)
australia_excel_root = ElementTree.fromstring(australia_info.content)
colombia_excel_root = ElementTree.fromstring(colombia_info.content)
estados_unidos_excel_root = ElementTree.fromstring(estados_unidos_info.content)
canada_excel_root = ElementTree.fromstring(canada_info.content)
costa_rica_root = ElementTree.fromstring(costa_rica_info.content)


def parse_XML(root, indicadores):
    Fact = root.findall('Fact')
    df_cols = ['GHO', 'COUNTRY', 'SEX', 'YEAR', 'GHECAUSES', 'AGEGROUP', 'Display', 'Numeric', 'Low', 'High']
    rows = []
    for node in Fact:
        res = []
        nombre = node.find(df_cols[0]).text
        if nombre in indicadores:
            res.append(nombre)
            for el in df_cols[1:]: 
                if node is not None and node.find(el) is not None:
                    res.append(node.find(el).text)
                else: 
                    res.append(None)
            rows.append({df_cols[i]: res[i] for i, _ in enumerate(df_cols)})
    out_df = pd.DataFrame(rows, columns=df_cols)
    return out_df

df_chile_muertes = parse_XML(chile_excel_root, indicadores_muertes)
df_australia_muertes = parse_XML(australia_excel_root, indicadores_muertes)
df_colombia_muertes = parse_XML(colombia_excel_root, indicadores_muertes)
df_estados_unidos_muertes = parse_XML(estados_unidos_excel_root, indicadores_muertes)
df_canada_muertes = parse_XML(canada_excel_root, indicadores_muertes)
df_costa_rica_muertes = parse_XML(costa_rica_root, indicadores_muertes)

df_muerte = pd.concat([df_chile_muertes, df_australia_muertes, df_colombia_muertes, df_estados_unidos_muertes, df_canada_muertes, df_costa_rica_muertes])

df_chile_peso = parse_XML(chile_excel_root, indicadores_peso)
df_australia_peso = parse_XML(australia_excel_root, indicadores_peso)
df_colombia_peso = parse_XML(colombia_excel_root, indicadores_peso)
df_estados_unidos_peso = parse_XML(estados_unidos_excel_root, indicadores_peso)
df_canada_peso = parse_XML(canada_excel_root, indicadores_peso)
df_costa_rica_peso = parse_XML(costa_rica_root, indicadores_peso)

df_peso = pd.concat([df_chile_peso, df_australia_peso, df_colombia_peso, df_estados_unidos_peso, df_canada_peso, df_costa_rica_peso])

df_chile_otros = parse_XML(chile_excel_root, otros_indicadores)
df_australia_otros = parse_XML(australia_excel_root, otros_indicadores)
df_colombia_otros = parse_XML(colombia_excel_root, otros_indicadores)
df_estados_unidos_otros = parse_XML(estados_unidos_excel_root, otros_indicadores)
df_canada_otros = parse_XML(canada_excel_root, otros_indicadores)
df_costa_rica_otros = parse_XML(costa_rica_root, otros_indicadores)

df_otros = pd.concat([df_chile_otros, df_australia_otros, df_colombia_otros, df_estados_unidos_otros, df_canada_otros, df_costa_rica_otros])




# # out_df.to_excel("algo.xlsx")
    
print("hola")



# ACCES GOOGLE SHEET
gc = gspread.service_account(
    filename='taller-tarea-4-315516-d690cdb3da75.json')
# 'your_google_sheet_ID'
sh = gc.open_by_key('1FPVgjpA8FentUjEFL-Lnq5gVcL15Eogv8tk7SQ5qhBI')
# sheet_index_no -> 0 first sheet, 1 second  sheet
worksheet = sh.get_worksheet(0)
worksheet2 = sh.get_worksheet(1)
worksheet3 = sh.get_worksheet(2)


# # APPEND DATA TO SHEET
# your_dataframe = pd.DataFrame()
# ->This exports your dataframe to the googleSheet
set_with_dataframe(worksheet, df_muerte)
set_with_dataframe(worksheet2, df_peso)
set_with_dataframe(worksheet3, df_otros)
