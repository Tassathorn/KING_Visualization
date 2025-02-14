#------------------------------Import library------------------------------
import time
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm
import pandas as pd
import seaborn as sns
import argparse
from argparse import RawTextHelpFormatter
import os

import warnings
warnings.filterwarnings("ignore")

argparser = argparse.ArgumentParser(description='''***** Example : python king_visualzation.py -i <file.kin> -size <float>
                                    ''', formatter_class=RawTextHelpFormatter)
    
argparser.add_argument(
    "-i",
    help=".kin file from KING <file.kin>. Note: the corresponding .kin0 file must also be in the same directory."
)
argparser.add_argument(
    "-size", 
    help="font size of the heatmap <float> ")
args = argparser.parse_args()

#------------------------------------------------ Prepare input ----------------------------------------
start = time.process_time()
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

if not os.path.exists(f'result_{current_time}'):
    os.mkdir(f'result_{current_time}') 

input_path = args.i
kin_exists = False
kin0_exists = False

if os.path.exists(input_path):
    print(f"{input_path} exists, processing .kin file...")
    kin_exists = True
  
if os.path.exists(input_path + '0'):
    print(f"{input_path + '0'} exists, processing .kin0 file...")
    kin0_exists = True
    
if (not kin_exists) and (not kin0_exists):
    # If neither .kin nor .kin0 exist
    print("Neither .kin nor .kin0 file found!")
    
if kin_exists:
    dfkin = pd.read_csv(input_path,
                    sep='\t')
    dfkin = dfkin.drop(columns=['N_SNP', 'Z0', 'Phi', 'HetHet', 'IBS0', 'Error'])
    dfkin = dfkin.rename(columns={"FID":"FID1"})
    dfkin.insert(2, "FID2", dfkin['FID1'].to_list())

if kin0_exists :    
    dfkin0 = pd.read_csv(input_path + '0',
                    sep='\t')
    dfkin0 = dfkin0.drop(columns=['N_SNP','HetHet', 'IBS0'])
    dfkin0

if kin_exists and kin0_exists:
    df = pd.concat([dfkin,dfkin0])
    df.index = np.arange(len(df))
elif kin_exists and (not kin0_exists):
    df = dfkin.copy()
elif (not kin_exists) and kin0_exists:
    df = dfkin0.copy()

for i in ["Kinship"]:
    df[i] = df[i].astype(float)
    
#------------------------------------------------ Create Heatmap -----------------------------------------------------
name_list = list(np.unique(df['ID1'].to_list() + df['ID2'].to_list()))

heat_df = pd.DataFrame(data=[[0.0000 for i in range(len(name_list))] for j in range(len(name_list))],
                       index=name_list,
                       columns=name_list)

multiply = 10000

for i in range(len(df)):
    heat_df[df['ID1'][i]][df['ID2'][i]] = df['Kinship'][i]*multiply 
    heat_df[df['ID2'][i]][df['ID1'][i]] = df['Kinship'][i]*multiply 
        
    # if df['Kinship'][i] >= 0:
    #     heat_df[df['ID1'][i]][df['ID2'][i]] = df['Kinship'][i]*multiply 
    #     heat_df[df['ID2'][i]][df['ID1'][i]] = df['Kinship'][i]*multiply 
    # else:
    #     heat_df[df['ID1'][i]][df['ID2'][i]] = 0
    #     heat_df[df['ID2'][i]][df['ID1'][i]] = 0
    
    if ((heat_df[df['ID1'][i]][df['ID2'][i]] == 0.0884*multiply) or 
        (heat_df[df['ID1'][i]][df['ID2'][i]] == 0.177*multiply) or 
        (heat_df[df['ID1'][i]][df['ID2'][i]] == 0.354*multiply)):
        heat_df[df['ID1'][i]][df['ID2'][i]] == heat_df[df['ID1'][i]][df['ID2'][i]] - 0.000001
    elif ((heat_df[df['ID1'][i]][df['ID2'][i]] == -0.0884*multiply) or 
        (heat_df[df['ID1'][i]][df['ID2'][i]] == -0.177*multiply) or 
        (heat_df[df['ID1'][i]][df['ID2'][i]] == -0.354*multiply)):
        heat_df[df['ID1'][i]][df['ID2'][i]] == heat_df[df['ID1'][i]][df['ID2'][i]] + 0.000001
        
