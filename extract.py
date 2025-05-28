import os
import zstandard as zstd

def decompress_zst_to_pgn(input_path, output_path):
    print(f"Decompressing:\n{input_path} → {output_path}")
    
    with open(input_path, 'rb') as compressed_file:
        dctx = zstd.ZstdDecompressor()
        with open(output_path, 'wb') as output_file:
            dctx.copy_stream(compressed_file, output_file)
    
    print("Decompression complete.")

input_zst_path = "lichess_db_standard_rated_2025-03.pgn.zst"
output_pgn_path = "lichess_2025_03.pgn"

decompress_zst_to_pgn(input_zst_path, output_pgn_path)
