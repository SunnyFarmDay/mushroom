import pandas as pd
import os
import sqlalchemy
engine = sqlalchemy.create_engine('mysql+pymysql://mushroomsqluser:mushroomSQL@localhost:3306/mushroom')
conn = engine.connect()



excel = pd.ExcelFile('/home/sunny/mushroom/ExcelToSql/salary.xlsx')
for cursheet in excel.sheet_names:
    cursheet = str(cursheet)
    atr = cursheet.split('_')
    if atr[0] == "salary" and len(atr) == 2:
        print(f"-- current sheet is {cursheet}\n")
        df = excel.parse(cursheet, )
        df = df.set_axis(["SID", "staff_name", "salary", "status"], axis='columns')
        df.insert(2, "description", '')
        print(df)
        df.to_sql(cursheet, engine,if_exists="replace", index=False)
