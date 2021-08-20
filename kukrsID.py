import sys
import json
import os
from subprocess import call
import inspect
import time


# # # # # # # # # # # # #
#      ASSUMPTIONS      #
# # # # # # # # # # # # #
#
# 1. GWAS SS file has a header on the first line
# 2. GWAS SS file has columns:
#    #1 Chromosome   [an integer]
#    #2 Base pair position   [an integer]
# 3. Restoring rsid only from Chr:BP
# 4. using dbSNPs file in vcf.gz format
#


# this config should define intermediate file names
CONFIG_JSON = sys.argv[1]



def file_exists(path: str):
    return os.path.isfile(path)

if not file_exists(CONFIG_JSON):
    print(f"ERROR: provided CONFIG_JSON file doesn't exist: \"{CONFIG_JSON}\"")
    exit(1)


CONFIG = json.load(open(CONFIG_JSON,))

the_dir = os.path.dirname(inspect.getfile(inspect.currentframe())) or os.getcwd() # type: ignore

lib_dir = the_dir +"/lib"

sort_GWASSS_by_ChrBP = lib_dir+"/sort_GWASSS_by_ChrBP.py"
get_rsIDs_from_ChrBP = lib_dir+"/get_rsIDs_from_ChrBP_v6.1.py"
cat_GWASSS_and_rsIDs_columns = lib_dir+"/cat_GWASSS_and_rsIDs_columns.py"


##### 1 #####
print('=== Step 1/3: Sort GWAS SS file by Chr and BP ===')
start_time = time.time()
ec = call(["python3",
           sort_GWASSS_by_ChrBP,
           CONFIG[0]["i_GWAS_SS_file"],
           CONFIG[0]["o_sorted_GWAS_SS_file"],
           str(CONFIG[0]["i_Chr_col_index"]),
           str(CONFIG[0]["i_BP_col_index"]),
           ])
print("--- Step 1/3 finished in %s seconds ---" % (time.time() - start_time))
if ec != 0:
    print(f"ERROR: sort_GWASSS_by_ChrBP program finished with exit code: {ec}")
    exit(2)


##### 2 #####
print('=== Step 2/3: Generate rsID column and save it to a file ===')
start_time = time.time()
ec = call(["python3",
           get_rsIDs_from_ChrBP,
           CONFIG[1]["i_sorted_GWAS_SS_file"],
           CONFIG[1]["o_rsIDs_file"],
           str(CONFIG[1]["i_Chr_col_index"]),
           str(CONFIG[1]["i_BP_col_index"]),
           CONFIG[1]["i_dbSNPs_file"],
           ])
print("--- Step 2/3 finished in %s seconds ---" % (time.time() - start_time))
if ec != 0:
    print(f"ERROR: get_rsIDs_from_ChrBP program finished with exit code: {ec}")
    exit(3)


##### 3 #####
print('=== Step 3/3: Concatenate columns of the sorted GWAS SS file and rsID file ===')
start_time = time.time()
ec = call(["python3",
           cat_GWASSS_and_rsIDs_columns, 
           CONFIG[2]["i_sorted_GWAS_SS_file"],
           CONFIG[2]["i_rsIDs_file"],
           CONFIG[2]["o_GWAS_SS_with_rsIDs_file"],
           ])
print("--- Step 3/3 finished in %s seconds ---" % (time.time() - start_time))
if ec != 0:
    print(f"ERROR: cat_GWASSS_and_rsIDs_columns program finished with exit code: {ec}")
    exit(4)


print('see resulting file at:')
print(f'"{CONFIG[2]["o_GWAS_SS_with_rsIDs_file"]}"')


