import pandas as pd
import re
import datetime
from docx import Document
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser

# Function to establish valid email domains in the CSV
def valid_email(email, domains_accepted):
    regex_domains = '|'.join([re.escape(domain) for domain in domains_accepted])
    pattern = rf"^[a-zA-Z0-9.%+-]+(?:'[a-zA-Z0-9.%+-]+)*@({regex_domains})$"
    return re.match(pattern, email) is not None

# Function to check for unsupported characters
def check_unsupported_characters(df,unsupported_chars_received):
    #Define the regex with the user entry
    unsupported_chars = rf'[{unsupported_chars_received}]'
    
    unsupported_char_errors = []
    for index, row in df.iterrows():
        for column in df.columns:
            if column in ['First Name', 'Last Name', 'Email', 'Unique Identifier', 'Manager_ID'] and re.search(unsupported_chars, str(row[column])):
                unsupported_char_errors.append((index + 1, column, row[column]))
    return unsupported_char_errors

# Function to check for excessive character lengths
def check_excessive_lengths(df):
    excessive_length_errors = []
    for index, row in df.iterrows():
        for column in df.columns:
            value = str(row[column])
            if column in ['First Name', 'Last Name'] and len(value) > 49:
                excessive_length_errors.append((index + 1, column, len(value)))
            elif column in ['Email', 'Unique Identifier'] and len(value) > 99:
                excessive_length_errors.append((index + 1, column, len(value)))
            elif len(value) > 1000:
                excessive_length_errors.append((index + 1, column, len(value)))
    return excessive_length_errors

# Function to check/read CSV
def check_csv(file_path, domains_accepted,unsupported_chars, checks):
    df = pd.read_csv(file_path)
    email_errors = []
    duplicate_emails = []
    duplicate_identifiers = []
    blank_cells = []
    unsupported_char_errors = []
    excessive_length_errors = []

    if 'blank_cells' in checks:
        required_columns = ['First Name', 'Last Name', 'Email', 'Unique Identifier', 'Manager_ID']
        for index, row in df.iterrows():
            for column in required_columns:
                if column in df.columns and pd.isna(row[column]):
                    first_name = row['First Name'] if 'First Name' in df.columns else 'N/A'
                    last_name = row['Last Name'] if 'Last Name' in df.columns else 'N/A'
                    blank_cells.append((index + 1, column, first_name, last_name))
        blank_cells.sort(key=lambda x: x[1])

    if 'duplicate_identifiers' in checks and 'Unique Identifier' in df.columns:
        identifier_counts = df['Unique Identifier'].value_counts()
        duplicate_identifiers = [(i + 1, identifier, df.loc[i, 'First Name'], df.loc[i, 'Last Name']) for i, identifier in enumerate(df['Unique Identifier']) if identifier_counts[identifier] > 1]

    if 'email_errors' in checks and 'Email' in df.columns:
        email_counts = df['Email'].value_counts()
        email_errors = [(i + 1, email) for i, email in enumerate(df['Email']) if pd.notna(email) and not valid_email(str(email), domains_accepted)]
        duplicate_emails = [(i + 1, email, df.loc[i, 'First Name'], df.loc[i, 'Last Name']) for i, email in enumerate(df['Email']) if pd.notna(email) and email_counts[email] > 1]

    if 'unsupported_char_errors' in checks:
        unsupported_char_errors = check_unsupported_characters(df,unsupported_chars)

    if 'excessive_length_errors' in checks:
        excessive_length_errors = check_excessive_lengths(df)

    summary = {
        'email_errors': email_errors,
        'blank_cells': blank_cells,
        'duplicate_emails': duplicate_emails,
        'duplicate_identifiers': duplicate_identifiers,
        'unsupported_char_errors': unsupported_char_errors,
        'excessive_length_errors': excessive_length_errors
    }
    return summary

