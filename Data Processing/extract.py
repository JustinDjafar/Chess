# ------------------------------------------------------------------------------------
# Decompress and Split Large Lichess .zst Files (.pgn.zst format)
#
# Description:
# This script is designed to run in Google Colab. It mounts your Google Drive, reads a 
# large Lichess .pgn.zst (Zstandard-compressed PGN) file directly from Drive, and 
# decompresses it into multiple smaller `.pgn` files (split by size) back into Drive.
# Displays progress with the tqdm libraries as decompressed file reached up to 200gb
#
# Input
# - A `.pgn.zst` file (e.g., `lichess_db_standard_rated_2024-10.pgn.zst`) stored in Drive.
#
# Output
# - Multiple decompressed `.pgn` files, saved in a target directory within Drive.
# - Each decompressed file is limited to 5gb to decrease colab disk usage
#
# Requirements:
# - zstandard
# - tqdm
# - google.colab
#
# Example use case:
# Use this after downloading Lichess database files in .zst format, to prepare data
# for further training or analysis (e.g., training a chess engine or ML model).
# ------------------------------------------------------------------------------------

import os
import zstandard as zstd
from tqdm import tqdm
from google.colab import drive
drive.mount('/content/drive')

def stream_decompress_and_split(input_zst_path, output_dir, max_chunk_size_gb=5, read_chunk_size=1024*1024):
    os.makedirs(output_dir, exist_ok=True)
    max_chunk_size_bytes = max_chunk_size_gb * 1024**3

    total_size = os.path.getsize(input_zst_path)
    print(f"Input .zst file size: {total_size / (1024**3):.2f} GB")

    dctx = zstd.ZstdDecompressor()

    with open(input_zst_path, 'rb') as compressed_file, tqdm(total=total_size, unit='B', unit_scale=True, desc='Decompressing') as pbar:
        reader = dctx.stream_reader(compressed_file)

        file_index = 1
        bytes_written = 0
        output_path = os.path.join(output_dir, f"lichess_part_{file_index:02d}.pgn")
        output_file = open(output_path, 'wb')

        while True:
            chunk = reader.read(read_chunk_size)
            if not chunk:
                break

            output_file.write(chunk)
            bytes_written += len(chunk)
            pbar.update(len(chunk))

            if bytes_written >= max_chunk_size_bytes:
                output_file.close()
                print(f"Saved: {output_path} ({bytes_written / (1024**3):.2f} GB)")
                file_index += 1
                output_path = os.path.join(output_dir, f"lichess_part_{file_index:02d}.pgn")
                output_file = open(output_path, 'wb')
                bytes_written = 0

        output_file.close()
        print(f"Saved: {output_path} ({bytes_written / (1024**3):.2f} GB)")

    print("✅ Decompression and splitting complete.")


input_zst_path = "/content/drive/MyDrive/Chess/lichess_db_standard_rated_2024-10.pgn.zst"
output_dir = "/content/drive/MyDrive/Chess/split_pgn_files_2024_10"
stream_decompress_and_split(input_zst_path, output_dir, max_chunk_size_gb=5)