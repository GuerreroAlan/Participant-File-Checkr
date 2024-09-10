
import pandas as pd  

def EmailValidationTable(df, domains_accepted):

    EmailValidTable = {}
    EmailHelper = df['Email'].str.split("@", n=1, expand=True)
    df['EmailUsername'] = EmailHelper[0]
    df['EmailDomain'] = EmailHelper[1]

    df['isDomainStart']= df['EmailDomain'].str.startswith(domains_accepted)
    df['isDomainEnd'] = df['EmailDomain'].str.endswith(domains_accepted)
    notValidDomainEmails = df[(df['isDomainStart'] == False) | (df['isDomainEnd'] == False)]

    notEmptyRows = []
    notEmptyRows = df[(df['EmailUsername'].notna()) & (df['EmailUsername'].notnull())]
    specialCharsEmail = notEmptyRows[notEmptyRows['EmailUsername'].str.contains(r'[^0-9a-zA-Z._\-%\+\?:\']')]

    if (len(notValidDomainEmails) == 0):
        notValidDomainEmails = pd.DataFrame(columns=['There are no invalid domains in the list of Emails.'])
        EmailValidTable['Domain'] = notValidDomainEmails
    else:
        EmailValidTable['Domain'] = notValidDomainEmails[['Unique Identifier', 'Email']]

    if (len(specialCharsEmail) == 0):
        specialCharsEmail = pd.DataFrame(columns=['There are no unsupported characters in the list of Emails.'])
        EmailValidTable['Username'] = specialCharsEmail
    else:
        EmailValidTable['Username'] = specialCharsEmail[['Unique Identifier', 'Email']]
    
    return EmailValidTable