# Function to print error summaries
def print_summary(summary, file_name):
    doc = Document()
    print("\n-----SUMMARY-----\n")
    
    word_unsupported_characters_insert = user_entry_unsupported_chars.get()
    
    doc.add_heading('HOW TO READ THE FOLLOWING REPORT:', level=1)
    doc.add_paragraph("\n-For Email Errors Summary check, issues can be related with:\n   +Unsupported format of emails address\n   +Unsupported characters in email address\n   +Unsupported email domains\n   +Unsupported characters before '@'") 
    doc.add_paragraph("\n-For blank cells, blank cells can be present across following columns: 'First Name', 'Last Name', 'Email', 'Unique Identifier', 'Manager_ID'.\n  There can be extra blank cells causing issues.")
    doc.add_paragraph("\n-For duplicate Unique Identifiers, the program will return one of the values that are duplicated, you will have to manually update and fix the ones that are worng.")
    doc.add_paragraph(f'\n-For unsupported characters, the program search for the following characters set by the user in the GUI in columns named:First Name, Last Name,Email,Unique Identifier, Manager_ID.\nUser unsupported characters:"{word_unsupported_characters_insert}"')
    doc.add_paragraph("\n-For the excessive lengths we search for values higher than 50 characters in columns First Name and Last Name, and values higher that 100 characters in columns Email and Unique Identifiers\n")
    
    
    doc.add_heading('\nEmail Errors Summary:', level=3)
    if summary['email_errors']:
        for row, email in summary['email_errors']:
            result = f" - Row: {row}, Wrong Email: {email}"
            print(result)
            doc.add_paragraph(result)
        doc.add_paragraph(f"\nTotal email errors: {len(summary['email_errors'])}\n")
    else:
        doc.add_paragraph(" - No email errors found in this file.\n")
        doc.add_paragraph(f"\nTotal email errors: {len(summary['email_errors'])}\n")

    doc.add_heading("Blank Cells Summary:", level=3)
    if summary['blank_cells']:
        for row, column, first_name, last_name in summary['blank_cells']:
            result = f" - Row: {row} / User: {first_name} {last_name} / Column: {column}"
            print(result)
            doc.add_paragraph(result)
        doc.add_paragraph(f"\nTotal blank cells: {len(summary['blank_cells'])}\n")
    else:
        doc.add_paragraph(" - No blank cells found in this file.\n")
        doc.add_paragraph(f"\nTotal blank cells: {len(summary['blank_cells'])}\n")

    doc.add_heading("Duplicate Emails Summary:", level=3)
    if summary['duplicate_emails']:
        seen = set()
        for row, email, first_name, last_name in summary['duplicate_emails']:
            if email not in seen:
                result = f" - Row: {row} / User: {first_name} {last_name} / Email: {email}"
                print(result)
                doc.add_paragraph(result)
                seen.add(email)
        doc.add_paragraph(f"\nTotal duplicate emails: {len(summary['duplicate_emails'])}\n")
    else:
        doc.add_paragraph(" - No duplicate emails found in this file.\n")
        doc.add_paragraph(f"\nTotal duplicate emails: {len(summary['duplicate_emails'])}\n")

    doc.add_heading("Duplicates Unique Identifiers Summary:", level=3)
    if summary['duplicate_identifiers']:
        for identifier in summary['duplicate_identifiers']:
            result = f" - Row: {identifier[0]} / User: {identifier[2]} {identifier[3]} / Duplicate ID: {identifier[1]}"
            print(result)
            doc.add_paragraph(result)
        doc.add_paragraph(f"\nTotal duplicate unique identifiers found: {len(summary['duplicate_identifiers'])}\n")
    else:
        doc.add_paragraph(" - No duplicate unique identifiers found in this file.\n")
        doc.add_paragraph(f"\nTotal duplicate unique identifiers found: {len(summary['duplicate_identifiers'])}\n")

    doc.add_heading("Unsupported Characters Summary:", level=3)
    if summary['unsupported_char_errors']:
        for row, column, value in summary['unsupported_char_errors']:
            result = f" - Row: {row} / Column: {column} / Value: {value}"
            print(result)
            doc.add_paragraph(result)
        doc.add_paragraph(f"\nTotal unsupported characters found: {len(summary['unsupported_char_errors'])}\n")
    else:
        doc.add_paragraph(" - No unsupported characters found in this file.\n")
        doc.add_paragraph(f"\nTotal unsupported characters found: {len(summary['unsupported_char_errors'])}\n")

    doc.add_heading("Excessive Length Summary:", level=3)
    if summary['excessive_length_errors']:
        for row, column, length in summary['excessive_length_errors']:
            result = f" - Row: {row} / Column: {column} / Length: {length}"
            print(result)
            doc.add_paragraph(result)
        doc.add_paragraph(f"\nTotal excessive length errors: {len(summary['excessive_length_errors'])}\n")
    else:
        doc.add_paragraph(" - No excessive length errors found in this file.\n")
        doc.add_paragraph(f"\nTotal excessive length errors: {len(summary['excessive_length_errors'])}\n")

    today = datetime.datetime.today()
    timestamp_str = today.strftime("%Y%m%d_%H%M")
    new_filename_to_save =file_name.split('/')
    print(file_name)
    
    
    #Extract the file name to delete ".csv" string
    final_filename = new_filename_to_save[-1]
    
    #Extract the # of charcaters to be deleted from the original path and assign to the new folder
    len_user_file=len(final_filename)+1
    
    #Delete the lenght of the user file to create the original path
    new_path_to_save = file_name[0:-len_user_file]
   
    #Setting new path to the ERROR_REPORTS FOLDER and creating new error report file name
    doc.save(f'{new_path_to_save}/ERROR_REPORTS/{final_filename[0:-4]}-error_report_{timestamp_str}.docx')
    messagebox.showinfo("Report Generated", f"Report saved as {final_filename[0:-4]}-error_report_{timestamp_str}.docx")

