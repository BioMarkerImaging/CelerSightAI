import json
import logging

# from re import L
# from cryptography.fernet import Fernet
import os
import ssl

import keyring
import requests
from PyQt6 import QtCore

ssl._create_default_https_context = ssl._create_unverified_context

logger = logging.getLogger(__name__)


def get_stored_username():
    usernames = get_recent_users()
    if len(usernames) > 0:
        username = usernames[0]
    else:
        return None
    return username


def get_stored_password(username=None):
    if username is None:
        usernames = get_recent_users()
        if len(usernames) > 0:
            username = usernames[0]
        else:
            return None
    try:
        return keyring.get_password("CelerSight", username)
    except Exception as e:
        logger.error(f"Error getting stored password: {e}")
        return None


def store_username(username):
    try:

        # Get QSettings
        settings = get_app_settings()

        # Get existing usernames list
        recent_users = settings.value("RecentUsers", [], type=list)

        # Remove username if it exists (to avoid duplicates)
        if username in recent_users:
            recent_users.remove(username)

        # Add username to the beginning of the list
        recent_users.insert(0, username)

        # Keep only the last 5 usernames
        recent_users = recent_users[:5]

        # Store updated list
        settings.setValue("RecentUsers", recent_users)

    except Exception as e:
        logger.error(f"Error storing username: {e}")


def get_recent_users():
    settings = get_app_settings()
    return settings.value("RecentUsers", [], type=list)


def store_jwt_token_for_auto_login(jwt_refresh_token):
    logger.info("Storing jwt token for auto login.")
    settings = get_app_settings()
    settings.setValue("last_jwt_refresh_token", jwt_refresh_token)


def get_jwt_token_for_auto_login():
    logger.info("Getting jwt token for auto login.")
    settings = get_app_settings()
    return settings.value("last_jwt_refresh_token", None)


def clear_jwt_token_for_auto_login():
    logger.info("Clearing jwt token for auto login.")
    settings = get_app_settings()
    settings.setValue("last_jwt_refresh_token", None)


def store_password(username, password):
    try:
        # Check if password exists
        if keyring.get_password("CelerSight", username):
            # Delete existing password
            keyring.delete_password("CelerSight", username)
            # Set new password
            keyring.set_password("CelerSight", username, password)
    except Exception as e:
        logger.error(f"Error storing password: {e}")


def delete_user_credentials(username):
    try:
        keyring.delete_password("CelerSight", username)
    except Exception as e:
        logger.error(f"Error deleting user credentials: {e}")


def getLocal():
    """gets the local path to save relevant files

    Returns:
        str: path to the local folder
    """
    local_dir = None
    # if windows platform
    if os.name == "nt":
        local_dir = os.path.expanduser(
            "~\\AppData\\Local\\BioMarkerImaging\\CelerSight"
        )
    else:
        # else is mac os
        local_dir = os.path.join(
            os.path.expanduser("~/Library/Application Support"),
            "BioMarkerImaging",
            "CelerSight",
        )
    if not os.path.exists(os.path.join(local_dir)):
        os.makedirs(os.path.join(local_dir))
    return os.path.join(local_dir)


def getServerLogAddress():
    """Main method to get the server address to connect to

    Returns:
        str: ip address
    """
    if os.environ.get("CELER_SIGHT_TESTING"):
        return "http://localhost:7500"
    elif os.environ.get("CELER_SIGHT_API_IP"):
        return f"{os.environ.get('CELER_SIGHT_API_IP')}"
    else:
        return "https://s1.biomarkerimaging.com"


def retrieve_inference_data_address():
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/infer/retrieve_inference_data"
    else:
        ad = os.path.join(getServerLogAddress(), "api/v1/infer/retrieve_inference_data")
    return ad


def get_refresh_token_address():
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/auth/refresh_token"
    else:
        ad = os.path.join(getServerLogAddress(), "api/v1/auth/refresh_token")
    return ad


