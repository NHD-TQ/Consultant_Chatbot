import pandas as pd

# excel_file = pd.read_excel("10_groupitem.xlsx")


# Đường dẫn tới file Excel (.xlsx)
excel_file = "data/10_groupitem.xlsx"

# Đọc file Excel
df = pd.read_excel(excel_file)

# Đường dẫn tới file CSV
csv_file = "data.csv"

# Ghi DataFrame vào file CSV với encoding là "utf-8-sig"
df.to_csv(csv_file, index=False, encoding="utf-8-sig")