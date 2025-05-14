import pandas as pd
from pathlib import Path

all_exel_files = []

directory = Path("DatabaseManager\FinalExelFiles")

for file in directory.iterdir():  
    if file.is_file():  # Check if it's a file
        xl = pd.ExcelFile(file) # turn to pd exel file
        all_exel_files.append(xl)
        print(file)
