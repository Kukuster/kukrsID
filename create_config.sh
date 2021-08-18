#!/usr/bin/env bash

#$1 - GWAS SS file with missing rsID, with 1st col - chr, 2nd col - BP

create_json_for_restore_rsID(){

    local file="$(cd "$(dirname "$1")"; pwd)/$(basename "$1")" # fullpath
    local file_noext="${file%.*}"
    local json_file="${file}.json"

    echo '[
        {
            "i_GWAS_SS_file": "'$file'",
            "o_sorted_GWAS_SS_file": "'$file_noext'_asc.tsv",
            "i_Chr_col_index": 0,
            "i_BP_col_index": 1
        },
        {
            "i_sorted_GWAS_SS_file": "'$file_noext'_asc.tsv",
            "o_rsIDs_file": "'$file_noext'_asc_kukrsIDs.tsv",
            "i_Chr_col_index": 0,
            "i_BP_col_index": 1,
            "i_dbSNPs_file": "<enter path to the dbSNP file in vcf.gz format>"
        },
        {
            "i_sorted_GWAS_SS_file": "'$file_noext'_asc.tsv",
            "i_rsIDs_file": "'$file_noext'_asc_kukrsIDs.tsv",
            "o_GWAS_SS_with_rsIDs_file": "'$file_noext'_asc_with-kukrsIDs.tsv"
        }
    ]

' > "$json_file"
    echo "$json_file"

}

create_json_for_restore_rsID "$1"
