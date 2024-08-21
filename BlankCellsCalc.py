import pandas as pd

def BlankCellsTable(df, required_columns):
    for colName in required_columns:
        df[f'{colName}_IsBlank'] = (df[colName].isna()) | (df[colName].isnull())

    blankColumns = df[df.iloc[:, list(range(-len(required_columns),0))].sum(axis=1) >= 1]
    blankColumns = blankColumns.fillna('Blank')

    if len(blankColumns) == 0:
        blankColumnsReport = pd.DataFrame(columns=['There are no blank cells in the selected file.'])
    else:
        blankColumnsReport = blankColumns[required_columns]

    return blankColumnsReport