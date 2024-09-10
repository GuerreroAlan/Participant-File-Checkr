import pandas as pd

from DataIntegrityCalc import DataIntegrityList
from BlankCellsCalc import BlankCellsTable
from duplicatedCellsCalc import DuplicatedCellsTable
from EmailValidationCalc import EmailValidationTable
from SpecialCharsCalc import UnsupportedCharsTable
from DataLengthCalc import ExcessiveLength

# Function to check/read CSV
def check_csv(file_path, optionalColumns, domains_accepted,unsupported_chars, checks):
    df = pd.read_csv(file_path, dtype='str')
    df.describe()
    blankIndex =['']*len(df)
    df.index=blankIndex
    summary = {}
    dfColumns = df.columns.values

    # data integrity check
    if 'data_integrity' in checks:
        required_columns = ['Unique Identifier', 'First Name', 'Last Name', 'Email']
        if optionalColumns[0] and 'blank_cells' in checks:
            required_columns.extend(optionalColumns)
        dataIntegrityResult = DataIntegrityList(df, required_columns)

    if 'blank_cells' in checks:
        required_columns = ['Unique Identifier', 'First Name', 'Last Name', 'Email']
        if optionalColumns[0]:
            required_columns.extend(optionalColumns)
        blankCellsResult = BlankCellsTable(df, required_columns)
        summary['blank_cells'] = blankCellsResult

    if 'duplicate_identifiers' in checks:
        required_columns = ['Unique Identifier', 'Email']

        duplicatedCellsResult = DuplicatedCellsTable(df, required_columns)

        summary['duplicated_cells'] = duplicatedCellsResult

    if 'email_errors' in checks:
        validEmailsResult = EmailValidationTable(df, domains_accepted)

        summary['email_errors'] = validEmailsResult

    if 'unsupported_char_errors' in checks:
        required_columns = dfColumns

        unsupportedCharsResult = UnsupportedCharsTable(df, unsupported_chars, required_columns)

        summary['unsupported_char_errors'] = unsupportedCharsResult

    if 'excessive_length_errors' in checks:
        required_columns = dfColumns
        excessiveLengthResult = ExcessiveLength(df, required_columns)

        summary['excessive_length_errors'] = excessiveLengthResult

    return summary