#PacbioToSRA
This repo contains scripts, instructions, and examples on preparing PacBio sequence data for data submission to the SRA. 

## Instructions
1. Register project and samples
2. Setup script's environment
3. Run the script
4. Email spreadsheet to NCBI


##Step 1. Register project and samples

    Go to https://submit.ncbi.nlm.nih.gov/ and register your Bioproject
    Go to https://submit.ncbi.nlm.nih.gov/ and register your Biosample


##Step 2. Prepare script's environment
####Install Aspera software:

*  download and install the linux version of aspera-connect that contains the ascp command (http://downloads.asperasoft.com/en/downloads/50)
*  Add Aspera's ascp command to your $PATH. Example:
```
    $ export PATH='/path/to/ascp/command':$PATH
```

####Setup virtual environment:

```
$ virtualenv virtualenv_PacbioToSRA
$ source virtualenv_PacbioToSRA/bin/activate
$ pip install -r requirements.txt
```


##Step 3. Run the script
####Usage:
```
$ bin/send_to_ncbi.py --bioproject_accession=BIOPROJECT_ACCESSION --biosample_accession=BIOSAMPLE_ACCESSION --input_fofn=INPUT_FOFN_FILE --ncbi_username=NCBI_USERNAME --ncbi_ssh_key_file=SSH_KEY_FILE [--excel_output_file=EXCEL_OUTPUT_FILE]
```
*  NCBI_USERNAME is the username that ncbi assigns to your institution (get this from info@ncbi.nlm.nih.gov)
*  SSH _KEY _FILE is the ssh key file that you generated for your institution (http://www.ncbi.nlm.nih.gov/books/NBK180157/)
*  For additional help on the script, type: ```$ bin/send_to_ncbi.py --help```


####Example:
```
$ bin/send_to_ncbi.py --bioproject_accession=PacBioProject1 --biosample_accession=PacBioSample1 --input_fofn=input.fofn --ncbi_username=myusername --ncbi_ssh_key_file=../../.ssh/id_rsa  --excel_output_file=my_spreadsheet.xlsx
```

##Step 4. Email spreadsheet to NCBI
Email (info@ncbi.nlm.nih.gov) and attach the spreadsheet to the email. 

