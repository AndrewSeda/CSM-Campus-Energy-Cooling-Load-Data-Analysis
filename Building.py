from fileinput import close
import pandas as pd
import numpy

#File location: D:\Work\Research\Research Fall 2022\Modified\
FILE_PATH = "D:\Work\Research\Research Fall 2022\Modified\\"

df = pd.ExcelFile(FILE_PATH + "Building.xlsx", sheet_name = 2)