#------------------------ Create cmap ------------------------
idx_duplicate = int(0.354 *multiply)  # 1/(2**(3/2))
idx_first_degree = int(0.177 *multiply)  # 1/(2**(5/2))
idx_second_degree = int(0.0884 *multiply)  # 1/(2**(7/2))
idx_third_degree = int(0.0442 *multiply)  # 1/(2**(9/2))

boundaries = [-1*multiply, 
              -idx_duplicate,
              -idx_first_degree, 
              -idx_second_degree, 
              -idx_third_degree, 
              0, 
              idx_third_degree, 
              idx_second_degree, 
              idx_first_degree, 
              idx_duplicate, 
              0.5*multiply]
 # Duplicate, First degree, Second degree, Third degree, Unrelated
colors = ["#0253c4", "#0a70ff", "#418efa", "#82b4fa", "#b8d5ff",
          "#fee3df", "#fab6ac", "#ed5f4a", "#bd1a02", "#630e01"]

# Create a colormap
mycmap = LinearSegmentedColormap.from_list("custom_cmap", colors, N=len(boundaries)-1)

# Create a BoundaryNorm to map values to discrete colors
norm = BoundaryNorm(boundaries, mycmap.N)

# create the tick middle points and tick label
tick_middle_points = [-10000,
                      -(idx_duplicate + 10000) / 2,                  # Middle of "Duplicate"
                      -idx_duplicate,
                      -idx_first_degree,
                      -idx_second_degree,
                      -idx_third_degree,
                      -(0 + idx_third_degree) / 2,               # Middle of "unrelated" (Negative)
                      0,
                      (0 + idx_third_degree) / 2,               # Middle of "unrelated"
                      idx_third_degree,
                      (idx_third_degree + idx_second_degree) / 2,  # Middle of "Third degree"
                      idx_second_degree,
                      (idx_second_degree + idx_first_degree) / 2,  # Middle of "Second degree"
                      idx_first_degree,
                      (idx_first_degree + idx_duplicate) / 2,       # Middle of "First degree"
                      idx_duplicate,
                      (idx_duplicate + 5000) / 2,                  # Middle of "Duplicate"
                      5000
                      ]

tick_labels = [-100,
               'High genetic distance\n(Negative Value)',
               -round(idx_duplicate / multiply * 100, 4),
               -round(idx_first_degree / multiply * 100, 4),
               -round(idx_second_degree / multiply * 100, 4),
               -round(idx_third_degree / multiply * 100, 4), 
               'Unrelated and from\ndifferent populations\n(Negative Value)',
               0, 
               'Unrelated', 
               round(idx_third_degree / multiply * 100, 4), 
               'Third degree', 
               round(idx_second_degree / multiply * 100, 4),
               'Second degree',
               round(idx_first_degree / multiply * 100, 4),
               'First degree', 
               round(idx_duplicate / multiply * 100, 4),
               'Duplicate',
               50]

formatted_text = []
for i in range(len(heat_df)):
    formatted_text.append((heat_df.iloc[i] / multiply * 100).to_list())
    
#------------------------ Plot Heatmap ------------------------
mask = np.zeros_like(heat_df)
mask[np.triu_indices_from(mask)] = True

fig, ax = plt.subplots(figsize=(20,15))
sns.heatmap(
    data=heat_df,
    ax=ax,
    vmax=5000, 
    vmin=-10000,
    cmap=mycmap,
    norm=norm,
    linewidths=.5, 
    linecolor='lightgray',
    annot=formatted_text,
    fmt=".2f",
    mask=mask,
    annot_kws={"fontsize": args.size}
)

cbar = ax.collections[0].colorbar
cbar.set_ticks(tick_middle_points)  # Set the ticks to the middle points
cbar.set_ticklabels(tick_labels) # Set the tick labels to the middle points

plt.title('Potential Relationship (Kinship*100)', fontsize = 20)
ax.set_yticklabels(ax.get_yticklabels(), rotation=1)
plt.savefig(f'result_{current_time}/KING_Heatmap_{current_time}.png', dpi=300, bbox_inches='tight')