import logging
import os
import sys
import tarfile
import urllib.request
import subprocess
import shutil
import time
import logging
import requests
from tqdm import tqdm
import glob
from PyQt6 import QtCore, QtWidgets
from urllib.parse import urlparse


logger = logging.getLogger(__name__)
p = os.path.dirname(os.path.abspath(__file__))


def download_large_file(
    url,
    local_filename="",
    progress_dialog=None,
    display_text="Downloading asset :",
    total_mb=None,
    attempts=2,
):
    """Downloads a URL content into a file (with large file support by streaming)

    :param url: URL to download
    :param file_path: Local file name to contain the data downloaded
    :param attempts: Number of attempts
    :return: New file path. Empty string if the download failed
    """
    from celer_sight_ai import config
    from celer_sight_ai import configHandle

    assert local_filename
    if progress_dialog:
        logger.debug(f"Showing window with progress bar with text : {display_text}")
        config.global_signals.loading_dialog_show.emit()
        config.global_signals.loading_dialog_set_text.emit(display_text)
        config.global_signals.loading_dialog_center.emit()
    # if not local_filename:
    #     local_filename = os.path.realpath(os.path.basename(url))
    dest = os.path.join(
        configHandle.getLocal(),
        "update",
        os.path.basename(local_filename),
    )
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    logger.info(f"Downloading {url} content to {dest}")
    url_sections = urlparse(url)

    if not url_sections.scheme:
        logger.debug("The given url is missing a scheme. Adding http scheme")
        url = f"http://{url}".encode("utf-8")
        logger.debug(f"New url: {url}")
    for attempt in range(1, attempts + 1):
        try:
            if attempt > 1:
                logger.debug("Waiting 3 seconds before retrying download")
                time.sleep(3)  # 10 seconds wait time between downloads
            with requests.get(url, stream=True) as response:
                response.raise_for_status()
                if total_mb:
                    total_file_size = total_mb * 1024 * 1024
                else:
                    total_file_size = int(response.headers.get("Content-Length", 0))

                with open(dest, "wb") as out_file:
                    for chunk in response.iter_content(
                        chunk_size=1024 * 1024
                    ):  # 1MB chunks
                        if progress_dialog:
                            config.global_signals.loading_dialog_signal_update_progress_percent.emit(
                                int((out_file.tell() / total_file_size) * 100)
                            )
                        out_file.write(chunk)
                logger.info("Download finished successfully")
                return dest
        except Exception as ex:
            logger.error(f"Attempt #{attempt} failed with error: {ex}")
    return ""


def check_for_updates(just_version=None, channel=None):
    from celer_sight_ai import config

    logger.info("Checking for updates")
    from requests.exceptions import RequestException
    from celer_sight_ai.configHandle import check_has_update_address

    if not config.is_executable:
        if not config.user_cfg["FORCE_UPDATE"]:
            logger.info("Skipping update")
            return False
        logger.info("Forcing update due ot FORCE_UPDATE on config settings")
    if just_version == None:
        logger.info("No version provided, importing form app")
        from celer_sight_ai import __version__

        # get version
        just_version = __version__
    if channel == None:
        logger.info("No channel provided, importing form app")
        from celer_sight_ai import __version__

        # channel is last letter of version
        channel = __version__[-1]
    if config.user_cfg.OVERRIDE_VERSION:
        version = config.user_cfg.OVERRIDE_VERSION_NUMBER
    else:
        version = __version__
    version = just_version + channel
    # make api call to /api/v1/celer_sight_has_update/<string:version>

    has_update_address = check_has_update_address()
    url = f"{has_update_address}/{version}"
    # if system is not mac, check for update, otherwise no update.
    if not os.name == "posix":
        try:
            r = requests.get(url)
            r.raise_for_status()
        except RequestException as e:
            print(f"An error occurred while making the request: {e}")
            return False

        if r.status_code != 200:
            logging.error(f"Checking for updates failed: {r.status_code}")

            return False
        data = r.json()
        if data["message"].lower() == "update available":
            from celer_sight_ai.gui.Utilities.threader import Threader

            t = Threader(download_updates, [data])
            t.start()
            return True
        else:
            return False
    else:
        return False


