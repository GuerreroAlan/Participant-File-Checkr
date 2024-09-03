import pandas as pd
import datetime
from docx import Document
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser
import os

from Check_CSV import check_csv
from Report import print_summary

def run_checks():
    # get the file path to be analyzed
    file_path = file_entry.get()
    # get the domains accepted
    domainsraw = domains_entry.get()
    domains = domains_entry.get().split(',')
    # removing extra spaces in the domains
    domains = [x.strip(' ') for x in domains]
        
    domainsAccepted = tuple(domains)

    # get optional columns for blank check
    optionalColumns = blanks_entry.get().split(',')
    optionalColumns = [x.strip(' ') for x in optionalColumns]
    required_columns_Report = ['Unique Identifier', 'First Name', 'Last Name', 'Email']
    if optionalColumns[0]:
        required_columns_Report.extend(optionalColumns)
    BlankCheck_Columns = ', '.join(required_columns_Report)

    #Get unsupported chars
    unsupportedChars = unsupported_Chars_entry.get()#.split(',')
    #unsupportedChars = '[]{}&|;$%()+*,`'
    #print(unsopportedChars)
    
    checks = []
    checks.append('data_integrity')

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

    if not file_path:
        messagebox.showerror("Error", "Please select a file.")
        return
    
    if 'email_errors' in checks and not domainsraw:
        messagebox.showerror("Error", "Please provide the domains accepted to validate the emails.")
        return
    
    if 'unsupported_char_errors' in checks and not unsupportedChars:
        messagebox.showerror("Error", "Please provide unsupported characters to be reviewed.")
        return

    summary = check_csv(file_path, optionalColumns, domainsAccepted, unsupportedChars, checks)
    print_summary(summary, file_path, unsupportedChars, checks, BlankCheck_Columns)

def browse_files():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

# Set up the main application window
root = tk.Tk()
root.title("Participant File Checker v2.1")

#Styles
blue_btn=ttk.Style().configure("blue.btn",foreground="black",background = "#0a8fab")

# File selection
file_label = tk.Label(root, text="Participant File Path:")
file_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
file_entry = tk.Entry(root, width=30)
file_entry.grid(row=0, column=1, padx=5, pady=5)
browse_button = tk.Button(root, text="Browse",command=browse_files)
browse_button.grid(row=0, column=2, padx=5, pady=5)

# function to enable/disable text boxes
# Blank
def BlankCheck():
    BlankCheckFlag = False
    if var_blank_cells.get():
        BlankCheckFlag = True
    if BlankCheckFlag:
        blanks_entry.configure(state='normal', foreground="black")
        blanks_entry.delete(0,tk.END)
    else:
        blanks_entry.delete(0,tk.END)
        blanks_entry.insert(0, "Provide optional columns...")
        blanks_entry.configure(foreground= "gray", state='disabled')
# Domains
def EmailCheck():
    EmailCheckFlag = False
    if var_invalid_emails.get():
        EmailCheckFlag = True
    if EmailCheckFlag:
        domains_entry.configure(state='normal', foreground="black")
        domains_entry.delete(0,tk.END)
    else:
        domains_entry.delete(0,tk.END)
        domains_entry.insert(0, "Provide valid Email Domains...")
        domains_entry.configure(foreground= "gray", state='disabled')

# Unsupported
def UnsupportedCheck():
    UnsupportedCheckFlag = False
    if var_unsupported_chars.get():
        UnsupportedCheckFlag = True
    if UnsupportedCheckFlag:
        unsupported_Chars_entry.configure(state='normal', foreground="black")
    else:
        unsupported_Chars_entry.configure(foreground= "gray", state='disabled')

# Check options
var_blank_cells = tk.BooleanVar()
var_duplicate_ids = tk.BooleanVar()
var_invalid_emails = tk.BooleanVar()
var_unsupported_chars = tk.BooleanVar()
var_excessive_lengths = tk.BooleanVar()

