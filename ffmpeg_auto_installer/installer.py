import os
import subprocess
import zipfile
import logging
import urllib.request
import time
from urllib.error import URLError, HTTPError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(handler)

def ensure_ffmpeg():
    def is_ffmpeg_installed():
        try:
            subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

    def download_ffmpeg_with_retries(url, dest, max_retries=3, wait_secs=3):
        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"Attempt {attempt}: Downloading ffmpeg from {url}")
                urllib.request.urlretrieve(url, dest)
                logger.info("Download successful.")
                return True
            except (URLError, HTTPError) as e:
                logger.warning(f"Download failed: {e}. Retrying in {wait_secs} seconds...")
                time.sleep(wait_secs)
        logger.error("All retries failed. Could not download ffmpeg.")
        return False

    def extract_ffmpeg(zip_path, extract_to):
        try:
            logger.info(f"Extracting {zip_path} to {extract_to}...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            logger.info("Extraction complete.")
            return True
        except zipfile.BadZipFile as e:
            logger.error(f"Failed to extract zip: {e}")
            return False

    def find_and_set_ffmpeg_bin(extract_root):
        for root, dirs, files in os.walk(extract_root):
            if "ffmpeg.exe" in files:
                bin_path = root
                os.environ["PATH"] = bin_path + os.pathsep + os.environ["PATH"]
                logger.info(f"ffmpeg found and PATH updated for this session: {bin_path}")
                return True
        logger.error("ffmpeg.exe not found in extracted folders.")
        return False

    logger.info("Checking if ffmpeg is already installed...")
    if is_ffmpeg_installed():
        logger.info("ffmpeg is already available.")
        return

    logger.warning("ffmpeg not found. Proceeding to download and setup...")

    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_filename = "ffmpeg.zip"
    extract_dir = os.path.abspath("ffmpeg_setup")

    if not download_ffmpeg_with_retries(ffmpeg_url, zip_filename):
        raise RuntimeError("Failed to download ffmpeg after multiple attempts.")
    if not extract_ffmpeg(zip_filename, extract_dir):
        raise RuntimeError("Failed to extract ffmpeg zip file.")
    if not find_and_set_ffmpeg_bin(extract_dir):
        raise RuntimeError("ffmpeg.exe not found in extracted files.")

    if is_ffmpeg_installed():
        logger.info("ffmpeg is now set up and ready to use.")
    else:
        raise RuntimeError("ffmpeg setup failed even after download and extraction.")