def getLogInAddress():
    """The address to log in to the server

    Returns:
        str: url of log in
    """
    # if os is windows
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/auth/login"
    else:
        ad = os.path.join(getServerLogAddress(), "api/v1/auth/login")
    logger.debug(f"Connecting to {ad}")
    return ad


def get_cloud_classes_address():
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/auth/get_cloud_classes"
    else:
        ad = os.path.join(getServerLogAddress(), "api/v1/auth/get_cloud_classes")
    return ad


def get_download_category_map_images_address():
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/auth/download_category_map_images"
    else:
        ad = os.path.join(
            getServerLogAddress(), "api/v1/auth/download_category_map_images"
        )
    return ad


def get_download_asset_address():
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/update/get_asset_url"
    else:
        ad = os.path.join(getServerLogAddress(), "api/v1/update/get_asset_url")
    return ad


def get_available_models_address():
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/auth/get_available_categories"
    else:
        ad = os.path.join(getServerLogAddress(), "api/v1/auth/get_available_categories")
    return ad


def get_create_new_category_address():
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/auth/create_new_category"
    else:
        ad = os.path.join(getServerLogAddress(), "api/v1/auth/create_new_category")
    return ad


def get_optimal_annotation_range_address():
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/infer/get_optimal_annotation_range"
    else:
        ad = os.path.join(
            getServerLogAddress(), "api/v1/infer/get_optimal_annotation_range"
        )
    return ad


def get_remove_category_address():
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/auth/remove_category"
    else:
        ad = os.path.join(getServerLogAddress(), "api/v1/auth/remove_category")
    return ad


def get_user_info_address():
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/auth/get_user_info"
    else:
        ad = os.path.join(getServerLogAddress(), "api/v1/auth/get_user_info")
    return ad


def get_update_category_image_address() -> str:
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/auth/update_category_image"
    else:
        ad = os.path.join(getServerLogAddress(), "api/v1/auth/update_category_image")
    return ad


def get_connect_patreon_address():
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/auth/connect_patreon"
    else:
        ad = os.path.join(getServerLogAddress(), "api/v1/auth/connect_patreon")
    return ad


def get_refresh_patreon_status_address():
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/auth/refresh_patreon_status"
    else:
        ad = os.path.join(getServerLogAddress(), "api/v1/auth/refresh_patreon_status")
    return ad


def get_disconnect_patreon_address():
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/auth/disconnect_patreon"
    else:
        ad = os.path.join(getServerLogAddress(), "api/v1/auth/disconnect_patreon")
    return ad


def get_patreon_status_address():
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/auth/get_patreon_status"
    else:
        ad = os.path.join(getServerLogAddress(), "api/v1/auth/get_patreon_status")
    return ad


def get_celer_sight_latest_full_version_address():
    if os.name == "nt":
        ad = (
            getServerLogAddress() + "/api/v1/update/get_celer_sight_latest_full_version"
        )
    else:
        ad = os.path.join(
            getServerLogAddress(), "api/v1/update/get_celer_sight_latest_full_version"
        )
    return ad


def get_files_hash_list_address():
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/update/get_files_hash_list"
    else:
        ad = os.path.join(getServerLogAddress(), "api/v1/update/get_files_hash_list")
    return ad


def get_update_address():
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/update/get_update"
    else:
        ad = os.path.join(getServerLogAddress(), "api/v1/update/get_update")
    return ad


def get_send_image_inference_address():
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/infer/send_image_inference"
    else:
        ad = os.path.join(getServerLogAddress(), "api/v1/infer/send_image_inference")
    return ad


def get_send_image_annotated_address():
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/contribute/send_image_annotated"
    else:
        ad = os.path.join(
            getServerLogAddress(), "api/v1/contribute/send_image_annotated"
        )
    return ad


def get_send_large_zipped_image_annotated_address():
    if os.name == "nt":
        ad = (
            getServerLogAddress()
            + "/api/v1/contribute/send_large_zipped_image_annotated"
        )
    else:
        ad = os.path.join(
            getServerLogAddress(), "api/v1/contribute/send_large_zipped_image_annotated"
        )
    return ad


