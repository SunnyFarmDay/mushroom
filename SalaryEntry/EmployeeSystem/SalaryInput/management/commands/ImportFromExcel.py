from django.core.management.base import BaseCommand
import pandas as pd

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
                print(df)

            
        