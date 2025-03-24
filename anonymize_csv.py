import csv
import re
import faker
import spacy

fake = faker.Faker('it_IT')

name_mapping = {}
company_mapping = {}
email_mapping = {}
phone_mapping = {}
cf_mapping = {}
case_id_mapping = {}
account_id_mapping = {}
contract_id_mapping = {}
preventivo_id_mapping = {}
ritm_id_mapping = {}
task_id_mapping = {}
ods_id_mapping = {}
impianto_id_mapping = {}
conto_contrattuale_id_mapping = {}
bp_id_mapping = {}
mandato_id_mapping = {}
documento_id_mapping = {}
fm_id_mapping = {}
ordine_id_mapping = {}
cod_prat_utente_id_mapping = {}
asset_id_mapping = {}

# Load the Italian spaCy model - you might need to download it first (see instructions below)
nlp = spacy.load("it_core_news_lg") # Or try "it_core_news_lg" for potentially better accuracy


def anonymize_name(name):
    if not name:
        return name
    if name not in name_mapping:
        name_mapping[name] = fake.name()
    return name_mapping[name]

def anonymize_company(company):
    if not company:
        return company
    if company not in company_mapping:
        company_mapping[company] = fake.company()
    return company_mapping[company]

def anonymize_email(email):
    if not email:
        return email
    if email not in email_mapping:
        username, domain = email.split('@') if '@' in email else (email, 'example.com')
        email_mapping[email] = f"{fake.user_name()}@{fake.domain_name()}"
    return email_mapping[email]

def anonymize_phone(phone):
    if not phone:
        return phone
    if phone not in phone_mapping:
        phone_mapping[phone] = fake.phone_number()
    return phone_mapping[phone]

def anonymize_cf(cf):
    if not cf:
        return cf
    if cf not in cf_mapping:
        cf_mapping[cf] = fake.ssn() # Using ssn as a placeholder for a plausible but fake code
    return cf_mapping[cf]

def anonymize_id(id_val, mapping_dict, prefix='ANONYMIZED'):
    if not id_val:
        return id_val
    if id_val not in mapping_dict:
        mapping_dict[id_val] = f"{prefix}_{fake.random_number(digits=7)}"
    return mapping_dict[id_val]


def anonymize_text_spacy(text):
    if not text:
        return text

    doc = nlp(text)
    new_text_parts = []
    last_char_index = 0

    for ent in doc.ents:
        if ent.label_ == "PER": # "PER" is the label for "PERSON" in spaCy Italian model
            new_text_parts.append(text[last_char_index:ent.start_char]) # Add text before entity
            new_text_parts.append(anonymize_name(ent.text)) # Add anonymized name
            last_char_index = ent.end_char # Update index to after entity
        else:
            pass # For other entities, we keep original text for now

    new_text_parts.append(text[last_char_index:]) # Add remaining text after last entity
    text = "".join(new_text_parts) # Reassemble text with anonymized names

    return text


