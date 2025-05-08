import os
import openpyxl

# Create a new Excel workbook and sheet
wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = "AVX2 Support"
sheet.append(["Hostname", "AVX2 Support"])

# Directory where Ansible saves results
results_dir = "./avx2_results/"

# Parse each result file
for filename in os.listdir(results_dir):
    if filename.endswith(".txt"):
        with open(os.path.join(results_dir, filename), 'r') as file:
            line = file.read().strip()
            hostname, status = line.split(": ")
            sheet.append([hostname, status])

# Save Excel file
wb.save("avx2_support_report.xlsx")
print("Excel report saved as 'avx2_support_report.xlsx'")
