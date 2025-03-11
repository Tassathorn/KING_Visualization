# KING Kinship Visualization

This script processes kinship data from KING software and generates a heatmap to visualize potential relationships.

## 📌 About This Script

This scipt was developed by **Tassathorn Poonsin** to assist in tasks at **National Biobank of Thailand (NBT)**. While it was created for work purposes, this project is released as an open-source tool under the **APACHE LICENSE, VERSION 2.0**, allowing others to use it freely.

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
  result_YYYY-MM-DD_HH.MM.SS/Heatmap_YYYY-MM-DD_HH.MM.SS.png
  ```
- The directory structure will look like:
  ```
  result_YYYY-MM-DD_HH.MM.SS/
  ├── Heatmap_YYYY-MM-DD_HH.MM.SS.png
  ```

## ⚠️ Notes

- Ensure `.kin` and `.kin0` files exist in the provided directory.
- If no valid input files are found, the script will exit with an error.

## 🛠️ License

This software is licensed under the [APACHE LICENSE, VERSION 2.0](LICENSE).

Copyright 2025 National Biobank of Thailand (NBT)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Any modifications or derivative works of this software must retain
this NOTICE file as part of the source distribution.

