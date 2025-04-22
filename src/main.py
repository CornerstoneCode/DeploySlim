import os
import gzip
import brotli
import mimetypes
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import logging
import minify_html
from csscompressor import compress as css_compress
from jsmin import jsmin
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

COMPRESSIBLE_TYPES = {
    'text/html', 'text/css', 'text/plain', 'text/xml',
    'application/javascript', 'application/json',
    'application/xml', 'image/svg+xml', 'application/wasm',
    'font/woff', 'font/woff2', 'application/manifest+json'
}
COMPRESSIBLE_EXTENSIONS = {
    '.html', '.css', '.js', '.json', '.xml', '.svg', '.wasm',
    '.txt', '.woff', '.woff2', '.webmanifest', '.png', '.jpg', '.jpeg', '.webp'
}

def is_compressible_file(filepath: str) -> bool:
    path = Path(filepath)
    if not path.is_file() or path.stat().st_size == 0:
        return False
    if path.suffix.lower() in COMPRESSIBLE_EXTENSIONS:
        return True
    content_type, _ = mimetypes.guess_type(filepath)
    return content_type in COMPRESSIBLE_TYPES

def minify_file(filepath: str) -> None:
    ext = Path(filepath).suffix.lower()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        if ext == '.html':
            minified = minify_html.minify(
                content,
                minify_js=True,
                minify_css=True,
                remove_bangs=True,
                remove_comments=True,
                keep_closing_tags=True
            )
        elif ext == '.css':
            minified = css_compress(content)
        elif ext == '.js':
            minified = jsmin(content)
        else:
            return
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(minified)
        logger.info(f"Minified {filepath}")
    except Exception as e:
        logger.error(f"Minification failed for {filepath}: {e}")

def optimize_image(filepath: str) -> None:
    ext = Path(filepath).suffix.lower()
    try:
        img = Image.open(filepath)
        if ext in ('.png', '.jpg', '.jpeg'):
            img.save(filepath, optimize=True, quality=85)
        elif ext == '.webp':
            img.save(filepath, 'WEBP', quality=80)
        logger.info(f"Optimized image {filepath}")
    except Exception as e:
        logger.error(f"Image optimization failed for {filepath}: {e}")

def compress_file(filepath: str, algorithms: list, brotli_level: int, gzip_level: int, do_minify: bool, do_optimize_images: bool) -> dict:
    if not is_compressible_file(filepath):
        return {'original': 0, 'br': 0, 'gz': 0}

    if do_minify and Path(filepath).suffix.lower() in ('.html', '.css', '.js'):
        minify_file(filepath)
    if do_optimize_images and Path(filepath).suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp'):
        optimize_image(filepath)

    original_size = os.path.getsize(filepath)
    results = {'original': original_size, 'br': 0, 'gz': 0}

    if 'br' in algorithms:
        br_path = f"{filepath}.br"
        try:
            with open(filepath, 'rb') as f_in:
                content = f_in.read()
            with open(br_path, 'wb') as f_out:
                f_out.write(brotli.compress(content, quality=brotli_level))
            results['br'] = os.path.getsize(br_path)
            logger.info(f"Compressed {filepath} to {br_path} ({results['br']} bytes)")
        except Exception as e:
            logger.error(f"Brotli compression failed for {filepath}: {e}")

    if 'gz' in algorithms:
        gz_path = f"{filepath}.gz"
        try:
            with gzip.open(gz_path, 'wb', compresslevel=gzip_level) as f_out:
                with open(filepath, 'rb') as f_in:
                    f_out.write(f_in.read())
            results['gz'] = os.path.getsize(gz_path)
            logger.info(f"Compressed {filepath} to {gz_path} ({results['gz']} bytes)")
        except Exception as e:
            logger.error(f"Gzip compression failed for {filepath}: {e}")

    return results

def process_file(filepath: str, algorithms: list, brotli_level: int, gzip_level: int, minify: bool, optimize_images: bool) -> dict:
    """Wrapper function to call compress_file, picklable for ProcessPoolExecutor."""
    return compress_file(filepath, algorithms, brotli_level, gzip_level, minify, optimize_images)

def process_directory(directory: str, algorithms: list, brotli_level: int, gzip_level: int, minify: bool, optimize_images: bool) -> None:
    files = [
        os.path.join(root, filename)
        for root, _, files in os.walk(directory)
        for filename in files
        if is_compressible_file(os.path.join(root, filename))
    ]

    if not files:
        logger.info("No files to process.")
        return

    total_original = 0
    total_compressed_br = 0
    total_compressed_gz = 0

    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        results = list(executor.map(
            process_file,
            files,
            [algorithms] * len(files),
            [brotli_level] * len(files),
            [gzip_level] * len(files),
            [minify] * len(files),
            [optimize_images] * len(files)
        ))

    for result in results:
        total_original += result['original']
        total_compressed_br += result['br']
        total_compressed_gz += result['gz']

    logger.info(
        f"Summary:\n"
        f"- Files processed: {len(files)}\n"
        f"- Original size: {total_original} bytes\n"
        f"- Brotli size: {total_compressed_br} bytes\n"
        f"- Gzip size: {total_compressed_gz} bytes"
    )

if __name__ == "__main__":
    directory = os.environ.get("INPUT_DIRECTORY", ".")
    algorithms = os.environ.get("INPUT_ALGORITHMS", "br,gz").split(',')
    brotli_level = int(os.environ.get("INPUT_BROTLI_LEVEL", "11"))
    gzip_level = int(os.environ.get("INPUT_GZIP_LEVEL", "9"))
    minify = os.environ.get("INPUT_MINIFY", "true").lower() == "true"
    optimize_images = os.environ.get("INPUT_OPTIMIZE_IMAGES", "true").lower() == "true"

    if not os.path.isdir(directory):
        logger.error(f"Invalid directory: {directory}")
        exit(1)

    logger.info(f"Processing directory: {directory}")
    process_directory(directory, algorithms, brotli_level, gzip_level, minify, optimize_images)
    logger.info("Processing complete.")