checks_frame = tk.LabelFrame(root, text="Select required check(s) for your participant file")
checks_frame.grid(row=3, column=0, columnspan=5, padx=15, pady=15, sticky=tk.W)

blank_cells_check = tk.Checkbutton(checks_frame, text="Check for blank cells", variable=var_blank_cells, command=BlankCheck)
blank_cells_check.grid(row=1, column=0, sticky=tk.W)
# Optional Columns for Blank Check input
blanks_entry = tk.Entry(checks_frame, width=40)
blanks_entry.insert(0, "Provide optional columns...")
blanks_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=3)
blanks_entry.configure(foreground= "gray", state='disabled')

duplicate_ids_check = tk.Checkbutton(checks_frame, text="Check for duplicated Unique Identifiers and Emails ", variable=var_duplicate_ids)
duplicate_ids_check.grid(row=2, column=0, sticky=tk.W)

invalid_emails_check = tk.Checkbutton(checks_frame, text="Check for invalid emails", variable=var_invalid_emails, command=EmailCheck)
invalid_emails_check.grid(row=3, column=0, sticky=tk.W)
# Email domains input
domains_entry = tk.Entry(checks_frame, width=40)
domains_entry.insert(0, "Provide valid Email Domains...")
domains_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=3)
domains_entry.configure(foreground= "gray", state='disabled')

unsupported_chars_check = tk.Checkbutton(checks_frame, text="Check for unsupported characters", variable=var_unsupported_chars, command=UnsupportedCheck)
unsupported_chars_check.grid(row=4, column=0, sticky=tk.W)
# unsupported characters entry
unsupported_Chars_entry = tk.Entry(checks_frame, width=40)
unsupported_Chars_entry.insert(0, "[]{}&|;$%()+*,`")
unsupported_Chars_entry.grid(row=4, column=1, padx=5, pady=5, columnspan=3)
unsupported_Chars_entry.configure(foreground= "gray", state='disabled')

# excessive length
excessive_lengths_check = tk.Checkbutton(checks_frame, text="Check for excessive lengths", variable=var_excessive_lengths)
excessive_lengths_check.grid(row=5, column=0, sticky=tk.W)

#LIST OF UNSUPPORTED CHARACTERS

unsupported_chars_list_frame = tk.LabelFrame(root, text = "HOW TO USE:")
unsupported_chars_list_frame.grid(row=4, column=0,columnspan=5, padx=15, pady=15, sticky=tk.W)

unsupported_chars_list_1=tk.Label(unsupported_chars_list_frame, text='1. Select the participant file to analyze. ')
unsupported_chars_list_1.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
unsupported_chars_list_3=tk.Label(unsupported_chars_list_frame, text='2. Select all the checks you need.')
unsupported_chars_list_3.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
unsupported_chars_list_2=tk.Label(unsupported_chars_list_frame, text="3. Optionally, provide extra Columns to check for Blanks, (comma-separated).")
unsupported_chars_list_2.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
unsupported_chars_list_2=tk.Label(unsupported_chars_list_frame, text="4. Provide valid Email Domains, (comma-separated, without '@').")
unsupported_chars_list_2.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
unsupported_chars_list_2=tk.Label(unsupported_chars_list_frame, text='5. Provide unsupported characters that will be checked, by default: []{}&|;$%()+*,`')
unsupported_chars_list_2.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
unsupported_chars_list_4=tk.Label(unsupported_chars_list_frame, text='6.Click "Run Check!"')
unsupported_chars_list_4.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)


# Run checks button
run_button = tk.Button(root, text="Run Checks!", command=run_checks)
run_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

new=1
url = "https://coda.io/d/CSV-checkr_diYJsprOr4k/Team-Ideas_su-_a#_luQT9"

def openweb():
    webbrowser.open(url,new=new)

feedback_button= tk.Button(root, text ="Feedback / New ideas", command=openweb)
feedback_button.grid(row=5, column=1, columnspan=3, padx=5, pady=10)



# Start the application
root.mainloop()