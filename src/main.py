import os
import gzip
import brotli
import mimetypes

def compress_file(filepath, algorithms=['br', 'gz'], brotli_level=6, gzip_level=6):
    """Compresses a file using specified algorithms."""
    content_type, _ = mimetypes.guess_type(filepath)
    if content_type and content_type.startswith(('text/', 'application/javascript', 'application/json', 'application/xml', 'image/svg+xml', 'application/wasm')):
        with open(filepath, 'rb') as f_in:
            content = f_in.read()
        if 'br' in algorithms:
            compressed_filepath_br = filepath + '.br'
            try:
                compressed_content_br = brotli.compress(content, quality=brotli_level)
                with open(compressed_filepath_br, 'wb') as f_out:
                    f_out.write(compressed_content_br)
                print(f"Compressed '{filepath}' to '{compressed_filepath_br}' using Brotli.")
            except Exception as e:
                print(f"Error compressing '{filepath}' with Brotli: {e}")
        if 'gz' in algorithms:
            compressed_filepath_gz = filepath + '.gz'
            try:
                with gzip.open(compressed_filepath_gz, 'wb', compresslevel=gzip_level) as f_out:
                    f_out.write(content)
                print(f"Compressed '{filepath}' to '{compressed_filepath_gz}' using Gzip.")
            except Exception as e:
                print(f"Error compressing '{filepath}' with Gzip: {e}")
    else:
        print(f"Skipping '{filepath}' - Content type '{content_type}' not suitable for compression.")

def process_directory(directory, algorithms, brotli_level, gzip_level):
    """Processes all files in a directory."""
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            compress_file(filepath, algorithms, brotli_level, gzip_level)

if __name__ == "__main__":
    target_directory = os.environ.get("INPUT_DIRECTORY")
    algorithms_str = os.environ.get("INPUT_ALGORITHMS", "br,gz")
    brotli_level = int(os.environ.get("INPUT_BROTLI_LEVEL", "6"))
    gzip_level = int(os.environ.get("INPUT_GZIP_LEVEL", "6"))

    if not target_directory:
        print("Error: 'directory' input is required.")
    elif not os.path.isdir(target_directory):
        print(f"Error: Directory '{target_directory}' not found.")
    else:
        algorithms_list = [alg.strip() for alg in algorithms_str.split(',')]
        print(f"Processing directory: {target_directory}")
        process_directory(target_directory, algorithms_list, brotli_level, gzip_level)
        print("Compression complete.")