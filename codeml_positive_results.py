import os
import re
import pandas as pd

# Summary classification table based on (model, NSsites)
CLASSIFICATION_TABLE = {
    (0, 0): {
        'Model_Name': 'M0',
        'ω > 1 Allowed': 'No',
        'Varies Across Sites': 'No',
        'Varies Across Branches': 'No'
    },
    (0, 1): {
        'Model_Name': 'M1a',
        'ω > 1 Allowed': 'No',
        'Varies Across Sites': 'Yes',
        'Varies Across Branches': 'No'
    },
    (0, 2): {
        'Model_Name': 'M2a',
        'ω > 1 Allowed': 'Yes',
        'Varies Across Sites': 'Yes',
        'Varies Across Branches': 'No'
    },
    (0, 3): {
        'Model_Name': 'M3',
        'ω > 1 Allowed': 'Yes',
        'Varies Across Sites': 'Yes',
        'Varies Across Branches': 'No'
    },
    (0, 4): {
        'Model_Name': 'M4',
        'ω > 1 Allowed': 'Yes',
        'Varies Across Sites': 'Yes',
        'Varies Across Branches': 'No'
    },
    (0, 5): {
        'Model_Name': 'M5',
        'ω > 1 Allowed': 'Yes',
        'Varies Across Sites': 'Yes',
        'Varies Across Branches': 'No'
    },
    (0, 6): {
        'Model_Name': 'M6',
        'ω > 1 Allowed': 'Yes',
        'Varies Across Sites': 'Yes',
        'Varies Across Branches': 'No'
    },
    (0, 7): {
        'Model_Name': 'M7',
        'ω > 1 Allowed': 'No',
        'Varies Across Sites': 'Yes',
        'Varies Across Branches': 'No'
    },
    (0, 8): {
        'Model_Name': 'M8',
        'ω > 1 Allowed': 'Yes',
        'Varies Across Sites': 'Yes',
        'Varies Across Branches': 'No'
    },
    (1, 0): {
        'Model_Name': 'Free-ratio',
        'ω > 1 Allowed': 'Yes',
        'Varies Across Sites': 'No',
        'Varies Across Branches': 'Yes'
    },
    (2, 2): {
        'Model_Name': 'Branch-site A',
        'ω > 1 Allowed': 'Yes (on branch)',
        'Varies Across Sites': 'Yes',
        'Varies Across Branches': 'Yes (marked branches)'
    },
}

def parse_out_file(file_path):
    """
    Parses a codeml .out file to extract key results.
    Searches for lnL and omega (dN/dS) values.
    """
    results = {}
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract lnL value (e.g., "lnL(ntime: 10  np: 20): -1234.56")
    lnL_match = re.search(r'lnL\(ntime:\s*\d+\s+np:\s*\d+\):\s*([-\d\.]+)', content)
    results['lnL'] = float(lnL_match.group(1)) if lnL_match else None

    # Extract omega value (e.g., "omega (dN/dS) = 1" or "omega (dN/dS) = 0.123")
    omega_match = re.search(r'omega\s*\(dN/dS\)\s*=\s*([\d\.]+)', content)
    results['omega'] = float(omega_match.group(1)) if omega_match else None

    return results

def parse_ctl_file(file_path):
    """
    Parses a codeml .ctl file expected to contain key=value pairs.
    Ignores blank lines and lines starting with '#'.
    """
    results = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                results[key.strip()] = value.strip()
    return results

def determine_selection(omega):
    """
    Determines the selection type based on the omega (dN/dS) value.
    """
    if omega is None:
        return None
    if omega < 1:
        return 'Purifying'
    elif omega == 1:
        return 'Neutral'
    elif omega > 1:
        return 'Positive'
    return 'NA'

