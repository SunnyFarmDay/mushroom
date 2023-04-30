from django.core.management.base import BaseCommand
import pandas as pd
import numpy as np
from ...models import Salary, Employee
class Command(BaseCommand):
    help = "Import Data from excel at targetted position to update Employee and Salary"

    def add_arguments(self, parser):
        parser.add_argument("file_location", type=str, help="location of excel file")

    def handle(self, *args, **kwargs):
        file_location = kwargs["file_location"]
        excel = pd.ExcelFile(file_location)
        for cursheet in excel.sheet_names:
            cursheet = str(cursheet)
            atr = cursheet.split('_')
            if atr[0] == "salary" and len(atr) == 2:
                print(f"-- current sheet is {cursheet}\n")
                df = excel.parse(cursheet)
                df.fillna('')
                df = df.set_axis(["SID", "chi_name", "salary", "pay_status"], axis='columns')
                df.insert(2, "eng_name", '')
                df["eng_name"] = np.where((df["chi_name"]).str.len() >= 4, df["chi_name"], "")
                df["chi_name"] = np.where((df["chi_name"]).str.len() >= 4, "", df["chi_name"])
                print(df)
                for _, row in df.iterrows():
                    print(row)
                    if (pd.isnull(row["SID"])):
                        continue
                    employee = (Employee.objects.update_or_create(SID=int(row["SID"]), chi_name=row["chi_name"], eng_name=row["eng_name"]))[0]
                    if (not pd.isnull(row["salary"])):
                        month = atr[1]
                        pid = str(employee.SID) + '_' + month
                        if (pd.isna(row['pay_status'])):
                            Salary.objects.update_or_create(pid=pid, month = month, employee=employee, amount=row["salary"], pay_status = 'N')
                        else:
                            Salary.objects.update_or_create(pid=pid, month = month, employee=employee, amount=row["salary"], pay_status = row["pay_status"])