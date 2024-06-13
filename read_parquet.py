import os
import gdown
import zipfile
import pandas as pd
import argparse


#example in how can it be run 
#python read_parquet_file.py 1s0irIrngQVeRDXY8F5gizkttG9Rqshg0


# Function to download a file from Google Drive
def download_file_from_google_drive(file_id, destination):
    url = f"https://drive.google.com/file/d/{file_id}/view"
    gdown.download(url, destination, quiet=False, fuzzy=True)

# Function to unzip a ZIP file
def unzip_file(zip_file, extract_to='.'):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def main(file_id):
    # Name of the destination file
    destination = 'file.zip'

    # Download the file
    download_file_from_google_drive(file_id, destination)

    # Unzip the downloaded file
    unzip_file(destination)

    # Navigate to the 'data' folder
    data_folder = 'data/'

    # Ensure that the 'data' folder exists
    if not os.path.exists(data_folder):
        print(f"The folder '{data_folder}' does not exist.")
    else:
        # Get a list of all files with the .snappy.parquet extension in the data folder
        parquet_files = [f for f in os.listdir(data_folder) if f.endswith(".snappy.parquet")]

        # Read each file into a Pandas DataFrame and concatenate them
        df = pd.concat([pd.read_parquet(os.path.join(data_folder, f)) for f in parquet_files])

        # Print the DataFrame
        print(df)

        # Save the DataFrame as a CSV file
        df.to_csv("celes.csv", index=False, sep=",")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download, unzip, and process parquet files.')
    parser.add_argument('file_id', type=str, help='Google Drive file ID to download')
    args = parser.parse_args()

    main(args.file_id)
