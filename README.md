# KING Kinship Visualization

This script processes kinship data from KING software and generates a heatmap to visualize potential relationships.

## 📌 About This Script

This software was developed by **Tassathorn Poonsin** to assist in tasks at **National Biobank of Thailand (NBT)**. While it was created for work purposes, this script is released as an open-source tool under the **MIT License**, allowing others to use and modify it freely.

## 🚀 Features

- Reads `.kin` and `.kin0` files from a specified directory
- Computes relationship categories based on kinship values
- Generates a heatmap for visualization
- Saves the output in a structured directory

## 🔧 Installation & Dependencies

Ensure you have Python installed along with the following libraries:

```bash
pip install numpy pandas matplotlib seaborn argparse
```

## 📊 Usage

Run the script with:

```bash
python king_visualization.py -i path/to/dataset -size font_size
```

For example:

```bash
ppython king_visualization.py -i path/to/king -size 8
```

This will search for `king.kin` and `king.kin0` inside `path/to/` and generate a heatmap.

## 📂 Output

- The script will save the heatmap to:
  ```
  results/heatmap_YYYY-MM-DD_HH.MM.SS/kinship_heatmap_YYYY-MM-DD_HH.MM.SS.png
  ```
- The directory structure will look like:
  ```
  results/
  ├── heatmap_2025-03-10_15.30.45/
  │   ├── kinship_heatmap_2025-03-10_15.30.45.png
  ```

## ⚠️ Notes

- Ensure `.kin` and `.kin0` files exist in the provided directory.
- If no valid input files are found, the script will exit with an error.

## 🛠️ License

This project is released under the [MIT License](LICENSE).

