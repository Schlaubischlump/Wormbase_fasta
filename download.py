#!/usr/bin/env python3

"""
Download all .genomic.fa.gz files from https://parasite.wormbase.org.
"""

import os
import gzip
import shutil
import urllib
from ftplib import FTP

# Change this to the release number you want to download.
RELEASE = 14

# Unless the server changes, you should not change these entries.
SERVER_URL = "ftp.ebi.ac.uk"
WORKING_DIR = f"pub/databases/wormbase/parasite/releases/WBPS{RELEASE}/species"

# Connect to the ftp server.
ftp = FTP(SERVER_URL)
ftp.login()
ftp.cwd(WORKING_DIR)

i = 0

# iterate over all subfolders
for folder in ftp.nlst():
    for subfolder in ftp.nlst(folder):
        for f in ftp.nlst(subfolder):
            if f.endswith(".genomic.fa.gz"):
                _, filename = f.rsplit("/", 1)
                print(f"[{i}] Downloading file: {filename}...")
                # download the file
                ftp.retrbinary("RETR " + f, open(filename, "wb").write)
                # inform the user
                print(f"[{i}] Downloaded file: {filename}")
                print(f"[{i}] Extracting file: {filename}...")

                # Extract the file
                with gzip.open(filename, 'rb') as f_in:
                    fasta_file_name, _ = filename.rsplit(".", 1)
                    with open(fasta_file_name, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)

                # Remove original .gz file
                os.remove(filename)

                print(f"[{i}] Extracted file: {filename}")
                print()

                i += 1

ftp.quit()
