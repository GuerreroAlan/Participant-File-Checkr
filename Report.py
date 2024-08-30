import pandas as pd
import datetime
from tkinter import  messagebox
import os


# Function to print error summaries
def print_summary(summary, file_name, word_unsupported_characters_insert, checks, BlankCheckColumns):

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
            output.write(f'- For blank cells, check in the following columns: "{BlankCheckColumns}".\n    + There can be extra blank cells causing issues. \n')
        if 'duplicate_identifiers' in checks:
            output.write('- For duplicated values, the program will return the values that are duplicated in the columns "Unique Identifier and Email". \n    + You will have to manually update and fix the ones that are wrong. \n')
        if 'email_errors' in checks:
            output.write("- For Email validation, the program will return issues related with:\n   + Unsupported Email Domains.\n   + Unsupported characters in the username. \n")
        if 'unsupported_char_errors' in checks:
            output.write(f'- For unsupported characters, the program search for the following characters:"{word_unsupported_characters_insert}" within all the columns in the file.\n')
        if 'excessive_length_errors' in checks:
            output.write('- For the excessive lengths we search for values:\n    + higher than 50 characters in columns "First Name and Last Name".\n    + higher than 100 characters in columns "Email and Unique Identifier". \n    + higher than 1000 in any other column.')
    
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
            newCol = colName + ':'
            df = pd.DataFrame(info)
            df.insert(loc=0,column=newCol, value=newCol)
            df.to_csv(thisReportPath + "/DuplicatedIdentifiersReport.csv", mode='a', index=False)

    # Email Validation
    if 'email_errors' in checks: 
        # creating a csv file for duplicated identifiers
        for colName, info in summary['email_errors'].items():
            # converting the info into a dataframe
            newCol = colName + ':'
            df = pd.DataFrame(info)
            df.insert(loc=0,column=newCol, value=newCol)
            df.to_csv(thisReportPath + "/EmailValidationReport.csv", mode='a', index=False)

    # Unsupported Characters
    if 'unsupported_char_errors' in checks:
        # creating a csv file for duplicated identifiers
        for colName, info in summary['unsopported_char_errors'].items():
            # converting the info into a dataframe
            newCol = colName + ':'
            df = pd.DataFrame(info)
            df.insert(loc=0,column=newCol, value=newCol)
            df.to_csv(thisReportPath + "/UnsupportedCharReport.csv", mode='a', index=False)

    # Excessive Length
    if 'excessive_length_errors' in checks:
        # creating a csv file for duplicated identifiers
        for colName, info in summary['excessive_length_errors'].items():
            # converting the info into a dataframe
            newCol = colName + ':'
            df = pd.DataFrame(info)
            df.insert(loc=0,column=newCol, value=newCol)
            df.to_csv(thisReportPath + "/ExcessiveLengthReport.csv", mode='a', index=False)

    messagebox.showinfo("Report Generated", "Report Generated")



    