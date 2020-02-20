
import PyPDF2
file_name = "codebook18_llcp-v2-508.pdf"
pdfFileObj = open(file_name, 'rb')

pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
page_numbers = pdfReader.numPages
print("number of pages: " + str(page_numbers))

variable_names, column_values = [], []

for page_idx in range(1, page_numbers):
    pageObj = pdfReader.getPage(page_idx)
    page_text = pageObj.extractText()
    page_text = page_text.split('\n')

    label_found, section_found, column_found = False, False, False
    var_name, col_number = "", ""
    for line_idx, line in enumerate(page_text):
        if line == ' ':
            continue

        if "Label:" in line:
            label_found = True
            continue

        if label_found:
            var_name = var_name + " " + line

        if label_found and "Name:" in line:
            var_name = var_name[1:len(var_name)-14]
            variable_names.append(var_name)
            section_found = True

        if section_found and "Column:" in line:
            column_found = True
            continue

        if column_found:
            col_number = col_number + " " + line

        if column_found and "Type" in line:
            col_number = col_number[1:len(col_number)-5]
            column_values.append(col_number)

            label_found, section_found, column_found = False, False, False
            var_name, col_number = "", ""
            continue

var_name_set = {}
print("var idx, column values, length, variable names:")
counter = 1
for idx in range(0, len(variable_names)):
    if variable_names[idx] not in var_name_set:
        var_name_set[variable_names[idx]] = column_values[idx]

        column_details = column_values[idx]
        if "-" in column_details:
            column_details = column_details.split("-")
            column_details = [int(column_details[0]), int(column_details[1])]
        else:
            column_details = [int(column_details)]

        # if len(column_details) == 1:
        #     print(str(counter) + ". " + column_values[idx] + " :: 1 :: " + variable_names[idx])
        # else:
        #     print(str(counter) + ". " + column_values[idx] + " :: " + str(column_details[1] - column_details[0] + 1) + " :: " + variable_names[idx])
        # counter += 1
    else:
        if column_values[idx] != var_name_set[variable_names[idx]]:

            column_details = column_values[idx]
            if "-" in column_details:
                column_details = column_details.split("-")
                column_details = [int(column_details[0]), int(column_details[1])]
            else:
                column_details = [int(column_details)]

            if len(column_details) == 1:
                print("rep " + str(counter) + ". " + column_values[idx] + " :: 1 :: " + variable_names[idx])
            else:
                print("rep " + str(counter) + ". " + column_values[idx] + " :: " + str(column_details[1] - column_details[0] + 1) + " :: " + variable_names[idx])
            counter += 1

        # else:
        #     if len(column_details) == 1:
        #         print("rep " + str(counter) + ". " + column_values[idx] + " :: 1 :: " + variable_names[idx])
        #     else:
        #         print("rep " + str(counter) + ". " + column_values[idx] + " :: " + str(column_details[1] - column_details[0] + 1) + " :: " + variable_names[idx])
        #     counter += 1
pdfFileObj.close()
