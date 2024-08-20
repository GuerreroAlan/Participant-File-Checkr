import pandas as pd
import datetime
from tkinter import  messagebox
import os


# Function to print error summaries
def print_summary(summary, file_name, word_unsupported_characters_insert, checks):

    # obtainin the timestamp to add it to the folder and report names
    today = datetime.datetime.today()
    timestamp_str = today.strftime("%Y%m%d_%H%M")
    new_filename_to_save =file_name.split('/')

    #Extract the file name to delete ".csv" string
    final_filename = new_filename_to_save[-1]
    
    #Extract the # of charcaters to be deleted from the original path and assign to the new folder
    len_user_file=len(final_filename)+1
    
    #Delete the length of the user file to create the original path
    new_path_to_save = file_name[0:-len_user_file]

    # Create Folder to save all the reports
    reportPath = new_path_to_save + '/Error_ReportsCSV'
    if not os.path.exists(reportPath):
        os.makedirs(reportPath)
    
    thisReportPath = reportPath + '/' + 'Error_Reports_' + timestamp_str
    # create folder to save this report
    if not os.path.exists(thisReportPath):
        os.makedirs(thisReportPath)

    # create ReadMe File
    with open(thisReportPath + "/ReadMe.txt", "w") as output:
        output.write('How to read the report: \n')
        if 'blank_cells' in checks:
            output.write("For blank cells, blank cells can be present across following columns: 'First Name', 'Last Name', 'Email', 'Unique Identifier', 'Manager_ID'.\n  There can be extra blank cells causing issues. \n")
        if 'duplicate_identifiers' in checks:
            output.write('For duplicated Unique Identifiers, the program will return one of the values that are duplicated, you will have to manually update and fix the ones that are wrong. \n')
        if 'email_errors' in checks:
            output.write("For Email Errors Summary check, issues can be related with:\n   +Unsupported format of emails address\n   +Unsupported characters in email address\n   +Unsupported email domains\n   +Unsupported characters before '@' \n")
        if 'unsupported_char_errors' in checks:
            output.write(f'For unsupported characters, the program search for the following characters set by the user in the GUI in columns named:First Name, Last Name,Email,Unique Identifier, Manager_ID.\nUser unsupported characters:"{word_unsupported_characters_insert} \n"')
        if 'excessive_length_errors' in checks:
            output.write('For the excessive lengths we search for values higher than 50 characters in columns First Name and Last Name, and values higher that 100 characters in columns Email and Unique Identifiers')
    
    # exporting the tables to the report docs
    # Blank cells
    if 'blank_cells' in checks:
        # creating the csv file for blank cells
        summary['blank_cells'].to_csv(thisReportPath + '/BlankCellsReport.csv', index=False)
    # Duplicated Cells
    if 'duplicate_identifiers' in checks:
        # creating a csv file for duplicated identifiers
        for colName, info in summary['duplicated_cells'].items():
            # converting the info into a dataframe
            titleList = [[colName+':', '']]
            title = pd.DataFrame(titleList)
            df = pd.DataFrame(info)
            title.to_csv(thisReportPath + "/DuplicatedIdentifiersReport.csv", mode='a', header=False, index=False)
            df.to_csv(thisReportPath + "/DuplicatedIdentifiersReport.csv", mode='a', index=False)

    # Email Validation
    if 'email_errors' in checks: 
        # creating a csv file for duplicated identifiers
        for colName, info in summary['email_errors'].items():
            # converting the info into a dataframe
            titleList = [[colName+':', '']]
            title = pd.DataFrame(titleList)
            df = pd.DataFrame(info)
            title.to_csv(thisReportPath + "/EmailValidationReport.csv", mode='a', header=False, index=False)
            df.to_csv(thisReportPath + "/EmailValidationReport.csv", mode='a', index=False)

    # Unsupported Characters
    if 'unsupported_char_errors' in checks:
        # creating a csv file for duplicated identifiers
        for colName, info in summary['unsopported_char_errors'].items():
            # converting the info into a dataframe
            titleList = [[colName+':', '']]
            title = pd.DataFrame(titleList)
            df = pd.DataFrame(info)
            title.to_csv(thisReportPath + "/UnsupportedCharReport.csv", mode='a', header=False, index=False)
            df.to_csv(thisReportPath + "/UnsupportedCharReport.csv", mode='a', index=False)

    # Excessive Length
    if 'excessive_length_errors' in checks:
        # creating a csv file for duplicated identifiers
        for colName, info in summary['excessive_length_errors'].items():
            # converting the info into a dataframe
            titleList = [[colName+':', '']]
            title = pd.DataFrame(titleList)
            df = pd.DataFrame(info)
            title.to_csv(thisReportPath + "/ExcessiveLengthReport.csv", mode='a', header=False, index=False)
            df.to_csv(thisReportPath + "/ExcessiveLengthReport.csv", mode='a', index=False)

    messagebox.showinfo("Report Generated", "Report Generated")



    