# ------------------------------ Import Libraries ------------------------------
import os
import sys 
import time
import warnings
import argparse
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm

warnings.filterwarnings("ignore")

# ------------------------------ Argument Parser ------------------------------
argparser = argparse.ArgumentParser(
    description="""***** Example: python king_visualization.py -i <file.kin> -size <float>""",
    formatter_class=argparse.RawTextHelpFormatter
)

argparser.add_argument(
    "-i",
    required=True,
    type=str,
    help="Path to the directory containing .kin and .kin0 files. "
     "For example, use '-i path/to/king' if 'king.kin' and 'king.kin0' exist in the same directory."
)

argparser.add_argument(
    "-size",
    type=float,
    default=7.0,
    help="Font size of the heatmap (default: 7.0)"
)

args = argparser.parse_args()

# ------------------------------ Prepare Input ------------------------------
start_cpu_time = time.process_time()
current_timestamp = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")

# Create results directory
result_dir = f"result_{current_timestamp}"
os.makedirs(result_dir, exist_ok=True)  # Avoid error if directory exists

# Set input path
input_path = args.i

# Check if .kin and .kin0 files exist
kin_path = f"{input_path}.kin"
kin_exists = os.path.exists(kin_path)
kin0_path = f"{input_path}.kin0"
kin0_exists = os.path.exists(kin0_path)

if kin_exists:
    print(f"{input_path} exists, processing .kin file...")
    dfkin = pd.read_csv(kin_path, sep='\t')
    dfkin.drop(columns=['N_SNP', 'Z0', 'Phi', 'HetHet', 'IBS0', 'Error'], inplace=True)
    dfkin.rename(columns={"FID": "FID1"}, inplace=True)
    dfkin.insert(2, "FID2", dfkin["FID1"])

if kin0_exists:
    print(f"{kin0_path} exists, processing .kin0 file...")
    dfkin0 = pd.read_csv(kin0_path, sep='\t')
    dfkin0.drop(columns=['N_SNP', 'HetHet', 'IBS0'], inplace=True)

if not kin_exists and not kin0_exists:
    print("Error: Neither .kin nor .kin0 file found!")
    sys.exit(1)

# Combine dataframes based on file existence
if kin_exists and kin0_exists:
    df = pd.concat([dfkin, dfkin0], ignore_index=True)
elif kin_exists:
    df = dfkin.copy()
elif kin0_exists:
    df = dfkin0.copy()

# Convert 'Kinship' column to float
df["Kinship"] = df["Kinship"].astype(float)

# ------------------------------ Create Heatmap ------------------------------
name_list = list(np.unique(df['ID1'].to_list() + df['ID2'].to_list()))
heat_df = pd.DataFrame(
    np.zeros((len(name_list), len(name_list)), dtype=float),
    index=name_list,
    columns=name_list
)

multiply = 10000

# Set threshold values for each category of potential relationships
thresholds = [round(1/(2**(9/2)), 4), 
              round(1/(2**(7/2)), 4), 
              round(1/(2**(5/2)), 4), 
              round(1/(2**(3/2)), 4)]

# Update heatmap matrix symmetrically
for row in df.itertuples(index=False):
    id1, id2, kinship = row.ID1, row.ID2, row.Kinship
    kinship_scaled = kinship * multiply

    heat_df.loc[id1, id2] = kinship_scaled
    heat_df.loc[id2, id1] = kinship_scaled



#------------------------ Create cmap ------------------------
# Compute integer threshold values for each relationship category
# The thresholds are derived from 1 / (2^(n/2)), where n = {3, 5, 7, 9}
# These values are then scaled by 'multiply' to obtain the final integer representation.
idx_duplicate = round(thresholds[3]*multiply)
idx_first_degree = round(thresholds[2]*multiply) 
idx_second_degree = round(thresholds[1]*multiply) 
idx_third_degree = round(thresholds[0]*multiply) 

# Define color boundaries
boundaries = [
    -1 * multiply, 
    -idx_duplicate, 
    -idx_first_degree, 
    -idx_second_degree, 
    -idx_third_degree, 
    0, 
    idx_third_degree, 
    idx_second_degree, 
    idx_first_degree, 
    idx_duplicate, 
    0.5 * multiply
]

