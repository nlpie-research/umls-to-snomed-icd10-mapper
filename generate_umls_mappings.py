import os
import csv
import json
from collections import defaultdict
from typing import Dict, List, Tuple

# Constants
UMLS_KB_PATH = "/path/to/your/directory/"
MRCONSO_FILE = os.path.join(UMLS_KB_PATH, "MRCONSO.RRF")
MRREL_FILE = os.path.join(UMLS_KB_PATH, "MRREL.RRF")

def generate_mappings(method: str) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    """
    Generate mappings between UMLS CUIs and SNOMED CT and ICD-10 codes using the specified method.

    Args:
        method (str): The method to use for generating mappings. Must be one of "RO", "PAR_CHD", or "EXACT".

    Returns:
        A tuple of two dictionaries. The first dictionary maps UMLS CUIs to SNOMED CT codes, and the second
        dictionary maps UMLS CUIs to ICD-10 codes.


    Note: The RO and PAR_CHD methods will result in more extensive mappings because they will include the exact 
    matches from the MRCONSO file and additional mappings based on the relationships found in the MRREL file. 
    The RO method will update the dictionaries with mappings that have a "RO" (Related To) relationship, while 
    the PAR_CHD method will update the dictionaries with mappings that have either a 
    "PAR" (Parent Of) or a "CHD" (Child Of) relationship.
    """

    cui_to_snomed = defaultdict(list)
    cui_to_icd10 = defaultdict(list)

    # Read MRCONSO file and populate the dictionaries
    with open(MRCONSO_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in reader:
            cui = row[0]
            sab = row[11]  # Abbreviation for the source of the code
            code = row[13]  # Code assigned by the source

            # Check if the code source is SNOMED CT or ICD-10
            if sab == "SNOMEDCT_US":
                if code not in cui_to_snomed[cui]:  # Add this line to avoid duplication
                    cui_to_snomed[cui].append(code)
            elif sab == "ICD10CM":
                if code not in cui_to_icd10[cui]:  # Add this line to avoid duplication
                    cui_to_icd10[cui].append(code)

    # Read MRREL file and update the dictionaries based on the selected method
    if method in ["RO", "PAR_CHD"]:
        with open(MRREL_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter="|", quoting=csv.QUOTE_NONE)
            for row in reader:
                cui1 = row[0]
                cui2 = row[4]
                rel = row[7]  # Abbreviation for the relationship between the concepts

                # Check if the relationship is selected and both CUIs are in the respective dictionaries
                if ((method == "RO" and rel == "RO") or
                    (method == "PAR_CHD" and (rel == "PAR" or rel == "CHD"))) and cui1 in cui_to_snomed and cui2 in cui_to_icd10:
                    for code in cui_to_snomed[cui2]: 
                        if code not in cui_to_snomed[cui1]:  # avoid duplication
                            cui_to_snomed[cui1].append(code)
                    for code in cui_to_icd10[cui2]:  
                        if code not in cui_to_icd10[cui1]:  # avoid duplication
                            cui_to_icd10[cui1].append(code)

    return dict(cui_to_snomed), dict(cui_to_icd10)

def save_mappings(method: str):
    """
    Having generate mappings between UMLS CUIs and SNOMED CT and ICD-10 codes using the specified method, save the
    mappings to JSON files.

    Args:
        method (str): The method to use for generating mappings. Must be one of "RO", "PAR_CHD", or "EXACT".

    Returns:
        None.

    Raises:
        FileNotFoundError: If the MRCONSO.RRF or MRREL.RRF files cannot be found.

    Example Usage:
        >>> save_mappings("PAR_CHD")

    The function calls the `generate_mappings` function with the specified method and saves the resulting
    dictionaries to two separate JSON files. The JSON files will be named "cui_to_snomed_METHOD.json" and
    "cui_to_icd10_METHOD.json", where METHOD is the specified method ("RO", "PAR_CHD", or "EXACT").
    """
    
    cui_to_snomed_list, cui_to_icd10_list = generate_mappings(method)
    snomed_filename = f"cui_to_snomed_{method}.json"
    icd10_filename = f"cui_to_icd10_{method}.json"
    with open(snomed_filename, "w") as snomed_file, open(icd10_filename, "w") as icd10_file:
        json.dump(cui_to_snomed_list, snomed_file)
        json.dump(cui_to_icd10_list, icd10_file)

# Example usage:
method = "EXACT"  # Choose method: "RO", "PAR_CHD", or "EXACT"
save_mappings(method)
