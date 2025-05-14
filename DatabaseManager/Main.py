import pandas as pd
from CalculationHandeler import all_country_names, all_country_data 

# Makes the format of the exel doc
header_format = [[], [" ","PR","SN","LD","SP","% functional CCE",
                      "% non-functional CCE", "% facilities with sufficient storage capacity",
                      "% facilities with insufficient storage capacity", "% PQS-prequalified CCE",
                      "% PIS-prequalified CCE", "% non-prequalified CCE",
                      "% electricity", "% solar", "% kereosene", "% gas", "No CCE", "CCE",
                      "% functional CCE", "% non-functional CCE","% facilities with sufficient storage capacity",
                      "% facilities with insufficient storage capacity","% PQS-prequalified CCE","% PIS-prequalified CCE",
                      "% non-PQS-prequalified CCE","% electricity","% solar (SDD+SB)","% kereosene","% gas",
                      " "," ","Maintenance","Energy","Maintenance + energy","Kerosene","Gas","Kerosene + gas"]]
def format_header():
    for i in range(1):
        header_format[0].append("Year")
    for i in range(4):
        header_format[0].append("All facilities")
    for i in range(7):
        header_format[0].append("LD facilities with CCE")
    for i in range(4):
        header_format[0].append("LD facilities with functional CCE")
    for i in range(2):
        header_format[0].append("SP facilities")
    for i in range(7):
        header_format[0].append("SP facilities with CCE")
    for i in range(4):
        header_format[0].append("SP facilities with functional CCE")
    for i in range(1):
        header_format[0].append("Service point density")
    for i in range(1):
        header_format[0].append("Average health facility supply distance")
    for i in range(3):
        header_format[0].append("Estimated annual costs")
    for i in range(3):
        header_format[0].append("Annual cO2 consumption (kg)")
format_header()

# Style exel sheet
print(len(all_country_data))
final_df = pd.DataFrame((all_country_data),
                        index= [all_country_names],
                  columns=pd.MultiIndex.from_arrays(header_format, names=('Country', " ")))

# Write to the exel file
with pd.ExcelWriter('DatabaseManager/database.xlsx') as writer:
    final_df.to_excel(writer, sheet_name="Sheet_3")