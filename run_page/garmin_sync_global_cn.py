"""
Python 3 API wrapper for Garmin Connect to get your statistics.
Copy most code from https://github.com/cyberjunky/python-garminconnect
"""

import argparse
import asyncio
import logging
import os
import sys

import httpx
from config import JSON_FILE, SQL_FILE
from config import FIT_FOLDER, GPX_FOLDER
from garmin_sync import Garmin, get_downloaded_ids
from garmin_sync import download_new_activities
# from utils import make_activities_file
from utils import make_activities_file_only


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "cn_secret_string", nargs="?", help="secret_string fro get_garmin_secret.py"
    )
    parser.add_argument(
        "global_secret_string", nargs="?", help="secret_string fro get_garmin_secret.py"
    )
    parser.add_argument(
        "--only-run",
        dest="only_run",
        action="store_true",
        help="if is only for running",
    )

    options = parser.parse_args()
    secret_string_cn = options.cn_secret_string
    secret_string_global = options.global_secret_string
    
    secret_string_global.encode('utf-8').strip()
    b64_string_global = secret_string_global + "=" * (
        (4 - len(secret_string_global) % 4) % 4
    )
    b64_string_cn = secret_string_cn + "=" * ((4 - len(secret_string_cn) % 4) % 4)

    auth_domain = "COM"

    is_only_running = options.only_run
    if secret_string_cn is None or secret_string_global is None:
        print("Missing argument nor valid configuration file")
        sys.exit(1)

    # Step 1:
    # Sync all activities from Garmin CN to Garmin Global in FIT format
    # If the activity is manually imported with a GPX, the GPX file will be synced

    # load synced activity list
    downloaded_fit = get_downloaded_ids(FIT_FOLDER)
    downloaded_gpx = get_downloaded_ids(GPX_FOLDER)
    downloaded_activity = list(set(downloaded_fit + downloaded_gpx))
    
    folder = FIT_FOLDER
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(
        download_new_activities(
            b64_string_global,
            auth_domain,
            downloaded_activity,
            is_only_running,
            folder,
            "fit",
        )
    )
    loop.run_until_complete(future)
    new_ids, id2title = future.result()
    new_ids.sort(key=int, reverse=True)
    nbound = min(100, len(new_ids))
    to_upload_files = []
    for i in new_ids[:nbound]:
        if os.path.exists(os.path.join(FIT_FOLDER, f"{i}.fit")):
            # upload fit files
            to_upload_files.append(os.path.join(FIT_FOLDER, f"{i}.fit"))
        elif os.path.exists(os.path.join(GPX_FOLDER, f"{i}.gpx")):
            # upload gpx files which are manually uploaded to garmin connect
            to_upload_files.append(os.path.join(GPX_FOLDER, f"{i}.gpx"))

    print("Files to sync:" + " ".join(to_upload_files))
    garmin_cn_client = Garmin(b64_string_cn, "CN", is_only_running)
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(
        garmin_cn_client.upload_activities_files(to_upload_files)
    )
    loop.run_until_complete(future)
    print("Garmin CN Sync Finished.")
    
    # Step 2:
    # Generate track from fit/gpx file
    make_activities_file_only(
        SQL_FILE, GPX_FOLDER, JSON_FILE, file_suffix="gpx", activity_title_dict=id2title
    )
    make_activities_file_only(
        SQL_FILE, FIT_FOLDER, JSON_FILE, file_suffix="fit", activity_title_dict=id2title
    )