def anonymize_email_phone_ids(text): # Function to anonymize emails, phones and IDs (reused)
    if not text:
        return text

    # Anonymize emails
    for email in set(re.findall(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', text)):
        text = text.replace(email, anonymize_email(email))

    # Anonymize phone numbers (simple pattern, might need refinement)
    for phone in set(re.findall(r'\b(?:\+?39)?\s?\(?0?\)?\s?\d{3}\s?[-.\s]?\d{3}\s?[-.\s]?\d{4}\b', text)):
        text = text.replace(phone, anonymize_phone(phone))
    for phone in set(re.findall(r'\b0\d{9,10}\b', text)): # Italian phone numbers starting with 0
        text = text.replace(phone, anonymize_phone(phone))

    # Anonymize company names (very basic, can be improved with more sophisticated NER)
    for company in set(re.findall(r'\b[A-Z][a-zA-Z0-9\s\.\&\,\-]+(?:S\.R\.L\.|S\.P\.A\.|S\.N\.C\.|SRL|SPA|SNC)\b', text)):
        text = text.replace(company, anonymize_company(company))
    for company in set(re.findall(r'\b[A-Z][a-zA-Z0-9\s\.\&\,\-]+(?:SRL|SPA|SNC)\b', text)): # Company names without dots
        text = text.replace(company, anonymize_company(company))

    # Anonymize Case IDs like 09[0-9]{6} or 9[0-9]{6}
    for case_id in set(re.findall(r'\b0?9\d{6,7}\b', text)):
        text = text.replace(case_id, anonymize_id(case_id, case_id_mapping, 'CASE'))
    for case_id in set(re.findall(r'\bcase\s*0?9\d{6,7}\b', text, re.IGNORECASE)):
        text = text.replace(case_id, f"case {anonymize_id(case_id.split('case')[-1].strip(), case_id_mapping, 'CASE')}")
    for case_id in set(re.findall(r'\bcase\s*n\.\s*0?9\d{6,7}\b', text, re.IGNORECASE)):
        text = text.replace(case_id, f"case n. {anonymize_id(case_id.split('n.')[-1].strip(), case_id_mapping, 'CASE')}")
    for case_id in set(re.findall(r'\bCase\s*n\.\s*0?9\d{6,7}\b', text)):
        text = text.replace(case_id, f"Case n. {anonymize_id(case_id.split('n.')[-1].strip(), case_id_mapping, 'CASE')}")
    for case_id in set(re.findall(r'\bcase:\s*0?9\d{6,7}\b', text, re.IGNORECASE)):
        text = text.replace(case_id, f"case: {anonymize_id(case_id.split(':')[-1].strip(), case_id_mapping, 'CASE')}")

    # Anonymize Account IDs like 20000[0-9]{8} or 25000[0-9]{8}
    for account_id in set(re.findall(r'\b(?:20|25)0{3}\d{8}\b', text)):
        text = text.replace(account_id, anonymize_id(account_id, account_id_mapping, 'ACCOUNT'))
    for account_id in set(re.findall(r'\bac\s*(?:20|25)0{3}\d{8}\b', text, re.IGNORECASE)):
        text = text.replace(account_id, f"ac {anonymize_id(account_id.split('ac')[-1].strip(), account_id_mapping, 'ACCOUNT')}")
    for account_id in set(re.findall(r'\bca\s*(?:20|25)0{3}\d{8}\b', text, re.IGNORECASE)):
        text = text.replace(account_id, f"ca {anonymize_id(account_id.split('ca')[-1].strip(), account_id_mapping, 'ACCOUNT')}")
    for account_id in set(re.findall(r'\bconto contrattuale\s*(?:20|25)0{3}\d{8}\b', text, re.IGNORECASE)):
        text = text.replace(account_id, f"conto contrattuale {anonymize_id(account_id.split('contrattuale')[-1].strip(), account_id_mapping, 'ACCOUNT')}")

    # Anonymize Contract IDs like 3[0-9]{9,10} or 350[0-9]{8} or 360[0-9]{8}
    for contract_id in set(re.findall(r'\b(?:3[56]0{2}|3)\d{8,10}\b', text)):
        text = text.replace(contract_id, anonymize_id(contract_id, contract_id_mapping, 'CONTRACT'))
    for contract_id in set(re.findall(r'\bcontratto\s*(?:3[56]0{2}|3)\d{8,10}\b', text, re.IGNORECASE)):
        text = text.replace(contract_id, f"contratto {anonymize_id(contract_id.split('contratto')[-1].strip(), contract_id_mapping, 'CONTRACT')}")

    # Anonymize Preventivo IDs like 110[0-9]{6}
    for preventivo_id in set(re.findall(r'\b110\d{6}\b', text)):
        text = text.replace(preventivo_id, anonymize_id(preventivo_id, preventivo_id_mapping, 'PREVENTIVO'))
    for preventivo_id in set(re.findall(r'\bpreventivo\s*n\.?\s*110\d{6}\b', text, re.IGNORECASE)):
        text = text.replace(preventivo_id, f"preventivo n. {anonymize_id(preventivo_id.split('preventivo')[-1].strip(), preventivo_id_mapping, 'PREVENTIVO')}")

    # Anonymize RITM IDs like RITM[0-9]{7}
    for ritm_id in set(re.findall(r'\bRITM\d{7}\b', text)):
        text = text.replace(ritm_id, anonymize_id(ritm_id, ritm_id_mapping, 'RITM'))

    # Anonymize SCTASK IDs like SCTASK[0-9]{7}
    for task_id in set(re.findall(r'\bSCTASK\d{7}\b', text)):
        text = text.replace(task_id, anonymize_id(task_id, task_id_mapping, 'SCTASK'))
    for task_id in set(re.findall(r'\bTask SCTASK\d{7}\b', text)):
        text = text.replace(task_id, f"Task {anonymize_id(task_id.split('Task')[-1].strip(), task_id_mapping, 'SCTASK')}")

    # Anonymize ODS IDs like 00095[0-9]{8}
    for ods_id in set(re.findall(r'\b00095\d{8}\b', text)):
        text = text.replace(ods_id, anonymize_id(ods_id, ods_id_mapping, 'ODS'))
    for ods_id in set(re.findall(r'\bodl\s*95\d{8}\b', text, re.IGNORECASE)):
        text = text.replace(ods_id, f"odl {anonymize_id(ods_id.split('odl')[-1].strip(), ods_id_mapping, 'ODS')}")

    # Anonymize Impianto IDs like 400[0-9]{7}
    for impianto_id in set(re.findall(r'\b400\d{7}\b', text)):
        text = text.replace(impianto_id, anonymize_id(impianto_id, impianto_id_mapping, 'IMPIANTO'))
    for impianto_id in set(re.findall(r'\bimpianto\s*400\d{7}\b', text, re.IGNORECASE)):
        text = text.replace(impianto_id, f"impianto {anonymize_id(impianto_id.split('impianto')[-1].strip(), impianto_id_mapping, 'IMPIANTO')}")

    # Anonymize Conto Contrattuale IDs like 2[05]0{3}[0-9]{8}
    for conto_contrattuale_id in set(re.findall(r'\b(?:2[05]0{3})\d{8}\b', text)):
        text = text.replace(conto_contrattuale_id, anonymize_id(conto_contrattuale_id, conto_contrattuale_id_mapping, 'CONTO_CONTRATTUALE'))

    # Anonymize BP IDs like 1[05]0{3}[0-9]{6} or BP-000[0-9]{6}
    for bp_id in set(re.findall(r'\b(?:1[05]0{3})\d{6}\b', text)):
        text = text.replace(bp_id, anonymize_id(bp_id, bp_id_mapping, 'BP'))
    for bp_id in set(re.findall(r'\bBP-000\d{6}\b', text)):
        text = text.replace(bp_id, anonymize_id(bp_id, bp_id_mapping, 'BP'))

    # Anonymize Mandato IDs like 003D[0-9]{16} or A8S07[0-9]{9}
    for mandato_id in set(re.findall(r'\b(?:003D\d{12}|A8S07\d{9})\d{4}\b', text)): # Adjusted regex for 16 digits after 003D and 9 digits after A8S07
        text = text.replace(mandato_id, anonymize_id(mandato_id, mandato_id_mapping, 'MANDATO'))

    # Anonymize Documento IDs like 20[0-9]{14}
    for documento_id in set(re.findall(r'\b20\d{14}\b', text)):
        text = text.replace(documento_id, anonymize_id(documento_id, documento_id_mapping, 'DOCUMENTO'))

    # Anonymize FM IDs like FM-[0-9]{7}
    for fm_id in set(re.findall(r'\bFM-\d{7}\b', text)):
        text = text.replace(fm_id, anonymize_id(fm_id, fm_id_mapping, 'FM'))

    # Anonymize Ordine IDs like 00095[0-9]{8} (similar to ODS but explicit to differentiate if needed)
    for ordine_id in set(re.findall(r'\b00095\d{8}\b', text)): #Reusing the same regex as ODS, adjust if different pattern needed
        text = text.replace(ordine_id, anonymize_id(ordine_id, ordine_id_mapping, 'ORDINE'))
    for ordine_id in set(re.findall(r'\bodl\s*95\d{8}\b', text, re.IGNORECASE)): #Reusing the same regex as ODS, adjust if different pattern needed
        text = text.replace(ordine_id, f"odl {anonymize_id(ordine_id.split('odl')[-1].strip(), ordine_id_mapping, 'ORDINE')}")

    # Anonymize COD_PRAT_UTENTE IDs like CA-0[6-9]{7}
    for cod_prat_utente_id in set(re.findall(r'\bCA-0[6-9]\d{6}\b', text)):
        text = text.replace(cod_prat_utente_id, anonymize_id(cod_prat_utente_id, cod_prat_utente_id_mapping, 'COD_PRAT_UTENTE'))

    # Anonymize Asset IDs like 02iWi[0-9]{9}
    for asset_id in set(re.findall(r'\b02iWi\d{9}\b', text)):
        text = text.replace(asset_id, anonymize_id(asset_id, asset_id_mapping, 'ASSET'))


    return text


input_csv_path = 'input.csv'  # Replace with your input CSV file path
output_csv_path = 'output_anonymized.csv'

with open(input_csv_path, 'r', newline='', encoding='latin-1') as infile, \
     open(output_csv_path, 'w', newline='', encoding='latin-1') as outfile:

    reader = csv.reader(infile, delimiter=';')
    writer = csv.writer(outfile, delimiter=';')

    header = next(reader)
    writer.writerow(header)

    for row in reader:
        anonymized_row = list(row) # Convert to list to allow modification

        # Anonymize all columns in each row
        for col_index in range(len(anonymized_row)):
            cell_value = anonymized_row[col_index]

            # Apply anonymization functions - Order matters: Spacy first for names, then regex for others
            anonymized_cell_value = anonymize_text_spacy(cell_value) # Anonymize names with spaCy NER
            anonymized_cell_value = anonymize_email_phone_ids(anonymized_cell_value) # Anonymize emails, phones, IDs, companies

            anonymized_row[col_index] = anonymized_cell_value # Update the cell in the row


        writer.writerow(anonymized_row)

print(f"Anonymized CSV saved to {output_csv_path}")