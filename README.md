#PacbioToSRA
This repo contains scripts, instructions, and examples on preparing PacBio sequence data for data submission to the SRA. 

## Instructions
1. Run the script
2. Register project and samples
3. Manually create excel spreadsheet
4. Upload using aspera
5. Email NCBI


##Step 1. Run the script
```
$ python PacbioToSRA.py input.fofn
```

###Inputs: 
  1. input.fofn

###Outputs:
  1. sra_data.txt - sample information for data submission (from metadata.xml)
  2. file_info.csv - md5sums of of files for data submission
  3. aspera.fofn - full path to all files that need to be uploaded to NCBI SRA


##Step 2. Register project and samples

    Go to https://submit.ncbi.nlm.nih.gov/ and register your Bioproject
    Go to https://submit.ncbi.nlm.nih.gov/ and register your Biosample

##Step 3. Manually create excel spreadsheet
Open SRA_submission.xlsx and paste the contents of sra_data.txt to the "library_ID" column of the spreadsheet.  Fill in the BioProject and BioSamples that you created in step 2 for each entry. Open file_info.csv, and paste the contents as a new sheet in SRA_submission.xlsx

##Step 4. Upload using aspera
``` 
$ screen
$ for i in $(cat aspera.fofn); 
  do aspera/connect/bin/ascp -i xxxx_sshkeyformyinstitution.openssh -QT -l200m -k1 $i asp-xxxx_myinstitution@upload.ncbi.nlm.nih.gov:incoming;
  done;
```

* do this in a screen session because it may take a long time
* download the linux version of aspera-connect that contains the ascp command (http://downloads.asperasoft.com/en/downloads/50
* xxxx_sshkeyformyinstitution is the ssh key file that you generated for your institution (http://www.ncbi.nlm.nih.gov/books/NBK180157/)
* asp-xxxx_myinstitution is the username that ncbi assigns to your institution (get this from info@ncbi.nlm.nih.gov)


##Step 5. Email NCBI
Email (info@ncbi.nlm.nih.gov) and attach the spreadsheet to the email. 

