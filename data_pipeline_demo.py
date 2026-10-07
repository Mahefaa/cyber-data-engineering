import pandas as pd
import numpy as np

def extract_logs():
    """Simulates extracting raw security logs from a source."""
    print("[*] Extracting raw logs...")
    data = {
        'timestamp': ['2023-10-01 10:00:00', '2023-10-01 10:05:00', 'invalid_time', '2023-10-01 10:15:00'],
        'ip_address': ['192.168.1.10', '10.0.0.5', '192.168.1.10', '256.256.256.256'],
        'status_code': ['200', '404', '500', '200'],
        'bytes_transferred': ['1500', '300', 'NaN', '12000']
    }
    return pd.DataFrame(data)

def transform_logs(df):
    """Cleans and transforms the extracted logs."""
    print("[*] Transforming and cleaning data...")
    
    # Clean timestamps
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    
    # Validate IP addresses (basic regex)
    ip_pattern = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
    df['valid_ip'] = df['ip_address'].str.match(ip_pattern)
    
    # Handle missing or invalid bytes
    df['bytes_transferred'] = pd.to_numeric(df['bytes_transferred'], errors='coerce')
    df['bytes_transferred'] = df['bytes_transferred'].fillna(0) # or mean/median
    
    # Drop rows with invalid critical data
    cleaned_df = df.dropna(subset=['timestamp'])
    cleaned_df = cleaned_df[cleaned_df['valid_ip'] == True]
    
    # Add a feature: High traffic flag
    cleaned_df['is_high_traffic'] = cleaned_df['bytes_transferred'] > 5000
    
    return cleaned_df

def load_logs(df):
    """Simulates loading the cleaned data into a secure data warehouse."""
    print("[*] Loading data into warehouse...")
    print(f"Loaded {len(df)} valid records successfully.")
    return df

if __name__ == "__main__":
    raw_df = extract_logs()
    print("Raw Data:\\n", raw_df)
    
    cleaned_df = transform_logs(raw_df)
    print("\\nCleaned Data:\\n", cleaned_df)
    
    final_df = load_logs(cleaned_df)
