import pandas as pd
import requests

def upload_csv_to_server(file_path, batch_size=1000):
    url = 'http://localhost:3000/api/upload-csv'
   
    # Read the CSV file using pandas
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    # 1. Map the CSV column 'Full Name' to the Supabase column 'team_name'
    if 'Full Name' in df.columns:
        df = df.rename(columns={'Full Name': 'team_name'})
    else:
        print("Error: 'Full Name' column not found in the CSV!")
        return

    # 2. Drop the 'score' column if it exists in the CSV so it uses your database default
    if 'score' in df.columns:
        df = df.drop(columns=['score'])

    # Keep only the columns you actually want to send
    df = df[['team_name']]

    # Clean data (handle NaN values by replacing with None for SQL NULL)
    df = df.where(pd.notnull(df), None)
   
    records = df.to_dict(orient='records')
    print("CSV columns:", df.columns.tolist())
    print("Records:", records[:5])
   
    # Send data in batches to prevent payload size issues
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
       
        try:
            response = requests.post(url, json=batch)
            if response.status_code in (200, 201):
                print(f"Successfully uploaded batch {i // batch_size + 1}: {response.json().get('message')}")
            else:
                print(f"Failed batch {i // batch_size + 1}: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")
            break

if __name__ == '__main__':
    upload_csv_to_server('full_names.csv')