def download_updates(data):
    from celer_sight_ai import config

    # create a temp dir
    import tempfile
    from celer_sight_ai.configHandle import getLocal, get_update_address

    # Create a folder to download the update to
    local_folder = getLocal()
    tmp_dest_dir = os.path.join(local_folder, "update")

    try:
        if os.path.exists(tmp_dest_dir):
            logger.debug(f"Update dir {tmp_dest_dir} already exists, deleting")
            shutil.rmtree(tmp_dest_dir)
        logger.debug(f"Creating update dir {tmp_dest_dir}")
        os.makedirs(tmp_dest_dir)
    except Exception as e:
        logger.error(f"Error creating update dir {tmp_dest_dir}: {e}")
        return False
    # set the celer sight folder dir
    if config.is_executable:
        dest_dir = p
    elif config.user_cfg["FORCE_UPDATE"]:
        if not os.path.exists(config.user_cfg["FORCE_UPDATE_LOCATION"]):
            logger.error(
                f"FORCE_UPDATE_LOCATION {config.user_cfg['FORCE_UPDATE_LOCATION']} does not exist"
            )
            return False
        dest_dir = config.user_cfg["FORCE_UPDATE_LOCATION"]
    logger.info(f"Update available , downloading to {dest_dir}")
    if "full_update" in data.keys():
        # download full update to "full_update.tar.gz"
        update_name = data["full_update"]
        logger.info(f"Downloading full update {update_name}")
        update_address = get_update_address()
        url = f"{update_address}/{update_name}"

        download_large_file(
            url,
            os.path.join(tmp_dest_dir, "full_update.tar.gz"),
            progress_dialog=True,
            display_text="Downloading update #1/1",
        )

        # once download is finished, move it to celer sight folder

        logger.info(f"Moving update to {dest_dir}")
        shutil.move(
            os.path.join(tmp_dest_dir, "full_update.tar.gz"),
            os.path.join(dest_dir, "full_update.tar.gz"),
        )
    elif "patch" in data.keys():
        # download all updates to "patch_1.tar.gz" then patch_2 etc
        for i, patch in enumerate(data["patch"]):
            update_address = get_update_address()

            url = f"{update_address}/{patch}"
            download_large_file(
                url,
                os.path.join(tmp_dest_dir, patch),
                progress_dialog=True,
                display_text=f"Downloading update #{i+1}/{len(data['patch'])}",
            )
            logger.info(f"Moving update to {dest_dir}")
            shutil.move(
                os.path.join(tmp_dest_dir, patch),
                os.path.join(dest_dir, f"patch_{i}.tar.gz"),
            )

    # set settings as needs_hash_check
    config.settings.setValue("needs_hash_check", "true")

    # close temp dir
    shutil.rmtree(tmp_dest_dir)
    logger.info("Update downloaded, launching updater")
    config.global_signals.update_signal.emit()


# def log_exception(exctype, value, traceback):
#     logging.error("Uncaught exception", exc_info=(exctype, value, traceback))


# # Set the global exception handler
# sys.excepthook = log_exception


logging.info("Importing updater module")
# get parent path

# create a worker process to check if there is an update


def launch_update(*args, **kwargs):
    import subprocess
    from celer_sight_ai import config

    logging.info("Launching update")
    config.global_signals.loading_dialog_set_text.emit(
        "Restarting, please wait for the update to finish.\nCeler Sight will start automatically."
    )
    # wait 2 seconds without blocking the main thread

    config.global_signals.loading_dialog_signal_close.emit()

    new_process = subprocess.Popen(
        [os.path.join(p, "cs_updater_binary.exe")],
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )
    # new_process = subprocess.Popen([os.path.join(p, "updater.exe")], close_fds=True)
    pid = new_process.pid

    # Check if the new process is running
    time.sleep(1)  # Give the new Python process some time to start
    config.global_signals.shut_down_signal.emit()
    sys.exit(0)
    QtWidgets.QApplication.processEvents()


def remove_empty_directories(start_path):
    for root, dirs, files in os.walk(start_path, topdown=False):
        for directory in dirs:
            dir_path = os.path.join(root, directory)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)


