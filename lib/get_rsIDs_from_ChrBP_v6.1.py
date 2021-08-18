import sys
import os
import gzip
import io

from chr_order import category_chr as CHRs_nums


# # # # # # # # # # # # #
#      ASSUMPTIONS      #
# # # # # # # # # # # # #
# 
# 1. GWAS SS file has a header on the first line
# 2. GWAS SS file has Chr and BP columns
# 3. Chr are coded without "chr" prefix
# 4. GWAS SS file is sorted by Chr and BP in accord to the order in the dbSNP file
# 5. Querying rsid only from Chr:BP
# 6. using dbSNP vcf.gz file format
# 

##########################################
###                                    ###
###                HEAD                ###
###                                    ###
##########################################

if len(sys.argv) < 6:
    print("ERROR: you should specify args:")
    print("   #1: GWAS summary statistics file sorted by Chr and BP columns in accord to the order in the dbSNP file")
    print("   #2: output path of the rsID column file to be generated")
    print("   #3: Chr column index")
    print("   #4: BP column index")
    print("   #5: dbSNP file in vcf.gz")
    exit(1)

# GWAS_FILE has to be in a tabular spaces- or tab-sep format, sorted by Chr and BP
GWAS_FILE = sys.argv[1]
print('input GWAS SS file: ', f'"{GWAS_FILE}"')

RSID_FILE = sys.argv[2]

Chr_col_i = int(sys.argv[3])
BP_col_i = int(sys.argv[4])

# SNPs_FILE has to be in vcf format, sorted by Chr and BP
SNPs_FILE = sys.argv[5]


def file_exists(path: str):
    return os.path.isfile(path)

if not file_exists(SNPs_FILE):
    print(f"ERROR: provided dbSNPs file doesn't exist: \"{SNPs_FILE}\"")
    exit(1)

if not file_exists(GWAS_FILE):
    print(f"ERROR: provided GWAS SS file doesn't exist: \"{GWAS_FILE}\"")
    exit(1)




def read_dbSNPs_data_row(FILE_o: io.TextIOWrapper):
    line = FILE_o.readline()
    words = line.split()
    return (
        words[0][3:], # bc in SNPs_file it chromosome number is prepended with "chr"
        int(words[1]), # BP
        words[2] # rsID
    )

def read_GWASSS_data_row(FILE_o: io.TextIOWrapper):
    line = FILE_o.readline()
    words = line.split()
    return words[Chr_col_i], int(words[BP_col_i])


# for debugging
# outputs the debug message
# may take an integer as an input, then it will skip this number of lines from SNPs_FILE
def read(msg: str):
    try:
        num = int(input(msg))
        for i in range(num):
            SNPs_FILE_o.readline()
    except ValueError:
        pass



##########################################
###                                    ###
###                BODY                ###
###                                    ###
##########################################

GWAS_FILE_o = open(GWAS_FILE, 'r')
SNPs_FILE_o_gz: io.RawIOBase = gzip.open(SNPs_FILE, 'r')  # type: ignore # GzipFile and RawIOBase _are_ in fact compatible
SNPs_FILE_o = io.TextIOWrapper(io.BufferedReader(SNPs_FILE_o_gz))
RSID_FILE_o = open(RSID_FILE, 'w')

i = 0
i_res = 0


"""
SNPs_FILE, being a VCF file, starts with comment lines at the beginning. Comments start with ##
Then comes a header, starts with #
after the header comes the dataframe table

THIS codeblock skips all the comment lines,
then reads the header line before going to the next loop.
this prevents putting more conditions into the loop
"""
SNPs_line = SNPs_FILE_o.readline()
while SNPs_line.startswith('##'):
    SNPs_line = SNPs_FILE_o.readline()

# skips the first line (header), and starts with the second line (first data line)
GWAS_FILE_o.readline()
i += 1
chr_gwas, bp_gwas = read_GWASSS_data_row(GWAS_FILE_o)

# writes the header for the 1-column output file
RSID_FILE_o.write("kukrsID\n")



# fills the output file with rsIDs
try:
    while True:
        chr_snps, bp_snps, rsid = read_dbSNPs_data_row(SNPs_FILE_o)

        if CHRs_nums.index(chr_gwas) == CHRs_nums.index(chr_snps):
            if bp_snps < bp_gwas:
                continue
            elif bp_gwas == bp_snps:
                RSID_FILE_o.write(rsid+'\n')
                i_res += 1
                chr_gwas, bp_gwas = read_GWASSS_data_row(GWAS_FILE_o)
                i += 1
            else: #bp_snps > bp_gwas:
                RSID_FILE_o.write('-\n')
                chr_gwas, bp_gwas = read_GWASSS_data_row(GWAS_FILE_o)
                i += 1
        elif CHRs_nums.index(chr_snps) > CHRs_nums.index(chr_gwas):
            RSID_FILE_o.write('-\n')
            chr_gwas, bp_gwas = read_GWASSS_data_row(GWAS_FILE_o)
            i += 1

except Exception as e:
    if isinstance(e, IndexError) or isinstance(e, EOFError):
        # it reached the end of an either file
        pass
    else:
        print(f'An error occured on line {i} of the GWAS SS file (see below)')
        raise e


SNPs_FILE_o.close()
GWAS_FILE_o.close()
RSID_FILE_o.close()


print(f"successfully restored {i_res} rsIDs based on provided dbSNP file: '{SNPs_FILE}'")
