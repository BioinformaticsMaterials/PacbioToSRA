#PacbioToSRA
This repo contains scripts, instructions, and examples on preparing PacBio sequence data for data submission to the SRA. 

## Instructions
1. Register project and samples
2. Prepare script's virtual environment
3. Run the script
4. Email spreadsheet to NCBI


##Step 1. Register project and samples

    Go to https://submit.ncbi.nlm.nih.gov/ and register your Bioproject
    Go to https://submit.ncbi.nlm.nih.gov/ and register your Biosample


##Step 2. Prepare script's virtual environment
```
$ virtualenv virtualenv_PacbioToSRA
$ source virtualenv_PacbioToSRA/bin/activate
$ pip install -r requirements.txt
```


##Step 3. Run the script
Usage:

```
$ bin/send_to_ncbi.py --bioproject_accession=BIOPROJECT_ACCESSION --biosample_accession=BIOSAMPLE_ACCESSION --input_fofn=INPUT_FOFN_FILE --ncbi_username=NCBI_USERNAME --ncbi_ssh_key_file=SSH_KEY_FILE [--excel_output_file=EXCEL_OUTPUT_FILE]
```

Example:

```
$ bin/send_to_ncbi.py --bioproject_accession=PacBioProject1 --biosample_accession=PacBioSample1 --input_fofn=input.fofn --ncbi_username=myusername --ncbi_ssh_key_file=../../.ssh/id_rsa  --excel_output_file=my_spreadsheet.xlsx
```

##Step 4. Email spreadsheet to NCBI
Email (info@ncbi.nlm.nih.gov) and attach the spreadsheet to the email. 

