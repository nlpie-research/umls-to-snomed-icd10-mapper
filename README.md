# UMLS to SNOMED CT and ICD-10 Mapper

This Python script maps UMLS codes to SNOMED CT and ICD-10 codes using the UMLS Metathesaurus. The program generates JSON files containing the mappings based on one of the following methods: exact match (``EXACT``), broad relations (``RO``), or parent-child hierarchy relations (``PAR_CHD``). The output will consist of two JSON files for each method, one for SNOMED CT mappings and another for ICD-10 mappings.

## Prerequisites

To run this program, you need to request access to the UMLS Metathesaurus from the [National Library of Medicine](https://www.nlm.nih.gov/research/umls/index.html). Once you have access, download the `MRCONSO.RRF` and `MRREL.RRF` files and place them in a directory on your local machine. For ``EXACT`` matches you would only need `MRCONSO.RRF`.

## Configuration

In the umls_mapping_tool.py file, set the UMLS_KB_PATH variable to the path of the directory where you have placed the `MRCONSO.RRF` and `MRREL.RRF` files:

```python
UMLS_KB_PATH = "/path/to/your/directory/"
```

## Usage

To run the script, execute the `umls_mapping_tool.py` file in your Python environment:

```bash
python umls_mapping_tool.py
```

By default, the script will use the ``EXACT`` mapping method. To change the mapping method, modify the method variable in the script:

```python
method = "RO"  # Choose method: "RO", "PAR_CHD", or "EXACT"
```

The script will generate two JSON files for the specified method. For example, if you choose the ``EXACT`` method, the output files will be named ``cui_to_snomed_EXACT.json`` and ``cui_to_icd10_EXACT.json``.

## Questions and Support

For questions or support, please [send an email](mailto:info@nlpie.com "Contact us") to the NLPie team.
