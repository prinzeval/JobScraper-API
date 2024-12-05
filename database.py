import pandas as pd
from supabase import create_client, Client
import os

# Supabase credentials
url = "https://qfwipzqywzjqoxzvrlxt.supabase.co"  # Replace with your Supabase URL
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFmd2lwenF5d3pqcW94enZybHh0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjAyNzQ1NzksImV4cCI6MjAzNTg1MDU3OX0.067C1RDQsklIyPs8Hr8eH5N-pu5jJ2pqV4wTZkcrbkM"  # Replace with your Supabase key

# Initialize Supabase client
supabase: Client = create_client(url, key)

# Path to CSV file
csv_file_path = r'C:\Users\valen\Desktop\JOB-WEBSITE\output.csv'  # Replace with your CSV file path

# Check if the file exists
if not os.path.isfile(csv_file_path):
    print(f"Error: The file '{csv_file_path}' does not exist.")
else:
    try:
        # Read CSV file
        df = pd.read_csv(csv_file_path)

        # Check if the DataFrame is empty
        if df.empty:
            print("Error: The CSV file is empty.")
        else:
            # Ensure the DataFrame column names match the Supabase table
            df.columns = ['POSITION', 'COMPANY NAME', 'LOCATION', 'SALARY', 'JOB LINK', 'BENEFITS', 'DESCRIPTION', 'EMPLOYMENT TYPE']

            # Convert all DataFrame values to strings and handle NaN
            df = df.astype(str).replace('nan', '')

            # Print the first few rows and column names for debugging
            print("DataFrame columns:", df.columns)
            print("First few rows of the DataFrame:")
            print(df.head())

            # Table name in Supabase
            table_name = 'Job_listing'

            # Convert DataFrame to dictionary and insert into Supabase
            records = df.to_dict(orient='records')

            try:
                # Perform insert operation
                response = supabase.table(table_name).insert(records).execute()
                print("Insert response:", response.data)
            except Exception as e:
                print("Error inserting records:", e)
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty or cannot be read.")
    except Exception as e:
        print("Error reading the CSV file:", e)