# Define colormap colors (blue to red gradient) for each category of potential relationships:
# Duplicate, First degree, Second degree, Third degree, and Unrelated
colors = [
    "#0253c4", "#0a70ff", "#418efa", "#82b4fa", "#b8d5ff",
    "#fee3df", "#fab6ac", "#ed5f4a", "#bd1a02", "#630e01"
]

# Create a colormap
mycmap = LinearSegmentedColormap.from_list("custom_cmap", colors, N=len(boundaries) - 1)

# Create a BoundaryNorm to map values to discrete colors
norm = BoundaryNorm(boundaries, mycmap.N)

# Define tick middle points for heatmap labels
tick_middle_points = [
    -1 * multiply,
    -(idx_duplicate + multiply) / 2,  # Middle of "Duplicate" (Negative)
    -idx_duplicate,
    -idx_first_degree,
    -idx_second_degree,
    -idx_third_degree,
    -idx_third_degree / 2,  # Middle of "Unrelated" (Negative)
    0,
    idx_third_degree / 2,  # Middle of "Unrelated" (Positive)
    idx_third_degree,
    (idx_third_degree + idx_second_degree) / 2,  # Middle of "Third degree"
    idx_second_degree,
    (idx_second_degree + idx_first_degree) / 2,  # Middle of "Second degree"
    idx_first_degree,
    (idx_first_degree + idx_duplicate) / 2,  # Middle of "First degree"
    idx_duplicate,
    (idx_duplicate + 0.5 * multiply) / 2,  # Middle of "Duplicate" (Positive)
    0.5 * multiply
]

# Convert previously scaled integer values back to percentage representation
# Now they are divided by 'multiply' and converted to percentages.
idx_duplicate_pct = round(idx_duplicate / multiply * 100, 4)
idx_first_degree_pct = round(idx_first_degree / multiply * 100, 4)
idx_second_degree_pct = round(idx_second_degree / multiply * 100, 4)
idx_third_degree_pct = round(idx_third_degree / multiply * 100, 4)

# Define tick labels for heatmap
tick_labels = [
    -100,
    "High genetic distance\n(Negative Value)",
    -idx_duplicate_pct,
    -idx_first_degree_pct,
    -idx_second_degree_pct,
    -idx_third_degree_pct,
    "Unrelated and from\ndifferent populations\n(Negative Value)",
    0,
    "Unrelated",
    idx_third_degree_pct,
    "Third degree",
    idx_second_degree_pct,
    "Second degree",
    idx_first_degree_pct,
    "First degree",
    idx_duplicate_pct,
    "Duplicate",
    50
]
        
# Convert heatmap values to percentage for labeling on the heatmap
formatted_text = (heat_df / multiply * 100).values.tolist()

#------------------------ Plot Heatmap ------------------------
mask = np.triu(np.ones_like(heat_df, dtype=bool))

fig, ax = plt.subplots(figsize=(20,15))
sns.heatmap(
    data=heat_df,
    ax=ax,
    vmax=0.5 * multiply, 
    vmin=-1 * multiply,
    cmap=mycmap,
    norm=norm,
    linewidths=0.5, 
    linecolor='lightgray',
    annot=formatted_text,
    fmt=".2f",
    mask=mask,
    # annot_kws={"fontsize": args.size} 
    annot_kws={"fontsize": 6} 
)

cbar = ax.collections[0].colorbar
cbar.set_ticks(tick_middle_points)  # Set ticks at the middle points
cbar.set_ticklabels(tick_labels)    # Set tick labels

plt.title('Potential Relationship (Kinship*100)', fontsize = 20)
plt.savefig(f'result_{current_timestamp}/Heatmap_{current_timestamp}.png', dpi=300, bbox_inches='tight')

end_cpu_time = time.process_time()
elapsed_cpu_time = end_cpu_time - start_cpu_time

print(f"Computation time: {elapsed_cpu_time:.4f} seconds")