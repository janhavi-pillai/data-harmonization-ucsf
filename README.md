# data-harmonization-ucsf

Data harmonization tools for multi-site structural and functional neuroimaging analysis. These scripts utilize ComBat (https://github.com/Jfortin1/ComBatHarmonization) and neuroHarmonize (https://github.com/rpomponio/neuroHarmonize).

Cortical Thickness:
`python3 harmonize_CorticalThickness.py --data /path/to/data.csv --dx DiagnosisType --covariates /path/to/covariates.csv --output_dir /path/to/output --atlas YourAtlasChoice`

Functional Matrices:
`python3 harmonize_FunctionalMatrices.py --data /path/to/data.csv --covariates /path/to/covariates.csv --output_dir /path/to/output --atlas YourAtlasChoice`

Note: We only have the Brainnetome (BNA) & Schaeffer400 atlases built in. You may need to make modifications to account for other atlases. 
