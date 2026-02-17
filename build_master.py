import pandas as pd
import os

# --- COUNTY DECODER ---
COUNTY_MAP = {
    '1': 'Alameda', '2': 'Alpine', '3': 'Amador', '4': 'Butte', '5': 'Calaveras', '6': 'Colusa', '7': 'Contra Costa',
    '8': 'Del Norte', '9': 'El Dorado', '10': 'Fresno', '11': 'Glenn', '12': 'Humboldt', '13': 'Imperial', '14': 'Inyo',
    '15': 'Kern', '16': 'Kings', '17': 'Lake', '18': 'Lassen', '19': 'Los Angeles', '20': 'Madera', '21': 'Marin',
    '22': 'Mariposa', '23': 'Mendocino', '24': 'Merced', '25': 'Modoc', '26': 'Mono', '27': 'Monterey', '28': 'Napa',
    '29': 'Nevada', '30': 'Orange', '31': 'Placer', '32': 'Plumas', '33': 'Riverside', '34': 'Sacramento', '35': 'San Benito',
    '36': 'San Bernardino', '37': 'San Diego', '38': 'San Francisco', '39': 'San Joaquin', '40': 'San Luis Obispo',
    '41': 'San Mateo', '42': 'Santa Barbara', '43': 'Santa Clara', '44': 'Santa Cruz', '45': 'Shasta', '46': 'Sierra',
    '47': 'Siskiyou', '48': 'Solano', '49': 'Sonoma', '50': 'Stanislaus', '51': 'Sutter', '52': 'Tehama', '53': 'Trinity',
    '54': 'Tulare', '55': 'Tuolumne', '56': 'Ventura', '57': 'Yolo', '58': 'Yuba'
}

def build_sarc_master():
    print("🚀 Starting Integrated Data Build...")
    subfolder = 'excel_files'
    
    def clean_cds(series):
        return series.apply(lambda x: str(int(float(x))).strip().zfill(14) if pd.notnull(x) and str(x).strip() != '' else '')

    # 1. Load Directory
    dir_path = os.path.join(subfolder, 'schldir.xlsx')
    if not os.path.exists(dir_path):
        print(f"❌ Error: {dir_path} not found!")
        return
    
    df = pd.read_excel(dir_path, dtype=str, engine='openpyxl')
    df.columns = [c.strip().upper() for c in df.columns]
    df = df.rename(columns={'CDSCODE': 'CDSCode', 'DISTRICT': 'District', 'SCHOOL': 'School'})
    df['CDSCode'] = clean_cds(df['CDSCode'])
    df['County'] = df['C'].map(COUNTY_MAP).fillna('Unknown')

    # 2. Merge Academics (caall.xlsx)
    scores_path = os.path.join(subfolder, 'caall.xlsx')
    if os.path.exists(scores_path):
        print("Merging Academics...")
        df_scores = pd.read_excel(scores_path, dtype=str, engine='openpyxl')
        df_scores.columns = [c.strip().upper() for c in df_scores.columns]
        df_scores['CDS_JOIN'] = clean_cds(df_scores['CDSCODE'])
        for col in ['SMATH_Y1', 'SELA_Y1']:
            if col in df_scores.columns:
                df_scores[col] = pd.to_numeric(df_scores[col], errors='coerce')
        df = pd.merge(df, df_scores[['CDS_JOIN', 'SMATH_Y1', 'SELA_Y1']], left_on='CDSCode', right_on='CDS_JOIN', how='left')

    # 3. Merge Class Size (acselm.xlsx and acssec.xlsx)
    class_dfs = []
    for f_name in ['acselm.xlsx', 'acssec.xlsx']:
        f_path = os.path.join(subfolder, f_name)
        if os.path.exists(f_path):
            print(f"Merging Class Size: {f_name}...")
            temp_df = pd.read_excel(f_path, dtype=str, engine='openpyxl')
            temp_df.columns = [c.strip().upper() for c in temp_df.columns]
            temp_df['CDS_JOIN_CLASS'] = clean_cds(temp_df['CDSCODE'])
            avg_cols = [c for c in temp_df.columns if c.startswith('AVG') and c.endswith('Y1')]
            for c in avg_cols:
                temp_df[c] = pd.to_numeric(temp_df[c], errors='coerce')
            temp_df['ROW_AVG'] = temp_df[avg_cols].mean(axis=1)
            agg = temp_df.groupby('CDS_JOIN_CLASS')['ROW_AVG'].mean().reset_index()
            class_dfs.append(agg)

    if class_dfs:
        all_class = pd.concat(class_dfs).groupby('CDS_JOIN_CLASS')['ROW_AVG'].mean().reset_index()
        df = pd.merge(df, all_class, left_on='CDSCode', right_on='CDS_JOIN_CLASS', how='left')
        df = df.rename(columns={'ROW_AVG': 'AVG_SIZE'})

    # 4. Merge Demographic DNA (enrbysubgrp.xlsx)
    dna_path = os.path.join(subfolder, 'enrbysubgrp.xlsx')
    dna_cols = ['PERGF','PERGM','PERGX','PERAI','PERAS','PERAA','PERFI','PERHI','PERPI','PERMULTI','PERWH','PEREL','PERSD','PERDI']
    if os.path.exists(dna_path):
        print("Merging Demographic DNA Profile...")
        df_dna = pd.read_excel(dna_path, dtype=str, engine='openpyxl')
        df_dna.columns = [c.strip().upper() for c in df_dna.columns]
        df_dna['CDS_JOIN_DNA'] = clean_cds(df_dna['CDSCODE'])
        for c in dna_cols:
            if c in df_dna.columns:
                df_dna[c] = pd.to_numeric(df_dna[c], errors='coerce').fillna(0)
        df = pd.merge(df, df_dna[['CDS_JOIN_DNA'] + [c for c in dna_cols if c in df_dna.columns]], 
                      left_on='CDSCode', right_on='CDS_JOIN_DNA', how='left')

    # Final Cleanup
    numeric_cols = ['SMATH_Y1', 'SELA_Y1', 'AVG_SIZE'] + dna_cols
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    df.to_parquet('sarc_master.parquet', index=False)
    print("✅ SUCCESS: 'sarc_master.parquet' generated with all Integrated Metrics.")

if __name__ == "__main__":
    build_sarc_master()