def apply_patch_file(app_dir, patch_name):
    logging.info(f"Applying patch file: {patch_name}")
    logging.info(f"App dir: app_dir")
    # Extract the contents of the patch file
    with tarfile.open(os.path.join(app_dir, patch_name), "r:gz") as tar:
        logging.info("Extracting patch file")
        tar.extractall("patch_contents")

    # Remove the files listed in removed_files.txt
    logging.info("Removing files")
    with open(
        os.path.join(app_dir, "patch_contents/removed_files.txt"), "r"
    ) as removed_file:
        for line in removed_file:
            file_path = os.path.join(app_dir, line.strip())
            logging.info("Removing file: %s" % file_path)
            if os.path.exists(file_path):
                os.remove(file_path)

    # Apply added and modified files
    for root, dirs, files in os.walk(os.path.join(app_dir, "patch_contents")):
        for filename in files:
            if filename != "removed_files.txt":
                logging.info("Copying file: %s" % filename)
                rel_path = os.path.relpath(
                    root, os.path.join(app_dir, "patch_contents")
                )
                if rel_path == ".":
                    from_path = os.path.join(app_dir, "patch_contents", filename)
                    to_path = os.path.join(app_dir, filename)
                else:
                    from_path = os.path.join(
                        app_dir, "patch_contents", rel_path, filename
                    )
                    to_path = os.path.join(app_dir, rel_path, filename)

                logging.info(f"To: app_file_loc{to_path}")

                os.makedirs(os.path.dirname(to_path), exist_ok=True)
                shutil.copy2(from_path, to_path)
    logging.info("Removing empty directories")
    remove_empty_directories(".")
    # Remove the patch_contents folder and the patch file
    shutil.rmtree("patch_contents")
    os.remove(os.path.join(app_dir, patch_name))


def main():
    # download_file(patch_url, patch_file)
    logging.info("Starting updater main")
    # get parent directory
    p = os.path.dirname(os.path.abspath(__file__))
    full_update = False
    # get appData local dir
    logging.info(f"Parent dir is {p}")
    if os.path.exists(os.path.join(p, "patch_0.tar.gz")):
        # check to see if ther patch files exists with the pattern patch_*.tar.gz
        all_patch_files = glob.glob(os.path.join(p, "patch_*.tar.gz"))
        logging.info(f"Found patches : {all_patch_files}")
    elif os.path.exists(os.path.join(p, "full_update.tar.gz")):
        all_patch_files = [os.path.join(p, "full_update.tar.gz")]
        full_update = True
        logging.info(f"Found full update")
    else:
        logging.info(f"No Updates")
        sys.exit()
    logging.info(f"Waiting 1 second")
    time.sleep(1.1)
    app_executable = os.path.join(p, "Celer Sight AI.exe")
    logging.info(f"App executable: {app_executable}")

    if full_update:
        files_to_skip = ["cs_updater_binary.exe", "updater.log", "updater.log.1"]
        logging.info(f"Starting full update")
        # try do delete everything in the folder, if something does not get deleted, try renaming it
        # get all files in the folder
        all_files = glob.glob(os.path.join(p, "*"))
        for f in all_files:
            if os.path.basename(f) in files_to_skip:
                logging.info(f"Skipping file {f}")
                continue
            if os.path.isdir(f):
                try:
                    shutil.rmtree(f)
                except Exception as e:
                    logging.error(f"Error deleting folder {f}: {e}")
                    try:
                        os.rename(f, f + "_old")
                    except Exception as e:
                        logging.error(f"Error renaming folder {f}: {e}")
            elif os.path.isfile(f):
                try:
                    os.remove(f)
                except Exception as e:
                    logging.error(f"Error deleting file {f}: {e}")
                    try:
                        os.rename(f, f + "_old")
                    except Exception as e:
                        logging.error(f"Error renaming file {f}: {e}")
    else:
        logging.info(f"Starting patching")

        # Apply the patch
        for patch_file in all_patch_files:
            logging.info(f"Applying patch: {p}")
            apply_patch_file(p, patch_file)

    # Restart the main application
    subprocess.Popen([app_executable], creationflags=subprocess.CREATE_NEW_CONSOLE)


if __name__ == "__main__":
    # parse arguments
    main()
