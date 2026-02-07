import pandas as pd

# File paths
excel1_path = "/Users/kgangwan/OneDrive - St. Jude Children's Research Hospital/oncology projects/ASH/latest datasets/ash.sample.CLL.xlsx"
excel2_path = "/Users/kgangwan/OneDrive - St. Jude Children's Research Hospital/oncology projects/ASH/latest datasets/Metadata_batch2_iimay26-AML-remaining.xlsx"
updated_excel1_path = "/Users/kgangwan/OneDrive - St. Jude Children's Research Hospital/oncology projects/ASH/latest datasets/ash.sample.CLL.xlsx"
unmatched_samples_path = "/Users/kgangwan/OneDrive - St. Jude Children's Research Hospital/oncology projects/ASH/latest datasets/unmatched_samples.xlsx"
tab_delimited_path = "/Users/kgangwan/OneDrive - St. Jude Children's Research Hospital/oncology projects/ASH/latest datasets/cll.sample.txt"

# Load the Excel files into pandas DataFrames
excel1 = pd.read_excel(excel1_path)
excel2 = pd.read_excel(excel2_path)

# Drop rows where MolecularSubtype is "T-other"
excel1 = excel1[excel1["MolecularSubtype"] != "T-other"]

# Rename columns in excel2 to match excel1 for easier merging
excel2.rename(columns={"Array_id": "sample_name", "gender": "Sex", "Short Subtype": "Short_Subtype"}, inplace=True)

# Map gender values (m -> Male, f -> Female)
gender_map = {"m": "Male", "f": "Female"}
excel2["Sex"] = excel2["Sex"].map(gender_map)

# Perform the matching and update the columns in excel1
# Using 'left' merge to keep all rows from excel1 and add matching data from excel2
merged = excel1.merge(excel2[["sample_name", "Short_Subtype", "subtype", "Sex"]], on="sample_name", how="left")

# Update the AML_Subtype, ICC2022, and Sex columns in excel1 using combine_first
# combine_first fills NaN values in the first Series with values from the second Series
merged["AML_Subtype"] = merged["Short_Subtype"].combine_first(merged["AML_Subtype"])
merged["ICC2022"] = merged["subtype"].combine_first(merged["ICC2022"])
# Sex_x comes from excel1, Sex_y from excel2. Prioritize Sex_y (from excel2) if available, else use Sex_x
merged["Sex"] = merged["Sex_y"].combine_first(merged["Sex_x"])

# Drop unnecessary intermediate columns created during the merge
updated_excel1 = merged.drop(columns=["Short_Subtype", "subtype", "Sex_x", "Sex_y"])

# Replace "St Jude" with "St. Jude" in the Institute column for consistency
updated_excel1["Institute"] = updated_excel1["Institute"].replace("St Jude", "St. Jude")

# Define the list of desired columns
desired_columns = [
    "sample_name", "Sex", "AgeAtDiagnosis", "MolecularSubtype", "PairedWGS", "PairedWES",
    "TumorWGS", "TumorWES", "WBC", "NCIStandard_Risk_High_Risk", "Institute", "Project",
    "Diagnosis", "Karyotype", "AML_Subtype", "ICC2022", "WHO2022", "hasSNVIndel",
    "hasCNV", "RNAseq", "Molecular_subgroup", "ETP_status", "Reviewed_driver_TALL",
    "Reviewed_genetic_subtype_TALL"
]

# Select only the desired columns, maintaining their order
# Use .reindex() to ensure the order and handle any missing columns gracefully (they will be NaN)
updated_excel1 = updated_excel1.reindex(columns=desired_columns)

# Save the updated excel1 to a new Excel file
updated_excel1.to_excel(updated_excel1_path, index=False)

# Save the updated excel1 to a tab-delimited file
updated_excel1.to_csv(tab_delimited_path, sep="\t", index=False)

# Find unmatched samples from excel2 (samples in excel2 that are not in excel1)
unmatched_samples = excel2[~excel2["sample_name"].isin(excel1["sample_name"])]

# Save the unmatched samples to a new Excel file
unmatched_samples.to_excel(unmatched_samples_path, index=False)

print("Excel and tab-delimited files updated successfully!")
