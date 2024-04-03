import pandas as pd
import string


df = pd.read_excel(r'Second Semester PG November 2023 R 7558.xlsx')

def apply_styles(worksheet, df, workbook):
    worksheet.set_column('A:A', 42 / 7)  # Sl.No.
    worksheet.set_column('B:B', 105 / 7)  # Bundle Code
    worksheet.set_column('C:C', 62 / 7)  # AS Count
    worksheet.set_column('D:D', 171 / 7)  # Course Name
    worksheet.set_column('E:E', 140 / 7)  # District
    worksheet.set_column('F:F', 67 / 7)  # Camp
    worksheet.set_column('G:G', 66 / 7)  # Status

    worksheet.set_default_row(39)

    align_format = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'text_wrap': True
    })

    worksheet.set_margins(left=0.25, right=0.25, top=0.6, bottom=0.3)

    header_format = workbook.add_format({
        'font_size': 15,
        'bold': True,
        'underline': True
    })
    worksheet.set_header('&C&"Arial"&BSecond Semester PG November 2023&"', {'header_header_spacing': 0.3, 'font': header_format})

    # Apply alignment and wrap text to data cells
    for row_num, row_data in enumerate(df.values):
        for col_num, cell_value in enumerate(row_data):
            worksheet.write(row_num + 1, col_num, str(cell_value), align_format)
    
    worksheet.repeat_rows(0)  

    (max_row, max_col) = df.shape
    column_settings = [{"header": column} for column in df.columns]
    worksheet.add_table(0, 0, max_row, max_col - 1, {"columns": column_settings})

writer = pd.ExcelWriter('merged_file.xlsx', engine='xlsxwriter')
workbook = writer.book

for camp in df['Camp'].unique():
    try:
        new_df = df[df['Camp'] == camp]
        new_df.to_excel(writer, sheet_name=camp, index=False, startrow=1, header=False)

        worksheet = writer.sheets[camp]
        apply_styles(worksheet, new_df, workbook)


    except:
        new_df = df[df['Camp'].isnull()]
        new_df.to_excel(writer, sheet_name='Generated', index=False, startrow=1, header=False)

        worksheet = writer.sheets['Generated']
        apply_styles(worksheet, new_df, workbook)


writer.close()
