# data-harmonization-ucsf

Data harmonization tools for multi-site structural and functional neuroimaging analysis. These scripts utilize ComBat (https://github.com/Jfortin1/ComBatHarmonization) and neuroHarmonize (https://github.com/rpomponio/neuroHarmonize).

All Data (csv format):
`python3 harmonizeData.py --data /path/to/data.csv --covariates /path/to/covariates.csv --output_dir /path/to/output/directory`

Functional Matrices:
`python3 harmonizeFunctionalMatrices.py --data /path/to/data.csv --covariates /path/to/covariates.csv --output_dir /path/to/output --atlas AtlasName`

Note for Functional Matrices: Only Brainnetome (BNA) & Schaeffer400 atlases built in. You may need to make modifications to account for other atlases. 
