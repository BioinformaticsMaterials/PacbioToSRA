#PacbioToSRA
This repo contains scripts, instructions, and examples on preparing PacBio sequence data for data submission to the SRA. 

## Instructions
1. Register project and samples
2. Setup script's environment
3. Run the script
4. Update spreadsheet and email it to NCBI


##Step 1. Register project and samples

    Go to https://submit.ncbi.nlm.nih.gov/ and register your Bioproject
    Go to https://submit.ncbi.nlm.nih.gov/ and register your Biosample


##Step 2. Prepare script's environment
####Setup virtual environment:

```
(go to the root directory of this repo)
$ virtualenv virtualenv_PacbioToSRA
$ source virtualenv_PacbioToSRA/bin/activate
$ pip install -r requirements.txt
```


##Step 3. Run the script
####Usage:
```
$ bin/pacb_ncbi --help
Usage: pacb_ncbi [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  calc_upload_size              Calculates the total size of the data that...
  create_excel_file             Creates the Excel file that contains the...
  create_excel_file_and_upload  Creates the Excel file that contains the...
  upload                        Uploads the datasets in the input.fofn file...
```
####Example:
```
$ bin/pacb_ncbi create_excel_file_and_upload -i /path/to/input.fofn -p bioproject1 -s biosample1 -x my_sra.xlsx -u ncbi_username -k /path/to/ssh/file
```
####Notes:
*  NCBI_USERNAME is the username that ncbi assigns to your institution (get this from info@ncbi.nlm.nih.gov)
*  SSH _KEY _FILE is the ssh key file that you generated for your institution (http://www.ncbi.nlm.nih.gov/books/NBK180157/)
* To get additional help, type:  
	```$ bin/pacb_ncbi <subcommand> --help```  
	ex:  
	```$ bin/pacb_ncbi create_excel_file_and_upload --help```  
	```$ bin/pacb_ncbi create_excel_file --help```  
	```$ bin/pacb_ncbi upload --help```  

##Step 4. Update spreadsheet and email it to NCBI
*  Update the spreadsheet with any additional information.
*  Email (info@ncbi.nlm.nih.gov) and attach the spreadsheet to the email. 

