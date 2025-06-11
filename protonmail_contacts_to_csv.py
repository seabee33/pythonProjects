# a python script that gets the email, number and name from protonmail and puts each email with its own line

import csv
import re

def parse_vcf(file_path):
    contacts = []
    contact = {}

    def flush_contact():
        if not contact:
            return
        name = contact.get('Full Name', '')
        phones = contact.get('Phone Numbers', [])
        emails = contact.get('Emails', [])

        # If multiple emails, create a row for each
        if emails:
            for email in emails:
                contacts.append({
                    'Full Name': name,
                    'Phone Number': phones[0] if phones else '',
                    'Email': email
                })
        else:
            contacts.append({
                'Full Name': name,
                'Phone Number': phones[0] if phones else '',
                'Email': ''
            })

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith("BEGIN:VCARD"):
                contact = {}
            elif line.startswith("FN"):
                contact['Full Name'] = line.split(":", 1)[1]
            elif line.startswith("TEL"):
                number = line.split(":", 1)[1]
                contact.setdefault('Phone Numbers', []).append(number)
            elif re.match(r"ITEM\d+\.EMAIL", line):
                email = line.split(":", 1)[1]
                contact.setdefault('Emails', []).append(email)
            elif line.startswith("END:VCARD"):
                flush_contact()
                contact = {}

    return contacts

def export_to_csv(contacts, output_file):
    keys = ['Full Name', 'Phone Number', 'Email']
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for contact in contacts:
            writer.writerow(contact)

# === CONFIGURATION ===
vcf_input = "4.vcf"          # Your input VCF file
csv_output = "contacts_export.csv"  # Desired output

# === EXECUTION ===
contacts = parse_vcf(vcf_input)
export_to_csv(contacts, csv_output)

print(f"Exported {len(contacts)} rows to {csv_output}")
