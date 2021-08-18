import sys
import os

import pandas as pd


if len(sys.argv) < 3:
    print("ERROR: you should specify args:")
    print("  #1 GWAS summary statistics file, ")
    print("  #2 rsIDs file (generated with get_rsIDs_from_ChrBR script, same n of lines as #1)")
    print("  #3 output file name, i.e. GWAS SS file with rsIDs column")
    exit(1)

# GWAS_FILE has to be in a tabular tab-sep format, sorted by Chr and BP
GWAS_FILE = sys.argv[1]
RSID_FILE = sys.argv[2]
OUT_FILE = sys.argv[3]


def file_exists(path: str):
    return os.path.isfile(path)

if not file_exists(GWAS_FILE):
    print(f"ERROR: provided gwas file doesn't exist: {GWAS_FILE}")
    exit(1)

if not file_exists(RSID_FILE):
    print(f"ERROR: provided rsIDs file doesn't exist: {RSID_FILE}")
    exit(1)


GWAS_df = pd.read_csv(GWAS_FILE, sep="\t")

RSID_df = pd.read_csv(RSID_FILE, sep="\t")

GWAS_df_len = len(GWAS_df)
RSID_df_len = len(RSID_df)

if (GWAS_df_len != RSID_df_len):
    print("ERROR: instantiated pandas dfs for GWAS SS and rsIDs files are of not equal length: ")
    exit(2)

missing_rsIDs = RSID_df.loc[RSID_df['kukrsID'] == '-'].count()['kukrsID']

# the first two columns 

df = pd.DataFrame()

for i in range(0, 2):
    col = GWAS_df.columns[i]
    df[col] = GWAS_df[col]

df['kukrsID'] = RSID_df['kukrsID']

for i in range(2, len(GWAS_df.columns)):
    col = GWAS_df.columns[i]
    df[col] = GWAS_df[col]


df.to_csv(OUT_FILE, index=False, sep="\t")

print(f"concatenated GWAS SS file with the file with restored rsID at: \"{OUT_FILE}\"")

