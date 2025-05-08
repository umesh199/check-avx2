import os
import subprocess
import openpyxl

# 1. Create results directory if it doesn't exist
results_dir = "avx2_results"
os.makedirs(results_dir, exist_ok=True)

# 2. Write the Ansible playbook to a temporary file
playbook_content = '''---
- name: Check AVX2 support on multiple hosts
  hosts: all
  gather_facts: no
  tasks:
    - name: Check for AVX2 support
      shell: "grep -i avx2 /proc/cpuinfo || echo 'not found'"
      register: avx2_check

    - name: Save result to a local file
      delegate_to: localhost
      copy:
        content: |
          {{ inventory_hostname }}: {{ 'Supported' if 'avx2' in avx2_check.stdout.lower() else 'Not Supported' }}
        dest: "./avx2_results/{{ inventory_hostname }}.txt"
'''
with open("check_avx2.yml", "w") as f:
    f.write(playbook_content)

# 3. Run the Ansible playbook
inventory_file = "hosts.ini"  # Make sure this exists
print("Running Ansible playbook...")
subprocess.run(["ansible-playbook", "-i", inventory_file, "check_avx2.yml"], check=True)
print("Ansible playbook execution completed.")

# 4. Create Excel workbook
wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = "AVX2 Support"
sheet.append(["Hostname", "AVX2 Support"])

# 5. Read Ansible output and write to Excel
for filename in os.listdir(results_dir):
    if filename.endswith(".txt"):
        with open(os.path.join(results_dir, filename), 'r') as file:
            line = file.read().strip()
            if ": " in line:
                hostname, status = line.split(": ", 1)
                sheet.append([hostname, status])

# 6. Save Excel file
excel_file = "avx2_support_report.xlsx"
wb.save(excel_file)
print(f"Excel report saved as '{excel_file}'")
