import argparse
import pandas as pd
import csv
import os
import numpy as np
from neuroHarmonize import harmonizationLearn

#In the terminal, you would run the script like this:
#python3 harmonize_CorticalThickness.py --data /path/to/data.csv --dx DiagnosisType --covariates /path/to/covariates.csv --output_dir /path/to/output --atlas YourAtlasChoice

def harmonizeCorticalThickness(data, dx, covariates, output_dir, atlas):
    """
    Run ComBat (neuroHarmonize package) on Cortical Thickness data

    Parameters:
    ---------
    data : str
        Path to a csv with 'PIDN' columns and neuroimaging data separated by 
        the ROI columns to correct with ComBat (e.g., cortical thickness data).
    covariates : str
        Path to a csv with covariates. The mandatory covariate is SITE. 
        Optional ones include AGE_M & SEX.
    output_dir : str
        Path to the desired output directory.
    atlas : str
        Name of the atlas being used.

    Returns:
    -------
    None
        Writes a csv with the corrected values to a specific directory locally.
    """

    # Load data
    modelData = pd.read_csv(covariates).drop('PIDN', axis=1)
    structData = pd.read_csv(data)
    structData_matrix = structData.drop('PIDN', axis=1).values

    # Run ComBat (neuroHarmonize) on the data
    cort_model, cort_data_adj = harmonizationLearn(structData_matrix, modelData)

    # Format the corrected data for output
    harmonized_cortical_data = pd.DataFrame(cort_data_adj, columns=structData.columns[1:])  # Assuming PIDN is the first column
    harmonized_cortical_data.insert(0, 'PIDN', structData['PIDN'])  # Add PIDN to the front

    # Save the corrected data to the desired directory
    output_filename = f"Harmonized_{dx}_{atlas}_CorticalThickness_Data.csv"
    output_path = os.path.join(output_dir, output_filename)
    harmonized_cortical_data.to_csv(output_path, index=False)

    print("Structural Harmonization and saving processes are complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Harmonize Cortical Thickness Data.')
    parser.add_argument('--data', required=True, help='Path to the data csv.')
    parser.add_argument('--dx', required=True, help='Name of the diagnosis being used.')
    parser.add_argument('--covariates', required=True, help='Path to the covariates csv.')
    parser.add_argument('--output_dir', required=True, help='Path to the desired output directory.')
    parser.add_argument('--atlas', required=True, help='Name of the atlas being used.')
    
    args = parser.parse_args()

    harmonizeCorticalThickness(args.data, args.covariates, args.output_dir, args.atlas)
