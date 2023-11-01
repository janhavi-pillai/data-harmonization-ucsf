import argparse
import pandas as pd
import csv
import os
import numpy as np
from neuroHarmonize import harmonizationLearn

#In the terminal, you would run the script like this:
#python3 harmonizeData.py --data /path/to/data.csv --covariates /path/to/covariates.csv --output_dir /path/to/output

def harmonizeData(data, covariates, output_dir):
    """
    Run ComBat (neuroHarmonize package) on any data

    Parameters:
    ---------
    data : str
        Path to a csv with 'PIDN' column and neuroimaging data to correct with ComBat (e.g., cortical thickness data with multiple ROIs).
    covariates : str
        Path to a csv with 'PIDN' column and covariates. The mandatory covariate is SITE. 
        Optional ones include AGE_M & SEX.
        The column names have to be named exactly as shown in the example csv.
    output_dir : str
        Path to the desired output directory.
    atlas : str
        Name of the atlas being used.
    metric : str
        Name of the metric type.

    Returns:
    -------
    None
        Writes a csv with the corrected values to a specific directory locally.
    """

    # Load data
    modelData = pd.read_csv(covariates).drop('PIDN', axis=1)
    input_data = pd.read_csv(data)
    data_matrix = input_data.drop('PIDN', axis=1).values

    # Run ComBat (neuroHarmonize) on the data
    model, data_adj = harmonizationLearn(data_matrix, modelData)

    # Format the corrected data for output
    harmonized_cortical_data = pd.DataFrame(data_adj, columns=input_data.columns[1:])  # Assuming PIDN is the first column
    harmonized_cortical_data.insert(0, 'PIDN', input_data['PIDN'])  # Add PIDN to the front

    # Save the corrected data to the desired directory
    output_filename = "Harmonized_" + os.path.basename(data)
    output_path = os.path.join(output_dir, output_filename)
    harmonized_cortical_data.to_csv(output_path, index=False)

    # I want to include the output path in the print statement so the user knows where to find the output
    print("Data Harmonization is complete and saved to " + output_path + "!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Data Harmonization using ComBat.')
    parser.add_argument('--data', required=True, help='Path to the data csv.')
    parser.add_argument('--covariates', required=True, help='Path to the covariates csv.')
    parser.add_argument('--output_dir', required=True, help='Path to the desired output directory.')
    
    args = parser.parse_args()
    harmonizeData(args.data, args.covariates, args.output_dir)
