import pandas as pd
import os
import glob
import numpy as np

data_dir = r'g:\Mi unidad\Proyectos\IPA27_project\results\data'
files = [f for f in glob.glob(os.path.join(data_dir, "ipa27_raw_*.xlsx")) if "~$" not in f]
files.sort(reverse=True)

new_file = files[0]
old_file = files[1]

print(f"New: {os.path.basename(new_file)}")
print(f"Old: {os.path.basename(old_file)}")

xl_new = pd.ExcelFile(new_file)
xl_old = pd.ExcelFile(old_file)

indicators = [s for s in xl_new.sheet_names if s.upper() != 'LEER']
print(f"Total indicators: {len(indicators)}")

changes = []
for ind in indicators:
    try:
        df_new = pd.read_excel(xl_new, sheet_name=ind)
        if 'Periodo' not in df_new.columns: continue
        
        last_p_new = str(df_new['Periodo'].iloc[-1])
        
        # Find Andalusia column
        and_col = [c for c in df_new.columns if 'Andaluc' in str(c) or c == 'AND']
        if not and_col: continue
        and_col = and_col[0]
        
        val_new = df_new[and_col].iloc[-1]
        
        if ind in xl_old.sheet_names:
            df_old = pd.read_excel(xl_old, sheet_name=ind)
            last_p_old = str(df_old['Periodo'].iloc[-1])
            
            if last_p_new != last_p_old:
                changes.append((ind, last_p_old, last_p_new, "PERIOD_CHANGE", val_new))
            else:
                # Check value change for last period
                val_old_series = df_old[df_old['Periodo'].astype(str) == last_p_new][and_col]
                if not val_old_series.empty:
                    val_old = val_old_series.values[0]
                    if abs(val_new - val_old) > 1e-6:
                        changes.append((ind, last_p_new, last_p_new, "VALUE_CHANGE", val_new))
        else:
            changes.append((ind, "N/A", last_p_new, "NEW_INDICATOR", val_new))
    except Exception as e:
        print(f"Error in {ind}: {e}")

print(f"\nIndicators with changes: {len(changes)}")
for c in changes:
    print(c)
