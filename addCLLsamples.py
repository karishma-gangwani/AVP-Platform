import pandas as pd

# File paths
excel1_path = "/Users/kgangwan/OneDrive - St. Jude Children's Research Hospital/oncology projects/ASH/latest datasets/ash.sample.xlsx"
excel2_path = "/Users/kgangwan/OneDrive - St. Jude Children's Research Hospital/oncology projects/ASH/latest datasets/CLL/Metadata_batch3_CLL.xlsx"
output_path = "/Users/kgangwan/OneDrive - St. Jude Children's Research Hospital/oncology projects/ASH/latest datasets/ash.sample.CLL.xlsx"

# Load Excel files
excel1 = pd.read_excel(excel1_path)
excel2 = pd.read_excel(excel2_path)

# Rename columns in excel2 to match excel1
excel2 = excel2.rename(columns={
    "Array_id": "sample_name",
    "disease": "Diagnosis",
    "age": "AgeAtDiagnosis",
    "gender": "Sex",
    "caryotype 1": "Karyotype"
})

# Map 'm' to 'Male' and 'f' to 'Female' in the Sex column of excel2
excel2['Sex'] = excel2['Sex'].map({'m': 'Male', 'f': 'Female'})

# Combine both datasets
combined = pd.concat([excel1, excel2], ignore_index=True)

# Set 'Institute' to 'MLL' for rows where 'Diagnosis' is 'CLL'
combined.loc[combined['Diagnosis'] == 'CLL', 'Institute'] = 'MLL'

# Save the combined dataset to a new Excel file
combined.to_excel(output_path, index=False)

print(f"Combined file saved to {output_path}")