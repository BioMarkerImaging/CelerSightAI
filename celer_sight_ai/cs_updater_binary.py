import logging
import os
import sys
import time
import glob
import shutil
import tarfile
import subprocess
import pyuac
import pathlib
import json

logger = logging.getLogger(__name__)


def try_move_file(source, destination):
    try:
        shutil.move(source, destination)
        True
    except PermissionError:
        False


def try_copy_file(source, destination):
    try:
        shutil.copy2(source, destination)  # copy2 preserves metadata
        True
    except PermissionError:
        False


def try_delete_file(filepath):
    try:
        os.remove(filepath)
        True
    except PermissionError:
        False


def check_if_admin_access_is_needed():
    from celer_sight_ai.configHandle import getLocal

    source = os.path.join(getLocal(), "/test_file.txt")
    p = pathlib.Path(__file__).parent.absolute()
    dest = os.path.join(p, "test_file.txt")
    # create a test_file.txt in the local folder
    with open(source, "w") as f:
        f.write("test")
    # try to copy a file from local to programs
    if not try_copy_file(source, dest):
        return False
    with open(source, "w") as f:
        new_dest = dest.replace(".txt", "_old")
        if not try_move_file(dest, new_dest):
            return False
    if not try_delete_file(new_dest):
        return False


def apply_patch_file(app_dir, patch_name):
    from celer_sight_ai.configHandle import getLocal

    source = os.path.join(getLocal(), "test_file.txt")
    logging.info(f"Applying patch file: {patch_name}")
    logging.info(f"App dir: app_dir")
    # Extract the contents of the patch file
    with tarfile.open(os.path.join(source, patch_name), "r:gz") as tar:
        logging.info("Extracting patch file")
        tar.extractall("patch_contents")

    # Remove the files listed in removed_files.txt
    logging.info("Removing files")
    with open(
        os.path.join(source, "patch_contents/removed_files.txt"), "r"
    ) as removed_file:
        for line in removed_file:
            file_path = os.path.join(app_dir, line.strip())
            logging.info("Removing file: %s" % file_path)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    try:
                        os.rename(file_path, file_path + "_old_for_deletion")
                    except Exception as e:
                        logging.error(e)

    # Apply added and modified files
    for root, dirs, files in os.walk(os.path.join(source, "patch_contents")):
        for filename in files:
            if filename != "removed_files.txt":
                logging.info("Copying file: %s" % filename)
                rel_path = os.path.relpath(root, os.path.join(source, "patch_contents"))
                if rel_path == ".":
                    from_path = os.path.join(source, "patch_contents", filename)
                    to_path = os.path.join(app_dir, filename)
                else:
                    from_path = os.path.join(
                        source, "patch_contents", rel_path, filename
                    )
                    to_path = os.path.join(app_dir, rel_path, filename)

                logging.info(f"To: app_file_loc{to_path}")

                os.makedirs(os.path.dirname(to_path), exist_ok=True)
                try:
                    shutil.copy(from_path, to_path)
                except Exception as e:
                    # if the file exists rename to
                    if os.path.exists(to_path):
                        # rename the file
                        os.rename(to_path, to_path + "_old_for_deletion")
                        try:
                            shutil.copy(from_path, to_path)
                        except Exception as e:
                            logging.error(e)
                    else:
                        logging.error(f"Error copying file: {e}")

    logging.info("Removing empty directories")
    # Remove the patch_contents folder and the patch file
    shutil.rmtree("patch_contents")
    os.remove(os.path.join(source, patch_name))


def main():
    from celer_sight_ai import config
    # download_file(patch_url, patch_file)
    logging.info("Starting updater")
    # get parent directory
    p = os.path.dirname(os.path.abspath(__file__))
    local_file = os.path.join(
        config.getLocal(), "update"
    )
    if not os.path.exists(local_file):
        os.makedirs(local_file)
    full_update = False
    # get appData local dir
    logging.info(f"Parent dir is {p}")
    if os.path.exists(os.path.join(local_file, "patch_0.tar.gz")):
        # check to see if ther patch files exists with the pattern patch_*.tar.gz
        all_patch_files = glob.glob(os.path.join(local_file, "patch_*.tar.gz"))
        logging.info(f"Found patches : {all_patch_files}")
    elif os.path.exists(os.path.join(local_file, "full_update.tar.gz")):
        all_patch_files = [os.path.join(local_file, "full_update.tar.gz")]
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
        files_to_skip = [
            # "updater.exe",
            # "cs_updater_binary.exe",
            # "updater.log",
            # "updater.log.1",
        ]
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
                        os.rename(f, f + "_old_for_deletion")
                    except Exception as e:
                        logging.error(f"Error renaming folder {f}: {e}")
            elif os.path.isfile(f):
                try:
                    os.remove(f)
                except Exception as e:
                    logging.error(f"Error deleting file {f}: {e}")
                    try:
                        os.rename(f, f + "_old_for_deletion")
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
    if not pyuac.isUserAdmin():
        if not check_if_admin_access_is_needed():
            print("Re-launching as admin!")
            pyuac.runAsAdmin()
    else:
        main()
    main()
