import argparse
import pandas as pd
import csv
import os
import numpy as np
from neuroHarmonize import harmonizationLearn

#In the terminal, you would run the script like this:
#python3 harmonizeFunctionalMatrices.py --data /path/to/data.csv --covariates /path/to/covariates.csv --output_dir /path/to/output --atlas YourAtlasChoice

def process_fMRI_csv_files(csv_directory, atlas):
    # Get a list of CSV filenames in sorted order
    csv_filenames = sorted([filename for filename in os.listdir(csv_directory) if filename.endswith(".csv")])

    # Create an empty DataFrame to store the results
    result_df = pd.DataFrame()

    # Loop through each CSV filename
    for filename in csv_filenames:
        csv_file_path = os.path.join(csv_directory, filename)
        
        # Read the CSV file using pandas
        df = pd.read_csv(csv_file_path, header=None)
        
        if atlas == 'BNA':
            # Remove the 233rd row and 233rd column
            df.drop(232, axis=0, inplace=True)
            df.drop(232, axis=1, inplace=True)

        # Flatten the matrix into a single vector
        flattened_data = df.values.flatten()

        # Append to the result dataframe
        result_df = pd.concat([result_df, pd.DataFrame([flattened_data])], ignore_index=True)

    return result_df

def harmonizeFunctionalMatrices(data, covariates, atlas, output_dir):

    """
    Harmonizes neuroimaging data using ComBat from the neuroHarmonize package.
    
    This function takes in the path to a directory of CSV files with neuroimaging data,
    performs harmonization using ComBat, reshapes the harmonized data based on the provided
    atlas, and then saves each reshaped matrix back to a separate CSV file in a specified 
    output directory.

    Parameters:
    -----------
    data : str
        Path to a directory containing CSV files with neuroimaging data. Each CSV should contain 
        matrix data flattened into a single vector. The filenames in this directory can be used 
        to derive participant identifiers (PIDN).
        
    covariates : str
        Path to a CSV file containing covariates. The mandatory covariate is 'SITE' and other 
        optional ones include 'AGE_M' & 'SEX'. The 'PIDN' column in this file should match the 
        order of the matrices in the `data` directory.

    atlas : str, one of ['Schaeffer400', 'BNA']
        Specifies the atlas used for the neuroimaging data. Determines the shape of the matrix 
        after reshaping. If the atlas is 'Schaeffer400', the shape is (244, 244). If the atlas is 
        'BNA', the shape is (400, 400).

    output_dir : str
        Path to the desired output directory where harmonized data matrices will be saved as CSV files.

    Returns:
    --------
    None. 
    Harmonized data matrices are saved to individual CSV files in the specified output directory.

    Raises:
    -------
    ValueError:
        If an unsupported atlas is provided.

    Example:
    --------
    > harmonizeFunctionalMatrices('./data/', './covariates.csv', 'BNA', './output/')
    """

    # Load in data
    modelData = pd.read_csv(covariates)
    funcMatrix = process_fMRI_csv_files(data, atlas=atlas)

    # 'funcMatrix' now contains the flattened data from all CSV files in the directory. 
    # Each row corresponds to a flattened vector for each participant.
    funcMatrix = funcMatrix.astype(float)
    funcMatrix = funcMatrix.values

    # Run ComBat (neuroHarmonize) on the data
    func_model, func_adj = harmonizationLearn(funcMatrix, modelData)

    # Convert the harmonized data back into its respective csv
    harmonized_df = pd.DataFrame(func_adj)
    
    # Extract PIDN values directly from the 'covariates' DataFrame
    pidn_list = modelData['PIDN'].tolist()

    # Decide the reshape dimensions based on the atlas
    if atlas == 'Schaeffer400':
        reshape_dims = (400, 400)
    elif atlas == 'BNA':
        reshape_dims = (244, 244)
    else:
        raise ValueError("This atlas has not been integrated into this harmonization yet.")

    # Loop through the DataFrame, unflatten each row into the desired matrix, and save it
    for index, row in harmonized_df.iterrows():
        vector = np.array(row, dtype=float)
        matrix = vector.reshape(reshape_dims)

        # Get the corresponding PIDN from the list
        pidn = pidn_list[index]

        # Construct the full path for the output file in the specified directory
        file_name = os.path.join(output_dir, f'matrix_{pidn}.csv')
        
        matrix_df = pd.DataFrame(matrix)
        
        # Save each matrix with PIDN in the filename to the specified directory
        matrix_df.to_csv(file_name, index=False, header=False)
        
    print("Harmonization and saving processes are complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Harmonize Functional Matrices Data.')
    parser.add_argument('--data', required=True, help='Path to the data csv containing neuroimaging data.')
    parser.add_argument('--covariates', required=True, help='Path to the covariates csv.')
    parser.add_argument('--output_dir', required=True, help='Path to the desired output directory.')
    parser.add_argument('--atlas', required=True, choices=['Schaeffer400', 'BNA'], help='Name of the atlas being used. Choose from "Schaeffer400" or "BNA".')

    args = parser.parse_args()

    harmonizeFunctionalMatrices(args.data, args.covariates, args.atlas, args.output_dir)