def infer_model_ns(file_prefix):
    """
    Attempts to infer the model and NSsites values from the file prefix.
    For example, from "OG0000001_model2orMore_dN_dS_NSsites0" it infers:
      - model: based on the string (if it contains "modelone", "model2orMore_dN_dS", or "modelb")
      - NSsites: extracted as the number following "NSsites".
    Returns a tuple (model, NSsites) as integers.
    """
    parts = file_prefix.split('_')
    model_part = None
    ns_sites_val = None

    for part in parts:
        if part.startswith("model"):
            model_part = part
        elif part.startswith("NSsites"):
            try:
                ns_sites_val = int(part.replace("NSsites", ""))
            except ValueError:
                ns_sites_val = None

    # Map model string to an integer code.
    model_map = {
        'modelone': 0,
        'model2orMore_dN_dS': 2,  # Adjusted based on provided examples.
        'modelb': 1             # Adjusted based on provided examples.
    }
    model_val = model_map.get(model_part, None)
    return model_val, ns_sites_val

def classify_model(ctl_results, file_prefix):
    """
    Classifies the result based on the control file keys (model and NSsites) if available,
    or infers them from the file prefix.
    Returns a dictionary with the classification details from the summary table.
    """
    model_val = None
    ns_sites_val = None
    if 'model' in ctl_results:
        try:
            model_val = int(ctl_results.get('model'))
        except ValueError:
            model_val = None
    if 'NSsites' in ctl_results:
        try:
            ns_sites_val = int(ctl_results.get('NSsites'))
        except ValueError:
            ns_sites_val = None

    # If not provided by the ctl file, try to infer from the file prefix.
    if model_val is None or ns_sites_val is None:
        inferred_model, inferred_ns = infer_model_ns(file_prefix)
        if model_val is None:
            model_val = inferred_model
        if ns_sites_val is None:
            ns_sites_val = inferred_ns

    key = (model_val, ns_sites_val)
    if key in CLASSIFICATION_TABLE:
        return CLASSIFICATION_TABLE[key]
    else:
        return {
            'Model_Name': 'Unclassified',
            'ω > 1 Allowed': 'Unclassified',
            'Varies Across Sites': 'Unclassified',
            'Varies Across Branches': 'Unclassified'
        }

def main():
    folder = 'codeml_results'
    combined_data = []
    
    # List all files in the folder.
    all_files = os.listdir(folder)
    # Separate out .out and .ctl files.
    out_files = [f for f in all_files if f.endswith('.out')]
    ctl_files = [f for f in all_files if f.endswith('.ctl')]
    
    for out_file in out_files:
        # Use the basename (without extension) to pair corresponding files.
        file_prefix = os.path.splitext(out_file)[0]
        ctl_file = file_prefix + '.ctl'
        
        out_path = os.path.join(folder, out_file)
        ctl_path = os.path.join(folder, ctl_file)
        
        # Parse the .out file.
        out_results = parse_out_file(out_path)
        
        # Parse the .ctl file if available.
        ctl_results = {}
        if ctl_file in ctl_files:
            ctl_results = parse_ctl_file(ctl_path)
        
        # Build the combined entry.
        combined_entry = {'file_prefix': file_prefix}
        combined_entry.update(out_results)
        for key, value in ctl_results.items():
            combined_entry[f'ctl_{key}'] = value
        
        # Add dn/ds (omega) and selection columns.
        omega_value = out_results.get('omega')
        combined_entry['dn/ds'] = omega_value
        combined_entry['selection'] = determine_selection(omega_value)
        
        # Classify using ctl values (or inferred from file name).
        classification = classify_model(ctl_results, file_prefix)
        combined_entry.update(classification)
        
        combined_data.append(combined_entry)
    
    # Create a DataFrame from all combined results.
    df = pd.DataFrame(combined_data)
    
    # Filter for only positive selection results (omega > 1, hence selection == "Positive")
    positive_df = df[df['selection'] == 'Positive']
    
    # Export the positive selection results to a new Excel file.
    output_excel = 'codeml_positive_results.xlsx'
    positive_df.to_excel(output_excel, index=False)
    print(f"Positive selection results have been saved to {output_excel}")

if __name__ == '__main__':
    main()
