# kukrsID
Restore missing or old rsID column for a GWAS summary statistics file


## Dependencies
  - python 3.7+
  - pandas 1.3+ (1.2.3 has a bug with sorting)
  - bash 4+

## Usage
  1. clone this repo
  2. Download the latest full dbSNP file in vcf.gz format for the corresponding build (e.g. `dbSNP151_GRCh37.vcf.gz`, `dbSNP154_GRCh38.vcf.gz`)
  3. Run `create_config.sh` to create a config file for the program:
      - `bash create_config.sh diabetes_GWAS_ss.tsv` or `. create_config.sh diabetes_GWAS_ss.tsv`
  4. Edit the generated config file `diabetes_GWAS_ss.tsv.json` to make sure you have:
      - indices of columns for chromosome and base pair position in the config file corresponding to these columns in your summary statistics file `diabetes_GWAS_ss.tsv`
      - path to the dbSNP file
      - filenames for intermediate and the resulting file not conflicting with your existing files
  5. Run `kukrsID`, passing config file:
      - `python3 kukrsID.py diabetes_GWAS_ss.tsv.json`

## Use cases
   - GWAS summary statistics file is missing "rsID" column
   - GWAS summary statistics file is old and has old rsIDs (that were merged into the newer ones)


## Example output:
```
python3 ~/kukrsID/add_missing_rsID_column.py continuous-20508-both_sexes.tsv.json 
=== Step 1/3: Sort GWAS SS file by Chr and BP ===
--- Step 1/3 finished in 394.9851267337799 seconds ---
=== Step 2/3: Generate rsID column and save it to a file ===
input GWAS SS file:  "/home/kukubuntu/Summary Stats to Fix/data/test_kukrsID_repo/continuous-20508-both_sexes_relevantColumns_asc.tsv"
successfully restored 28940544 rsIDs based on provided dbSNP file: '/media/kukubuntu/Samsung_T5/dbSNP151_GRCh37.vcf.gz'
--- Step 2/3 finished in 3006.899871110916 seconds ---
=== Step 3/3: Concatenate columns of the sorted GWAS SS file and rsID file ===
concatenated GWAS SS file with the file with restored rsID at: "/home/kukubuntu/Summary Stats to Fix/data/test_kukrsID_repo/continuous-20508-both_sexes_asc_with-kukrsIDs.tsv"
--- Step 3/3 finished in 348.7267150878906 seconds ---
see resulting file at:
"/home/kukubuntu/Summary Stats to Fix/data/test_kukrsID_repo/continuous-20508-both_sexes_asc_with-kukrsIDs.tsv"
```

