# Define columns to keep
columns_to_keep = [
    'sample_name', 'Sex', 'AgeAtDiagnosis', 'MolecularSubtype', 'PairedWGS', 'PairedWES', 'TumorWGS', 'TumorWES', 'WBC',
    'NCIStandard_Risk_High_Risk', 'Institute', 'Project', 'Diagnosis', 'Karyotype', 'AML_Subtype', 'WHO2022', 'ICC2022',
    'hasSNVIndel', 'hasCNV', 'RNAseq', 'Molecular_subgroup', 'ETP_status',
    'Reviewed_driver_TALL', 'Reviewed_genetic_subtype_TALL'
]

def parse_sample_file(filename, columns_to_keep):
    sample_dict = {}
    with open(filename, 'r') as f:
        header = f.readline().strip().split('\t')
        col_indices = [header.index(col) for col in columns_to_keep if col in header]
        col_names = [header[i] for i in col_indices]
        for line in f:
            values = line.strip().split('\t')
            if not values or not values[0]:
                continue
            sample_name = values[0]
            sample_dict[sample_name] = {
                col_names[i]: values[col_indices[i]] if col_indices[i] < len(values) else ''
                for i in range(len(col_indices))
            }
    return sample_dict

def is_blank(val):
    return val.strip() == '' or val.strip().lower() == 'not available'

# Parse input files
ash_sample_dict = parse_sample_file('ash.sample', columns_to_keep)
cll_aml_dict = parse_sample_file('ash.sample.CLL.AML_ii.txt', columns_to_keep)

# Merge logic
final_dict = {}
all_samples = set(ash_sample_dict.keys()) | set(cll_aml_dict.keys())

for sample in all_samples:
    merged = {}
    ash_data = ash_sample_dict.get(sample, {})
    cll_data = cll_aml_dict.get(sample, {})
    for key in columns_to_keep:
        val_ash = ash_data.get(key, '')
        val_cll = cll_data.get(key, '')
        if is_blank(val_ash) and not is_blank(val_cll):
            merged[key] = val_cll
        else:
            merged[key] = val_ash
    final_dict[sample] = merged

# Write output file
with open('ash.sample', 'w') as out:
    out.write('\t'.join(columns_to_keep) + '\n')
    for sample in sorted(final_dict.keys()):
        row = [final_dict[sample].get(col, '') for col in columns_to_keep]
        out.write('\t'.join(row) + '\n')

print("Final merged output written to ash.output.txt")