def get_send_crash_logs_address():
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/logs_and_feedback/send_crash_logs"
    else:
        ad = os.path.join(
            getServerLogAddress(), "api/v1/logs_and_feedback/send_crash_logs"
        )
    return ad


def get_set_remote_annotation_session_as_audited_address():
    if os.name == "nt":
        ad = (
            getServerLogAddress()
            + "/api/v1/remote_annotation/set_remote_annotation_session_as_audited"
        )
    else:
        ad = os.path.join(
            getServerLogAddress(),
            "api/v1/remote_annotation/set_remote_annotation_session_as_audited",
        )
    return ad


def get_initialize_inference_address():
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/infer/initialize_inference"
    else:
        ad = os.path.join(getServerLogAddress(), "api/v1/infer/initialize_inference")
    return ad


def get_delete_remote_annotation_address():
    if os.name == "nt":
        ad = (
            getServerLogAddress() + "/api/v1/remote_annotation/delete_remote_annotation"
        )
    else:
        ad = os.path.join(
            getServerLogAddress(), "api/v1/remote_annotation/delete_remote_annotation"
        )
    return ad


def get_remote_annotations_for_image_address():
    if os.name == "nt":
        ad = (
            getServerLogAddress()
            + "/api/v1/remote_annotation/get_remote_annotations_for_image"
        )
    else:
        ad = os.path.join(
            getServerLogAddress(),
            "api/v1/remote_annotation/get_remote_annotations_for_image",
        )
    return ad


def get_remote_image_low_address() -> str:
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/remote_annotation/get_remote_image_low"
    else:
        ad = os.path.join(
            getServerLogAddress(), "api/v1/remote_annotation/get_remote_image_low"
        )
    return ad


def get_remote_image_high_address() -> str:
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/remote_annotation/get_remote_image_high"
    else:
        ad = os.path.join(
            getServerLogAddress(), "api/v1/remote_annotation/get_remote_image_high"
        )
    return ad


def get_remote_image_batch_for_annotation():
    # for retrieving images that need annotations
    if os.name == "nt":
        ad = (
            getServerLogAddress()
            + "/api/v1/remote_annotation/get_remote_image_batch_for_annotation"
        )
    else:
        ad = os.path.join(
            getServerLogAddress(),
            "api/v1/remote_annotation/get_remote_image_batch_for_annotation",
        )
    return ad


def get_insert_remote_annotation():
    # for retrieving images that need annotations
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/remote_annotation/insert_annotation"
    else:
        ad = os.path.join(
            getServerLogAddress(),
            "api/v1/remote_annotation/insert_annotation",
        )
    return ad


def get_update_remote_annotation_address() -> str:
    if os.name == "nt":
        ad = (
            getServerLogAddress() + "/api/v1/remote_annotation/update_remote_annotation"
        )
    else:
        ad = os.path.join(
            getServerLogAddress(),
            "api/v1/remote_annotation/update_remote_annotation",
        )
    return ad


def get_check_for_duplicates_address():
    if os.name == "nt":
        ad = getServerLogAddress() + "/api/v1/admin/check_hashed_images"
    else:
        ad = os.path.join(getServerLogAddress(), "api/v1/admin/check_hashed_images")
    return ad


def set_load_from_past_login(load_from_past_login: str) -> None:
    """Method to set the load from past login

    Args:
        load_from_past_login (bool): load from past login
    """
    settings = get_app_settings()
    settings.setValue("LoadFromLastLogIn", load_from_past_login)


def get_app_settings() -> QtCore.QSettings:
    from celer_sight_ai import config

    if not hasattr(config, "qsettings"):
        settings = QtCore.QSettings("BioMarkerImaging", "CelerSight")
        config.qsettings = settings
    return config.qsettings


if __name__ == "__main__":
    pass
