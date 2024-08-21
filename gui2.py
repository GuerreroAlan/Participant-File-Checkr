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
    #Get unsupported chars
    user_unsupported_chars = user_entry_unsupported_chars.get()#.split(',')
    unsopportedChars = ''.join(str(x) for x in user_unsupported_chars)
    print(unsopportedChars)
    
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

    if not file_path:
        messagebox.showerror("Error", "Please select a file.")
        return
    
    if 'email_errors' in checks and not domainsraw:
        messagebox.showerror("Error", "Please provide the domains accepted to validate the emails.")
        return
    
    if 'unsupported_char_errors' in checks and not user_unsupported_chars:
        messagebox.showerror("Error", "Please provide the unsopported characters.")
        return

    summary = check_csv(file_path, domainsAccepted,unsopportedChars, checks)
    print_summary(summary, file_path, unsopportedChars, checks)

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