def run_checks():
    file_path = file_entry.get()
    domains = domains_entry.get().split(',')
    #Get unsupported chars
    user_unsupported_chars = user_entry_unsupported_chars.get()#.split(',')
    
    
    checks = []
    if var_blank_cells.get():
        checks.append('blank_cells')
    if var_duplicate_ids.get():
        checks.append('duplicate_identifiers')
    if var_invalid_emails.get():
        checks.append('email_errors')
    if var_unsupported_chars.get():
        checks.append('unsupported_char_errors')
    if var_excessive_lengths.get():
        checks.append('excessive_length_errors')

    if not file_path or not domains or not user_unsupported_chars:
        messagebox.showerror("Error", "Please provide both file path, valid email domains and unsupported characters.")
        return

    summary = check_csv(file_path, domains,user_unsupported_chars, checks)
    print_summary(summary, file_path)

def browse_files():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

# Set up the main application window
root = tk.Tk()
root.title("Participant File Checker")

#Styles
blue_btn=ttk.Style().configure("blue.btn",foreground="black",background = "#0a8fab")

# File selection
file_label = tk.Label(root, text="Participant File Path:")
file_label.grid(row=0, column=0, padx=20, pady=20, sticky=tk.W)
file_entry = tk.Entry(root, width=30)
file_entry.grid(row=0, column=1, padx=20, pady=20)
browse_button = tk.Button(root, text="Browse",command=browse_files)
browse_button.grid(row=0, column=2, padx=20, pady=20)

# Email domains input
domains_label = tk.Label(root, text="Valid Email Domains in your PF (comma-separated without '@'):")
domains_label.grid(row=1, column=0, padx=20, pady=20, sticky=tk.W)
domains_entry = tk.Entry(root, width=30)
domains_entry.grid(row=1, column=1, padx=0, pady=20, columnspan=2)

#Unsupported characters input
user_unsupported_chars_label =tk.Label (root, text="Enter the unsupported characters in your file (NO comma-separated)")
user_unsupported_chars_label.grid(row=2, column=0, padx=20, pady=20, sticky=tk.W)
user_entry_unsupported_chars = tk.Entry(root, width=30)
user_entry_unsupported_chars.grid(row=2, column=1, padx=0, pady=20, columnspan=2)

# Check options
var_blank_cells = tk.BooleanVar()
var_duplicate_ids = tk.BooleanVar()
var_invalid_emails = tk.BooleanVar()
var_unsupported_chars = tk.BooleanVar()
var_excessive_lengths = tk.BooleanVar()

checks_frame = tk.LabelFrame(root, text="Select required check(s) for your participant file")
checks_frame.grid(row=3, column=0, columnspan=10, padx=20, pady=30, sticky=tk.W)

blank_cells_check = tk.Checkbutton(checks_frame, text="Check for blank cells", variable=var_blank_cells)
blank_cells_check.grid(row=1, column=0, sticky=tk.W)

duplicate_ids_check = tk.Checkbutton(checks_frame, text="Check for duplicate unique identifiers", variable=var_duplicate_ids)
duplicate_ids_check.grid(row=2, column=0, sticky=tk.W)

invalid_emails_check = tk.Checkbutton(checks_frame, text="Check for invalid and duplicate emails", variable=var_invalid_emails)
invalid_emails_check.grid(row=3, column=0, sticky=tk.W)

unsupported_chars_check = tk.Checkbutton(checks_frame, text="Check for unsupported characters", variable=var_unsupported_chars)
unsupported_chars_check.grid(row=4, column=0, sticky=tk.W)

excessive_lengths_check = tk.Checkbutton(checks_frame, text="Check for excessive lengths", variable=var_excessive_lengths)
excessive_lengths_check.grid(row=5, column=0, sticky=tk.W)

#LIST OF UNSUPPORTED CHARACTERS

unsupported_chars_list_frame = tk.LabelFrame(root, text = "HOW TO USE:")
unsupported_chars_list_frame.grid(row=3, column=1,columnspan=10, padx=20, pady=30, sticky=tk.W)

unsupported_chars_list_1=tk.Label(unsupported_chars_list_frame, text='1.Select the participant file to analyze. ')
unsupported_chars_list_1.grid(row=1, column=1, padx=20, pady=20, sticky=tk.W)
unsupported_chars_list_2=tk.Label(unsupported_chars_list_frame, text='2.Provide valid email domains and unsupported characters. ')
unsupported_chars_list_2.grid(row=2, column=1, padx=20, pady=20, sticky=tk.W)
unsupported_chars_list_3=tk.Label(unsupported_chars_list_frame, text='3.Select all the checks you needs')
unsupported_chars_list_3.grid(row=3, column=1, padx=20, pady=20, sticky=tk.W)
unsupported_chars_list_4=tk.Label(unsupported_chars_list_frame, text='4.Click "Run Check!"')
unsupported_chars_list_4.grid(row=4, column=1, padx=20, pady=20, sticky=tk.W)


# Run checks button
run_button = tk.Button(root, text="Run Checks!", command=run_checks)
run_button.grid(row=4, column=0, columnspan=3, padx=20, pady=20)

new=1
url = "https://coda.io/d/CSV-checkr_diYJsprOr4k/Team-Ideas_su-_a#_luQT9"

def openweb():
    webbrowser.open(url,new=new)

feedback_button= tk.Button(root, text ="Feedback / New ideas", command=openweb)
feedback_button.grid(row=4, column=1, columnspan=3, padx=20, pady=20)



# Start the application
root.mainloop()