import pandas as pd
import os
import glob
from .config import DATA_PROCESSED

class IPA27Consolidator:
    """Engine to merge multiple indicator CSVs into a Master Table."""
    
    def __init__(self):
        self.master_df = None

    def consolidate(self):
        """Finds all CSVs in data/processed and merges them."""
        csv_files = glob.glob(os.path.join(DATA_PROCESSED, "*.csv"))
        # Exclude existing master table if present
        csv_files = [f for f in csv_files if "Master_Table" not in f and "Results" not in f]
        
        if not csv_files:
            print("❌ No processed CSV files found to consolidate.")
            return None
            
        print(f"🔄 Consolidating {len(csv_files)} indicators...")
        
        merged_df = None
        
        for file in csv_files:
            name = os.path.basename(file).replace(".csv", "")
            df = pd.read_csv(file)
            
            # Ensure standard columns
            if not all(col in df.columns for col in ['Periodo', 'Region', 'Valor']):
                print(f"   ⚠️ Skipping {name}: Missing standard columns.")
                continue
                
            # Use 'Indicador' if present, else filename
            indicator_name = df['Indicador'].iloc[0] if 'Indicador' in df.columns else name
            
            # Prepare for join
            temp_df = df[['Periodo', 'Region', 'Valor']].copy()
            temp_df.columns = ['Periodo', 'Region', indicator_name]
            
            if merged_df is None:
                merged_df = temp_df
            else:
                merged_df = pd.merge(merged_df, temp_df, on=['Periodo', 'Region'], how='outer')
        
        if merged_df is not None:
            # Sort by Period
            merged_df = merged_df.sort_values(['Periodo', 'Region'], ascending=[False, True])
            
            # Export Master Table
            master_path = os.path.join(DATA_PROCESSED, "IPA27_Master_Table.csv")
            merged_df.to_csv(master_path, index=False)
            print(f"✅ Master Table generated: {master_path} ({len(merged_df)} rows)")
            
            # Export to Excel with multiple sheets
            excel_path = os.path.join(DATA_PROCESSED, "IPA27_Results.xlsx")
            with pd.ExcelWriter(excel_path) as writer:
                merged_df.to_excel(writer, sheet_name='Master_Table', index=False)
                # Regional sheets
                for reg in merged_df['Region'].unique():
                    merged_df[merged_df['Region'] == reg].to_excel(writer, sheet_name=f'Data_{reg}', index=False)
            
            print(f"✅ Excel Results generated: {excel_path}")
            self.master_df = merged_df
            
        return merged_df
