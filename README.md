🏫 SARC Shape of Performance
A High-Performance School Comparison Engine

This application provides a "radar-style" visualization for California School Accountability Report Card (SARC) data. It allows users to compare academic proficiency and class sizes across different schools or entire districts with zero latency.

📋 Data Acquisition Requirements
To populate the engine, you must download the following Excel files from the California Department of Education (CDE) website.

CDE Download Portal: SARC Data Files

Required Files:

schldir.xlsx (School Directory)

caall.xlsx (CAASPP Academic Results)

acselm.xlsx (Elementary Class Size Distribution)

acssec.xlsx (Secondary Class Size Distribution)

🏗️ Project Structure
For the builder script to work, your local directory must look exactly like this:

Plaintext
/CAASPP-Scores
│
├── app.py # The Streamlit Dashboard
├── build_master.py # The Data Processing Engine (ETL)
├── excel_files/ # Source Data Folder
│ ├── schldir.xlsx
│ ├── caall.xlsx
│ ├── acselm.xlsx
│ └── acssec.xlsx
└── README.md
⚙️ Installation & Setup
Ensure you have Python installed, then set up your environment:

Bash

# Install the necessary libraries

pip install streamlit pandas plotly openpyxl pyarrow
🚀 Execution Guide
Step 1: Process the Data
Because the raw Excel files are large and slow to parse, we use a "Builder" script to merge them into a high-performance Parquet file. Run this once, or whenever you update your Excel files.

Bash
python build_master.py
Wait for the success message: ✅ SUCCESS: 'sarc_master.parquet' generated.

Step 2: Launch the Dashboard
Once the .parquet file exists, launch the dashboard. It will load instantly.

Bash
streamlit run app.py
🕹️ How to Use
Select Dimension: Choose between School vs. School or District vs. District.

Filter Region: Use the County dropdown to narrow your search.

Choose Challengers: \* Challenger A is mapped in Blue.

Challenger B is mapped in Orange.

Read the Radar: \* Academic scores are raw percentages.

Small Class Score is an inverted metric: a larger shape on the chart represents smaller (more favorable) class sizes.

🛠️ Developer Notes
Performance: The app uses pd.read_parquet and @st.cache_data to ensure that on-device performance (like on a Surface Pro 11) remains buttery smooth.

Data Integrity: The build_master.py script automatically handles scientific notation in CDS codes and maps numeric County codes to their actual names.

Would you like me to add a section to this README explaining how to host this online for free using Streamlit Community Cloud?
