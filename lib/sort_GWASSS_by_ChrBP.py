import sys

from chr_order import category_chr_order

import pandas as pd


if len(sys.argv) < 5: # first, 0th arg is the name of this script
    print("ERROR: you should specify args:")
    print("  #1 GWAS summary statistics file, ")
    print("  #2 output file name, i.e. GWAS SS file, sorted by Chr and BP")
    print("  #3 Chr column index")
    print("  #4 BP column index")
    exit(1)

# GWAS_FILE has to be in a tabular tab-sep format
GWAS_FILE = sys.argv[1]
SORTED_FILE = sys.argv[2]

Chr_col_i = int(sys.argv[3])
BP_col_i = int(sys.argv[4])

GWAS_df = pd.read_csv(GWAS_FILE, sep="\t")


# set order for the data type of Chr column
GWAS_df[GWAS_df.columns[Chr_col_i]] = GWAS_df[GWAS_df.columns[Chr_col_i]].astype(str).astype(category_chr_order) # type: ignore
GWAS_df[GWAS_df.columns[BP_col_i]] = GWAS_df[GWAS_df.columns[BP_col_i]].astype('Int64')



GWAS_df.sort_values(
    by=[GWAS_df.columns[Chr_col_i], GWAS_df.columns[BP_col_i]],
    ascending=[True, True],
    inplace=True
)  # type: ignore

GWAS_df.to_csv(SORTED_FILE, index=False, sep="\t")

