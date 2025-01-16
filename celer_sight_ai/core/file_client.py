import asyncio
import functools
import json
import os
import pathlib
import random
import string
import threading
import time
from concurrent import futures
from typing import Any, Callable, Dict, List, Tuple, Union

import cv2
from PyQt6 import QtCore, QtGui, QtWidgets

from celer_sight_ai import config
from celer_sight_ai.core import LogTool

CDIR = str(pathlib.Path(__file__).parent.absolute())
CHUNK_SIZE = 1024 * 1024  # 1 MB
import json
import logging
import os
import time
from typing import Optional, Tuple

from PyQt6 import QtCore
from requests.exceptions import HTTPError

from celer_sight_ai import config, configHandle
from celer_sight_ai.configHandle import getLocal
from celer_sight_ai.core.threader import Threader

logger = logging.getLogger(__name__)
import threading

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import celer_sight_ai.configHandle as configHandle


class AuthenticationError(Exception):
    pass


class OfflineModeException(Exception):
    pass


def GenerateRandomTokken(stringLength=100):
    """
    Generates random ID for users
    """
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(password_characters) for i in range(stringLength))


def get_file_chunks_usrID_imgID(filename, extr1=None, extr2=None):
    """This is a method to read chunks of two files at the same time
        for this case, the user ID and image ID

    Args:
        filename (str): path to the file to be read
        extr1 (str, optional): username. Defaults to None.
        extr2 (str, optional): image ID. Defaults to None.

    Yields:
        bytes: byte of either user id or image id
    """
    raise NotImplementedError
    # with open(filename, 'rb') as f:
    #     itr = 0
    #     while True:
    #         piece = f.read(CHUNK_SIZE)
    #         if len(piece) == 0:
    #             return
    #         if itr == 0:
    #             yield chunk_pb2.ChunkWithID(buffer=piece, User=extr1, ImId=extr2)
    #             continue
    #         yield chunk_pb2.ChunkWithID(buffer=piece, User=None, ImId=None)
    #         itr += 1


def save_chunks_to_file(chunks, filename, progress_callback=None):
    """Writes the chunks to a file

    Args:
        chunks (byte): the chunks to be written
        filename (str): where the bytes are writen to
        progress_callback (callback, optional): callback for the progress. Defaults to None.
    """
    raise NotImplementedError
    with open(filename, "wb") as f:
        for Mychunk in chunks:
            f.write(Mychunk.buffer)


def ping_endpoint(endpoint_url, max_interval=4.0, start_interval=0.5, timeout=60):
    interval = start_interval
    elapsed_time = 0
    start_time = time.time()

    while elapsed_time < timeout:
        try:
            response = requests.get(endpoint_url)
            response.raise_for_status()  # Raise an error for bad HTTP status codes

            # Check if response contains results (you can customize this logic)
            if response.json().get("results"):
                print("Results found!")
                return response.json()
            else:
                print(f"No results yet, waiting {interval} seconds before retrying...")

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

        time.sleep(interval)
        interval = min(interval * 2, max_interval)
        elapsed_time = time.time() - start_time

    print("Timeout reached, no results found.")
    return None


def save_chunks_to_file_APP_LINK(
    chunks, filename, progress_callback=None, maxSize=None
):
    """Method to write the file chunks to a file, this is for the .csfl file located
    on the server sent by the mobile application

    Args:
        chunks (bytes): bytes of the .csfl file
        filename (str): path to the file to be written
    """
    raise NotImplementedError
    totMB = 0
    totIt = 1
    updateEvery = 100
    mB = 1024 * 1024
    from celer_sight_ai import config

    with open(filename, "wb") as f:
        for Mychunk in chunks:
            f.write(Mychunk.buffer)
            if totIt % updateEvery == 0:
                config.global_signals.setSplashText.emit(
                    "Fetching file: "
                    + str(int((((totIt * CHUNK_SIZE) / mB) / maxSize) * 100))
                    + " %"
                )
            totIt = totIt + 1


def SaveCredentialsToFile(Username, PassWord, Email, FirstName, LastName, Organization):
    # Runs from user to the server to save the send file
    print(Username)
    return


def html2text(html):
    doc = QtGui.QTextDocument()
    doc.setHtml(html)
    return doc.toPlainText()


class FileClient:
    _instance = None

    def __new__(cls, address_override=None, MainWindow=None):
        if cls._instance is None:
            cls._instance = super(FileClient, cls).__new__(cls)
            cls._instance.jwt = None  # short lived access token
            cls._instance.jwt_long = None  # long lived access token
            cls._instance.session = cls.create_retry_session()  # Use retry session
        if MainWindow:
            cls._instance.MainWindow = MainWindow
        cls._instance.mainAddr = configHandle.getServerLogAddress()
        return cls._instance

    @staticmethod
    def create_retry_session(
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504),
    ):
        session = requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def __init__(self, address_override=None, MainWindow=None) -> None:
        # get biomarkerimaging address
        if MainWindow:
            self.MainWindow = MainWindow
        self.images_being_sent = 0  # images being sent for inference to the server
        config.global_signals.update_remote_annotation_signal.connect(
            self.update_remote_annotation
        )

    def is_jwt_expired(self, jwt):
        """
        Check if a JWT token has expired.

        Args:
            jwt (str): The JWT token to check

        Returns:
            bool: True if token is expired or invalid, False otherwise
        """
        if not jwt:
            return True

        try:
            # JWT tokens have 3 parts separated by dots
            parts = jwt.split(".")
            if len(parts) != 3:
                return True

            # Decode the payload (middle part)
            import json
            import time
            from base64 import b64decode

            # Add padding if needed
            payload = parts[1]
            padding = 4 - (len(payload) % 4)
            if padding != 4:
                payload += "=" * padding

            # Decode payload and parse JSON
            decoded = b64decode(payload)
            payload_data = json.loads(decoded)

            # Check expiration time
            exp = payload_data.get("exp")
            if not exp:
                return True

            return time.time() > exp

        except Exception as e:
            logger.warning(f"Error checking JWT expiration: {e}")
            return True

    def login_required(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if config.user_cfg["OFFLINE_MODE"] == True:
                config.global_signals.errorSignal.emit(
                    "This feature is not available in offline mode."
                )
                raise OfflineModeException(
                    "This feature is not available in offline mode."
                )

            # Check if JWT exists and is not expired
            if self.jwt is None or self.is_jwt_expired(self.jwt):
                # First try to refresh the token if we have a refresh token
                if hasattr(self, "jwt_refresh") and self.jwt_refresh:
                    try:
                        self.refresh_token()
                    except AuthenticationError:
                        # If refresh fails, attempt full login, with UI
                        # Attempt to log in with UI
                        login_handler = LogTool.LogInHandler(
                            is_main_window_launched=True
                        )
                        login_handler.exec()
                        # check if we managed to log in by checking the jwt token
                        if self.jwt is None or self.is_jwt_expired(self.jwt):
                            config.global_signals.errorSignal.emit(
                                "There has been an authentication error. Please try again."
                            )
                            return

            # Execute the function
            try:
                return func(self, *args, **kwargs)
            # if the error is 401, which is authentication error
            except AuthenticationError:
                # If an authentication error occurred, set self.jwt to None and attempt to log in again
                self.jwt = None
                self.session = requests.Session()
                # add bearer token
                self.session.headers["Authorization"] = f"Bearer {self.jwt}"
                result = self.login()
                if "error" in result:
                    config.global_signals.errorSignal.emit(result["error"])
                    return
                return func(self, *args, **kwargs)

        return wrapper

    def refresh_token(self):
        refresh_address = configHandle.get_refresh_token_address()
        response = self.session.post(
            refresh_address, headers={"Authorization": f"Bearer {self.jwt_refresh}"}
        )
        response.raise_for_status()
        self.jwt = response.json().get("JWT")
        self.jwt_refresh = response.json().get("JWT_refresh")
        self.session.headers.update({"Authorization": f"Bearer {self.jwt}"})

    def is_logged_in(self):
        """Checks if the user is logged, in. To save bandwidth, we only check if the jwt is not None"""
        if not self.jwt:
            return False
        if self.is_jwt_expired(self.jwt):
            return False
        # check refresh token
        if not self.jwt_refresh:
            return False
        if self.is_jwt_expired(self.jwt_refresh):
            return False
        return True

    def login_request(self, username, password, jwt_refresh_token=None):
        """
        Send a login request to the server with the provided credentials.

        Args:
            username (str): The username of the user trying to log in.
            password (str): The password for the user.
            jwt_refresh_token (str, optional): The refresh token for the user. Defaults to None.

        Returns:
            tuple: A tuple containing (response, exception).
                   If successful, response is the server response and exception is None.
                   If failed, response is None and exception contains the error message.
        """
        from celer_sight_ai import config

        data = {
            "User": username,
            "Pass": password,
            "jwt_refresh_token": jwt_refresh_token,
        }
        url = configHandle.getLogInAddress()
        timeout = 7 if config.is_executable else 30

        try:
            response = self.session.post(
                url,
                headers={"Content-Type": "application/json"},
                json=data,
                verify=True,  # Consider enabling SSL verification in production
                timeout=timeout,
            )
            response.raise_for_status()  # Raise an exception for HTTP errors

            jwt = response.json().get("JWT")
            if jwt:
                self.jwt = jwt
                self.session.headers.update(
                    {"x-access-token": jwt, "Authorization": f"Bearer {jwt}"}
                )
            return response, None

        except requests.exceptions.Timeout:
            return None, "Request timed out. Please try again later."
        except requests.exceptions.RequestException as e:
            if hasattr(e, "response"):
                if 500 <= e.response.status_code < 600:
                    return None, "Cant reach server. Please try again later."
                elif e.response.status_code == 404:
                    return (
                        None,
                        "Server not found. Please check your network connection.",
                    )
                elif e.response.status_code == 429:
                    return None, "Too many requests. Please try again later."
                elif e.response.status_code:
                    return None, e.response.text
                return None, e.response.text
            else:
                return None, str(e)
        # The following code is unreachable due to the try-except block above
        # return None, None

    def login(
        self,
        username: str = None,
        password: Optional[str] = None,
        jwt_refresh_token: Optional[str] = None,
    ) -> dict[str, str] | Any:
        logger.debug("Login started")

        username, password = self._get_credentials(username, password)
        if not username or (not password and not jwt_refresh_token):
            self._handle_empty_credentials()
            return {"error": "Login attempt with empty credentials"}

        settings = QtCore.QSettings(config.SETTINGS_ORG, config.SETTINGS_APP)
        config.user_attributes.username = username

        self._update_last_save_directory(settings)

        try:
            return_val, exc = self.login_request(username, password, jwt_refresh_token)
            status_code = return_val.status_code if return_val else 200
        except Exception as e:
            logger.error(f"Error getting status code from return_val: {e}")
            self._stop_login_spinner()
            return {
                "error": "Can't establish connection to the server. Please try again later."
            }

        if exc or not 200 == status_code:
            return self._handle_login_error(exc, status_code)

        response_json = return_val.json()
        self._update_jwt_tokens(response_json)
        self._update_cloud_categories(response_json, settings)
        self._update_user_attributes(response_json)
        self._stop_login_spinner()
        return response_json

    def _get_credentials(
        self, username: Optional[str], password: Optional[str]
    ) -> Tuple[Optional[str], Optional[str]]:
        if username is None:
            username = config.user_attributes.username
        if password is None:
            password = config.user_attributes.password
        return username, password

    def _handle_empty_credentials(self):
        """
        Handle the case when login credentials are empty.

        This method sets the login state to false and emits a signal to stop the login spinner.
        """
        self.during_log_in = False
        config.global_signals.stop_log_in_spinner.emit()
        logger.warning("Login attempt with empty credentials")

    def _update_last_save_directory(self, settings: QtCore.QSettings):
        """
        Update the last save directory settings if not already set.

        Args:
            settings (QtCore.QSettings): The application settings object.
        """
        last_save_directory_bool = settings.value(
            "LastSaveDirectoryBOOL", "false"
        ).lower()
        if last_save_directory_bool != "true":
            logger.info("Updating last save directory settings")
            settings.setValue("LastSaveDirectoryBOOL", "true")
            settings.setValue("LastSaveDirectory", os.path.expanduser("~"))

    def _stop_login_spinner(self):
        config.global_signals.stop_log_in_spinner.emit()

    def _handle_login_error(self, exc=None, status_code=500):
        logger.error(f"Login error: {exc}, Status code: {status_code}")
        self._stop_login_spinner()
        if status_code >= 500:
            return {
                "error": f"There was an error on the server side, status code {status_code}."
            }
        elif 400 < status_code < 500:
            return {
                "error": f"There was an error on the client side, status code {status_code}."
            }
        return {"error": str(exc) if exc else "Unknown error occurred during login."}

    def _update_jwt_tokens(self, response_json: dict):
        if "JWT" in response_json:
            self.jwt = response_json["JWT"]
            self.jwt_refresh = response_json["JWT_refresh"]
            self.session.headers.update({"Authorization": f"Bearer {self.jwt}"})
        else:
            logger.debug("Did not get a JWT refresh token back.")

    def _update_cloud_categories(self, response_json: dict, settings: QtCore.QSettings):
        config.cloud_categories = response_json["organism_map"]
        self._refresh_categories_if_needed(settings)
        self._save_cloud_organism_map(response_json["organism_map"])

    def _refresh_categories_if_needed(self, settings: QtCore.QSettings):
        last_refresh = settings.value("RefreshedCategoriesTime", None)
        self._clear_cloud_categories()
        settings.setValue("RefreshedCategoriesTime", int(time.time()))

    def _clear_cloud_categories(self):
        logger.info("Clearing out the cloud folder of categories and refreshing them.")
        if os.path.exists(
            os.path.join(configHandle.getLocal(), config.CLOUD_CATEGORIES_FILE)
        ):
            os.remove(
                os.path.join(configHandle.getLocal(), config.CLOUD_CATEGORIES_FILE)
            )

    def _save_cloud_organism_map(self, organism_map: list):
        logger.info(f"Saving cloud organism map to {config.CLOUD_CATEGORIES_FILE}")
        organism_map_path = os.path.join(
            configHandle.getLocal(), config.CLOUD_CATEGORIES_FILE
        )
        os.makedirs(os.path.dirname(organism_map_path), exist_ok=True)
        if not [i for i in organism_map if i["supercategory"] == "tissue"]:
            print()
        with open(organism_map_path, "w") as f:
            json.dump(organism_map, f)

    def _update_user_attributes(self, response_json: dict):
        config.cloud_user_variables = response_json
        if "license" in response_json:
            config.user_attributes.license = response_json["license"]
        config.user_attributes.lab_uuid = response_json.get("lab")
        config.user_attributes.is_admin = response_json.get("isAdmin", False)

    def connect_patreon(self, click_state=None):
        """Connect to Patreon via OAuth2"""
        import webbrowser

        from celer_sight_ai.configHandle import get_connect_patreon_address

        try:
            # Get the authorization URL from the server
            url = get_connect_patreon_address()
            response = self.session.get(url)

            response.raise_for_status()
            auth_url = response.json().get("url")
            if not auth_url:
                config.global_signals.errorSignal.emit("Failed to connect to Patreon.")
            # Open the authorization URL in browser
            if auth_url:
                import urllib

                state = urllib.parse.quote(self.jwt)
                webbrowser.open(auth_url + f"&state={state}")
            else:
                raise Exception("No authorization URL received from server")

        except Exception as e:
            logger.error(f"Failed to connect to Patreon: {str(e)}")
            raise e

    def disconnect_patreon(self, click_state=None):
        from celer_sight_ai.configHandle import get_disconnect_patreon_address

        url = get_disconnect_patreon_address()
        response = self.session.post(url)
        response.raise_for_status()

    @login_required
    def get_patreon_status(self):
        from celer_sight_ai.configHandle import get_patreon_status_address

        url = get_patreon_status_address()
        response = self.session.get(url)
        response.raise_for_status()
        # store patreon latest status in user config

        return response.json()

    @config.threaded
    def download_assets(self, force_download=False):
        from functools import partial

        try:
            # assets are a list of filenames to download. For each file
            # request a SAS link and download the file
            parent_path = os.path.join(configHandle.getLocal(), "mats/mgb")
            assets_for_download = {
                "general_encoder": parent_path,
                "general_decoder": parent_path,
                "specialized": parent_path,
            }

            # iterate over assets retrieved from log in and check if any of them need updatating
            assets_to_ignore = []
            # check witch assets need to be downloaded
            for asset, path in assets_for_download.items():
                # every asset has the following name : assetName_{version} and no extension
                asset_version_name = config.get_latest_file_version(path, asset)
                if asset_version_name:
                    # check if the asset is up to date
                    asset_version = asset_version_name.split("_")[-1]
                    if not config.user_cfg["OFFLINE_MODE"]:
                        if (
                            asset_version
                            == config.cloud_user_variables["assets"][asset]
                        ):
                            # asset is up to date
                            assets_to_ignore.append(asset)
                    else:
                        assets_to_ignore.append(
                            asset
                        )  # assume we are on the latest version
                else:
                    # download the asset
                    continue

            # remove assets that dont need downloading / updating
            for asset in assets_to_ignore:
                del assets_for_download[asset]
            if len(assets_for_download) == 0:
                logger.info("No assets to download")
                return
            # in case assets are needed, ask the user to confirm
            if not force_download:
                config.global_signals.actionDialogSignal.emit(
                    "Found missing assets. Downloading assets will take a while\nbut its required for the app to work properly.\nContinue?",
                    {
                        "Yes": partial(self.download_assets, force_download=True),
                        "No": lambda: None,
                    },
                )
                return

            logger.info(f"Downloading assets ({len(assets_for_download)})")
            for i, asset in enumerate(assets_for_download):

                asset_download_sas_address = configHandle.get_download_asset_address()
                asset_download_sas_address = f"{asset_download_sas_address}/{asset}"
                try:
                    r = self.session.get(asset_download_sas_address)
                    r.raise_for_status()
                    response = r.json()
                    sas_link = response["url"]
                    destination_name = os.path.join(
                        configHandle.getLocal(),
                        "mats/mgb",
                        asset + f"_{config.model_versions.get(asset)}",
                    )
                    # destination_name -> full_path/asset_{version}
                    self.download_blob_file_with_progress(
                        sas_link,
                        response.get("container_name"),
                        asset,
                        destination_name,
                        with_dialog=True,
                        content_length=response.get("content-length"),
                        extra_text=f"{i+1} / {len(assets_for_download)}",
                    )
                except Exception as e:
                    config.global_signals.notificationSignal.emit(
                        f"Failed to download asset : {asset} "
                    )
                    logger.error(f"Error getting SAS link for {asset} {e}")
                    continue
            self.MainWindow.sdknn_tool.startSessWithModel()
        except Exception as e:
            logger.error(f"Error downloading assets {e}")
            config.global_signals.complete_progress_bar_signal.emit()
            raise e
        config.global_signals.complete_progress_bar_signal.emit()

    def download_test_fixtures(self):
        # Download image fixtures for tests. For each file
        # request a SAS link and download the file
        self.downloading_test_fixtures = True
        parent_path = os.path.join(configHandle.getLocal(), "fixtures")
        if not os.path.exists(parent_path):
            os.makedirs(parent_path)
        assets_for_download = {
            "42784052-0cf6-40a8-9613-dacf5f93948f.tiff": parent_path,
            "daf-2_D2_aup-1i_26.tif": parent_path,
            "TMRE_D1_N2_C.tif": parent_path,
        }
        # iterate over assets retrieved from log in and check if any of them need updatating
        assets_to_ignore = []
        # check witch assets need to be downloaded
        for asset, path in assets_for_download.items():
            # Check if file is on disk
            if os.path.exists(os.path.join(path, asset)):
                assets_to_ignore.append(asset)
            else:
                # download the asset
                continue
        # remove assets that dont need downloading / updating
        for asset in assets_to_ignore:
            del assets_for_download[asset]
        if len(assets_for_download) == 0:
            logger.info("No assets to download")
            self.downloading_test_fixtures = False
            return
        logger.info(f"Downloading assets ({len(assets_for_download)})")
        config.global_signals.loading_dialog_show.emit()
        for i, asset in enumerate(assets_for_download):
            config.global_signals.loading_dialog_set_text.emit(
                f"Fetching assets {i+1}/{len(assets_for_download)}"
            )
            config.global_signals.loading_dialog_signal_update_progress_percent.emit(0)

            asset_download_sas_address = configHandle.get_download_asset_address()
            asset_download_sas_address = f"{asset_download_sas_address}/{asset}"
            try:
                r = self.session.get(asset_download_sas_address)
                r.raise_for_status()
                response = r.json()
                sas_link = response["url"]
                destination_name = os.path.join(
                    parent_path,
                    asset,
                )
                # destination_name -> full_path/asset
                self.download_blob_file_with_progress(
                    sas_link,
                    response.get("container_name"),
                    asset,
                    destination_name,
                    with_dialog=True,
                    content_length=response.get("content-length"),
                    extra_text=f"{i+1} / {len(assets_for_download)}",
                )
            except Exception as e:
                logger.error(f"Error getting SAS link for {asset} {e}")
                continue
        self.downloading_test_fixtures = False
        config.global_signals.loading_dialog_signal_close.emit()

    def download_blob_file_with_progress(
        self,
        sas_url,
        container_name,
        asset,
        destination_name,
        with_dialog=False,
        content_length=0,
        extra_text=None,
    ):
        # save it on a temporary directory and transfer after
        import os
        import shutil
        import tempfile
        import time

        from azure.storage.blob import BlobClient, BlobServiceClient

        blob_client = BlobClient.from_blob_url(blob_url=sas_url)

        # # Get a blob client using the container and blob name
        # blob_client = blob_service_client.get_blob_client(
        #     container=container_name, blob=asset
        # )

        with tempfile.TemporaryDirectory() as temp_dir:
            offset = 0
            content_length = int(content_length)
            remaining_bytes = content_length
            start_time = time.time()
            last_update_time = start_time
            bytes_since_last_update = 0

            if with_dialog:
                config.global_signals.start_progress_bar_signal.emit(
                    {
                        "title": "Downloading assets " + extra_text,
                        "message": f"Downloading {extra_text}",
                        "modal": True,
                        "percent": 0,
                    }
                )

            destination = os.path.join(temp_dir, f"{asset}")
            with open(destination, "wb") as download_file:
                while remaining_bytes > 0:
                    download_size = min(CHUNK_SIZE, remaining_bytes)
                    download_stream = blob_client.download_blob(
                        offset=offset, length=download_size
                    )
                    chunk_data = download_stream.readall()
                    download_file.write(chunk_data)

                    # Update progress tracking
                    offset += download_size
                    remaining_bytes -= download_size
                    bytes_since_last_update += download_size
                    current_time = time.time()

                    # Update speed and ETA calculations every 0.5 seconds
                    if current_time - last_update_time >= 0.5:
                        elapsed = current_time - start_time
                        speed = (
                            content_length - remaining_bytes
                        ) / elapsed  # bytes/sec
                        speed_mb = speed / (1024 * 1024)  # Convert to MB/s

                        if speed > 0:
                            eta_seconds = remaining_bytes / speed
                            eta_str = f"{int(eta_seconds/60)}m {int(eta_seconds%60)}s"
                        else:
                            eta_str = "calculating..."

                        progress = (
                            (content_length - remaining_bytes) / content_length
                        ) * 100

                        if with_dialog:
                            if not config.user_cfg["USER_WORKERS"]:
                                QtWidgets.QApplication.processEvents()
                            config.global_signals.update_progress_bar_progress_signal.emit(
                                {
                                    "title": "Downloading assets " + extra_text,
                                    "percent": round(progress, 2),
                                    "message": f"Speed: {speed_mb:.1f} MB/s | ETA: {eta_str}",
                                }
                            )
                            QtWidgets.QApplication.processEvents()
                        else:
                            print(
                                f"Download progress: {extra_text} - {speed_mb:.1f} MB/s | ETA: {eta_str}"
                            )

                        last_update_time = current_time
                        bytes_since_last_update = 0

            shutil.move(destination, destination_name)  # from temp dir to destination

    def download_image_file_with_progress(
        self, url, image_uuid, with_dialog=False, return_response=False
    ):
        # save it on a temporary directory and transfer after
        import os
        import shutil
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            response = self.session.get(url, stream=True)
            total_length = response.headers.get("content-length")
            content_disposition = response.headers.get("content-disposition")
            if with_dialog:
                config.global_signals.loading_dialog_show.emit()
            if content_disposition:
                # Extract filename from Content-Disposition header if available.
                if len(content_disposition.split("extension=")) == 2:
                    extension = (
                        content_disposition.split("extension=")[1]
                        .strip('"')
                        .replace(".", "")
                    )
                elif len(content_disposition.split("filename=")) == 2:
                    extension = (
                        content_disposition.split("filename=")[1]
                        .strip('"')
                        .split(".")[-1]
                    )
                else:
                    extension = "jpg"
            else:
                extension = "jpg"  # default is jpg

            if total_length is None:  # no content length header
                print("Couldn't get the content-length header")
            else:
                total_length = int(total_length)
                downloaded = 0

                destination = os.path.join(temp_dir, f"{image_uuid}.{extension}")
                with open(destination, "wb") as file:
                    for data in response.iter_content(chunk_size=CHUNK_SIZE):
                        downloaded += len(data)
                        file.write(data)
                        done_percentage = 100 * downloaded / total_length
                        if with_dialog:
                            config.global_signals.loading_dialog_set_text.emit(
                                f"Downloading {done_percentage:.2f}%"
                            )
                            config.global_signals.loading_dialog_signal_update_progress_percent.emit(
                                int(done_percentage)
                            )
                        else:
                            print(f"Download progress: {done_percentage:.2f}%")
            # make sure the filename is unique on the cache dir
            filename = os.path.basename(destination)
            file_path = config.get_cache_unique_file_path(filename)
            shutil.move(destination, file_path)  # from temp dir to cache dir
            if with_dialog:
                config.global_signals.loading_dialog_signal_close.emit()
        if return_response:
            return file_path, response
        return file_path

    @config.threaded
    def download_category_images(self):
        # provided a list of category uuids, download the images required
        # for the categories
        import base64
        import glob

        import cv2
        import numpy as np

        from celer_sight_ai import config

        category_icons_path = os.path.join(
            configHandle.getLocal(), "experiment_configs/category_image_cache"
        )
        if not os.path.exists(category_icons_path):
            os.makedirs(category_icons_path)

        logger.info("Downloading category images")
        from celer_sight_ai.configHandle import get_download_category_map_images_address

        all_downloaded_icons = []
        # list all uuid.jpg in the category_image_cache
        for file in glob.glob(os.path.join(category_icons_path, "*.jpg")):
            all_downloaded_icons.append(os.path.basename(file).split(".")[0])

        category_uuids_to_request_images = []
        if not config.cloud_categories:
            return
        for organism in config.cloud_categories:
            class_uuid = None
            available_classes = organism.get("classes")
            if available_classes:
                if len(available_classes) == 0:
                    continue
                class_uuid = available_classes[0].get("uuid")
            else:
                continue

            if class_uuid not in all_downloaded_icons:
                category_uuids_to_request_images.append(class_uuid)

        if len(category_uuids_to_request_images) == 0:
            return

        url = get_download_category_map_images_address()
        data = {"uuids": category_uuids_to_request_images}
        r = self.session.get(url, json=data)
        r.raise_for_status()
        # for every image returned, write it to disk with uuid.jpg
        for uuid, image in r.json().items():
            if isinstance(image, type(None)):
                continue
            try:
                image = cv2.imdecode(
                    np.frombuffer(base64.b64decode(image), np.uint8),
                    cv2.IMREAD_COLOR,
                )
                cv2.imwrite(
                    os.path.join(
                        configHandle.getLocal(),
                        f"experiment_configs/category_image_cache/{uuid}.jpg",
                    ),
                    image,
                )
            except Exception as e:
                logger.error(f"Error downloading image {uuid} {e}")
                continue
        logger.info("Category images downloaded")
        config.global_signals.update_category_icons_signal.emit()

    @login_required
    def create_new_category_cloud(self, data):
        """
        Add new category to the server
        "category": str
        "supercategory": str
        "type": str, # private or public
        # parent category gets converted to uuid on the server
        "parent_category" : str,
        "username": str,
        "text": str,

        """
        from celer_sight_ai import config

        logger.debug("Creating category for active training.")

        url = configHandle.get_create_new_category_address()

        resp = self.session.post(url, json=data)
        if resp.status_code == 404 or resp.status_code == 403:
            # get responce data
            data = resp.json()
            config.global_signals.errorSignal.emit(f"Error : {data['message']}")
            logger.warning(f"Error : {data['message']}")
            return data["message"]
        resp.raise_for_status()
        logger.info("Category created successfully")
        config.global_signals.successSignal.emit("Category created successfully")
        return

    def update_category_image(self, category_uuid, image_array):
        """
        Update the cloud category displayed (thumbnail) image
        Convert the image data to base64 encoded image data jpg
        """
        import base64
        import io

        from celer_sight_ai import config

        url = configHandle.get_update_category_image_address()

        _, buffer = cv2.imencode(".jpg", image_array)
        image_bytes = io.BytesIO()
        # Convert buffer to a byte string
        image_bytes = buffer.tobytes()

        # Encode bytes to base64 string
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")

        req = self.session.post(
            url, json={"category_uuid": category_uuid, "image_data": image_b64}
        )
        req.raise_for_status()

    def remove_category_cloud(self, data):
        """
        Remove category from the server

        Args:
            data: {
                supercategory: str ,
                category: str ,
                username : str,
        }
        """
        from celer_sight_ai import config

        logger.info(f"Deleting the cloud category {data}")
        url = configHandle.get_remove_category_address()

        resp = self.session.post(url, json=data)
        if resp.status_code == 404 or resp.status_code == 403:
            # get responce data
            data = resp.json()
            config.global_signals.errorSignal.emit(f"Error : {data['message']}")
            logger.warning(f"Error : {data['message']}")
            return data["message"]
        resp.raise_for_status()
        logger.info("Removed category successfully")
        config.global_signals.successSignal.emit("Category removed successfully")
        return

    @login_required
    def get_cloud_classes(self):
        """
        Get the address of the cloud classes
        """
        from celer_sight_ai.configHandle import get_cloud_classes_address

        r = self.session.get(get_cloud_classes_address(), timeout=60)
        r.raise_for_status()
        return r.json()

    @login_required
    @config.threaded
    def delete_remote_images(self, image_uuids: list[str]):
        try:
            url = configHandle.get_delete_remote_image_address()
            for image_uuid in image_uuids:
                r = self.session.delete(url, json={"image_uuid": image_uuid})
                r.raise_for_status()
            return r.json()
        except Exception as e:
            logger.error(f"Error deleting remote image: {e}")
            config.global_signals.notificationSignal.emit(
                f"Failed to delete remote image: {e}"
            )
            return False

    @login_required
    def insert_remote_annotation(self, data: dict = {}):
        logger.info("Sending annotation to remote")
        url = configHandle.get_insert_remote_annotation()
        # send request through data
        r = self.session.post(url, json=data)
        r.raise_for_status()
        logger.info(f"Insert remote annotation response {r}")
        return r.json()["annotation_uuid"]

    @login_required
    def get_remote_annotations_for_image(self, data: dict = {}):
        logger.info("Getting remote annotations for image")
        url = configHandle.get_remote_annotations_for_image_address()
        # send request through data
        r = self.session.get(url, json=data)
        r.raise_for_status()
        logger.info(f"Get remote annotations response {r}")
        return r.json()  # list of annotations

    @config.threaded
    @login_required
    def update_remote_annotation(self, data: dict = {}) -> tuple[bool, Optional[str]]:
        """
        Updates an existing annotation on the remote server.

        Args:
            data: Dictionary containing annotation data with the following fields:
                - annotation_uuid (str): Unique identifier for the annotation
                - image_uuid (str): Unique identifier for the image
                - category (str): Category name
                - supercategory (str): Supercategory name
                - data (list): Annotation coordinates/data
                - audited (bool): Whether annotation has been audited

        Returns:
            Tuple[bool, Optional[str]]: Success status and error message if any
        """
        logger.info(f"Updating remote annotation {data.get('annotation_uuid')}")

        # Validate required fields
        required_fields = [
            "annotation_uuid",
            "image_uuid",
            "category",
            "supercategory",
            "data",
        ]
        missing_fields = [f for f in required_fields if f not in data]
        if missing_fields:
            error_msg = f"Missing required fields: {', '.join(missing_fields)}"
            logger.error(error_msg)
            return False, error_msg

        try:
            url = configHandle.get_update_remote_annotation_address()
            r = self.session.post(url, json=data, timeout=30)  # Add timeout
            r.raise_for_status()

            logger.info(
                f"Successfully updated annotation {data.get('annotation_uuid')}"
            )
            return True, None

        except requests.Timeout:
            error_msg = "Request timed out while updating annotation"
            logger.error(error_msg)
            return False, error_msg

        except requests.HTTPError as e:
            error_msg = f"HTTP error occurred: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

        except Exception as e:
            error_msg = f"Unexpected error updating annotation: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    @login_required
    def delete_remote_annotation(self, data: dict = {}):
        """
        Data should look like this:
            "supercategory": str,
            "image_uuid": str,
            "annotation_uuid": uuid str of existing annotation,
        """
        logger.info("Deleting remote annotation")
        url = configHandle.get_delete_remote_annotation_address()
        r = self.session.post(url, json=data)
        r.raise_for_status()
        logger.info(f"Delete remote annotation response {r}")
        return

    @login_required
    def get_remote_image_high(self, image_uuid):
        api_addr = f"{configHandle.get_remote_image_high_address()}/{image_uuid}"
        destination_path, r = self.download_image_file_with_progress(
            api_addr, image_uuid, return_response=True
        )
        width = r.headers.get("X-Image-Width")
        height = r.headers.get("X-Image-Height")
        image_shape = {"SizeX": width, "SizeY": height}
        return destination_path, image_shape

    @login_required
    def get_remote_image(self, image_url=None, quality="low"):
        import numpy as np

        if not image_url:
            return
        # quality = "low"
        # remove celer_sight_ai:// form the address
        image_url = image_url.replace("celer_sight_ai:", "")
        # get image from server
        if quality.lower() == "high":
            api_addr = f"{configHandle.get_remote_image_high_address()}/{image_url}"
        elif quality.lower() == "low":
            api_addr = f"{configHandle.get_remote_image_low_address()}/{image_url}"
        else:
            raise ValueError("Quality can only be high or low")
        # get the image, retry 3 times
        for i in range(3):
            try:
                r = self.session.get(api_addr)
                r.raise_for_status()
                break
            except Exception as e:
                if i == 2:
                    raise e
                continue

        # convert to numpy array
        nparr = np.frombuffer(r.content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # get the original width and height of the image
        # Access headers
        headers = r.headers

        # Get the custom header
        image_width = headers.get("X-Image-Width")
        image_height = headers.get("X-Image-Height")
        if int(image_width) != img.shape[1] or int(image_height) != img.shape[0]:
            # resize image
            img = cv2.resize(img, (int(image_width), int(image_height)))
        data = {}
        data["image_data"] = img
        data["size_x"] = int(image_width)
        data["size_y"] = int(image_height)
        if headers.get("X-Is-UltraHighRes") == "True":
            data["is_ultra_high_res"] = True
        else:
            data["is_ultra_high_res"] = False
        return data

    @login_required
    def get_available_models(self, username=None):
        import requests

        from celer_sight_ai.configHandle import get_available_models_address

        if not username:
            username = config.user_attributes.username
        headers = {"Accept": "application/json", "Content-Type": "application/json"}

        api_addr = f"{get_available_models_address()}"

        json_data = {"email": username}

        r = self.session.get(api_addr, json=json_data, headers=headers, timeout=60)
        r.raise_for_status()
        resp = r.json()
        return resp

    @login_required
    def set_remote_annotation_session_as_audited(
        self, image_uuids: list = [], class_names: list = []
    ):
        from celer_sight_ai import configHandle

        # get the address
        addr = configHandle.get_set_remote_annotation_session_as_audited_address()

        data = {
            "image_uuids": image_uuids,
            "audited_categories": class_names,
            "supercategory": config.supercategory,
        }
        try:
            r = self.session.post(addr, json=data)
            r.raise_for_status()
        except Exception:
            return False, str(r.text)
        return True, ""

    @login_required
    def remote_image_batch_for_annotation(self):
        """
        This method gets a list of image id on celer sight server for annotation
        """

        data = {
            "user_id": config.user_attributes.username,
            "supercategory": config.user_cfg["REMOTE_ANNOTATION_SUPERCATEGORY"],
            "categories": config.user_cfg["REMOTE_ANNOTATATION_CATEGORIES"],
            "amount": config.user_cfg["ANNOTATED_DATA_AMOUNT"],
            "categories_to_exclude": config.user_cfg[
                "REMOTE_ANNOTATION_CATEGORIES_TO_EXCLUDE"
            ],
            "contribute_mode_retrieval": config.user_cfg[
                "REMOTE_ANNOTATION_CONTRIBUTE_MODE"
            ],
            "partial_annotation_id": config.user_cfg["REMOTE_ANNOTATIONS_PARTIAL_ID"],
            "fetch_images_without_annotations": config.user_cfg[
                "REMOTE_ANNOTATIONS_WITHOUT_ANNOTATIONS"
            ],
            "audited": config.user_cfg["REMOTE_ANNOTATIONS_AUDITED"],
            "randomized": config.user_cfg["REMOTE_ANNOTATIONS_RANDOMIZED"],
            "order": config.user_cfg["REMOTE_ANNOTATIONS_ORDER"],
            "private": False,
        }

        # if we are testing we only retrieve mock images
        if os.environ.get("CELER_SIGHT_TESTING"):
            data["mock"] = True  # only admins can see mock images
        config.supercategory = config.user_cfg["REMOTE_ANNOTATION_SUPERCATEGORY"]
        result = self.remote_image_batch_for_annotation_method(data)

        return result.json().get("image_ids", [])

    def remote_image_batch_for_annotation_method(self, data):
        from celer_sight_ai.configHandle import get_remote_image_batch_for_annotation

        api_addr = f"{get_remote_image_batch_for_annotation()}"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        r = self.session.get(api_addr, data=json.dumps(data), headers=headers)
        r.raise_for_status()
        return r

    @config.threaded
    def send_image_for_inference_partial(
        self,
        image_object,
        supercategory,
        tile_group,
        tile_group_metadata,
        tile,
        event=None,
        max_retries=3,
    ):
        """
        This method handles inference threaded every tile in send_image_for_infernece
        """
        from celer_sight_ai.configHandle import get_send_image_inference_address

        warning_message = ""
        unavailable_categories = []

        process_dimention = tile_group_metadata["image_size"]

        if not image_object._is_ultra_high_res:
            # convert x,y,w,h to x,y,x2,y2
            # tile_1 = [tile[0], tile[1], tile[2] - tile[0], tile[3] - tile[1]]
            image_to_send = image_object.getImage(to_uint8=True, bbox=tile)
            slider_val = self.MainWindow.pg1_settings_contras_slider.value()
            if slider_val != 0:
                image_to_send = self.MainWindow.handle_adjustment_to_image(
                    image_to_send, slider_val
                )
            if isinstance(image_to_send, type(None)):
                logger.warning(f"Skipping tile image {tile} on inference.")
                return
            config.dbg_image(image_to_send)
            print(f"tile {tile}")
            # resize image to 1024x1024 , the ideal dimention used for model prediction
            # store the resize factor to resizing back later
            image_to_send = cv2.resize(image_to_send, process_dimention)
        # # retrieve image as ultra high res, needs different handling
        else:
            # get the image
            image_to_send = image_object.getImage(
                to_uint8=True,
                bbox=tile,
                avoid_loading_ultra_high_res_arrays_normaly=True,
            )
            image_to_send = cv2.resize(image_to_send, process_dimention)
        _, img_encoded = cv2.imencode(
            ".jpg", image_to_send, [int(cv2.IMWRITE_JPEG_QUALITY), 100]
        )

        send_image_inference_url = get_send_image_inference_address()
        if config.stop_inference:
            return (None, "")
        for i in range(max_retries):
            try:
                resp = self.session.post(
                    send_image_inference_url,
                    data={
                        "json": json.dumps(
                            {
                                "inference_user_settings": (
                                    "settings.json",
                                    None,
                                    "application/json",
                                ),
                                "supercategory": supercategory,
                                "file_encoding": "jpg",
                                "class_names": list(tile_group),
                            }
                        )
                    },
                    files={
                        "data": ("image.png", img_encoded.tostring(), "image/png"),
                    },
                    timeout=60,
                )
                if resp.status_code != 200:
                    config.global_signals.errorSignal.emit(html2text(resp.text))
                    self.MainWindow.get_roi_ai_button.click()  # cancel inference
                    return
                resp.raise_for_status()
                response = resp.json()
                if "warning" in response:
                    warning_message = response.get("warning")
                if "unavailable_categories" in response:
                    unavailable_categories = response.get("unavailable_categories")

                request_id = response.get("request_id")
                logger.debug(
                    f"Sent image with request_id {request_id}, tile {tile} and image_uuid {image_object.unique_id}"
                )
                # add a polygon shape on the region that we are inferencing
                config.global_signals.add_inference_tile_graphics_item_signal.emit(
                    {
                        "tile_box": tile,
                        "inference_uuid": request_id,
                        "image_uuid": image_object.unique_id,
                    }
                )

                with config.lock:
                    self.MainWindow.MyInferenceHandler.inference_uuids[request_id] = {
                        "image_uuid": image_object.unique_id,
                        "send_image_dimention": image_to_send.shape[:2],
                        "source_tile": tile,
                        "send_time": time.time(),
                    }

                if config.stop_inference:
                    return (None, "")
                if event:
                    if event.is_set():
                        return (None, "")
                break
            except Exception as e:
                logger.warning("Failed sending image for inference, retrying.")
                if config.stop_inference:
                    return (None, "")
                if event:
                    if event.is_set():
                        return (None, "")
                if i == max_retries - 1:
                    logger.error(
                        "Too many retries, aborting sending image to inference."
                    )
                    config.inference_buffer -= 1
                    config.global_signals.remove_inference_tile_graphics_item_signal.emit(
                        {"inference_uuid": request_id}
                    )
                    raise e
                continue
            finally:
                self.images_being_sent -= 1
                if warning_message:
                    config.global_signals.notificationSignal.emit(warning_message)
                # convert unavailable categories to names
                unavailable_categories = [
                    self.MainWindow.custom_class_list_widget.classes[i].text()
                    for i in unavailable_categories
                ]
                if len(unavailable_categories):
                    config.global_signals.notificationSignal.emit(
                        f"Unavailable classes: {', '.join(unavailable_categories)}"
                    )

    @login_required
    def send_initialize_inference(self, supercategory, requests):
        from celer_sight_ai.configHandle import get_initialize_inference_address

        addr = get_initialize_inference_address()
        data = {"supercategory": supercategory, "amount_of_requests": requests}
        r = self.session.post(addr, json=data)
        resp = r.json()
        if "error" in resp:
            raise Exception(resp["error"])
        r.raise_for_status()
        return r.json()

    @login_required
    def send_image_for_inference(
        self,
        image_object,
        supercategory=None,
        tile_groups={},  # if tile groups are provided, send multiple sub-images (tiles) for inference, each for a different class group
        inference_user_settings=None,
        event=None,  # for threading --> to exit thread safely.
    ):
        """
        Sends an image for inference in the cloud

        Parameters
        ----------
        image_object : object of the image to send for inference
            Image object to send for inference, required.
        group_name : str
            Group name of the image, only required when the UI is on
        condition_name : str
            Actually its the condition uuid, TODO: change in the future
        supercategory : str
            Supercategory of the image, only required when the UI is on, optional
        tile_groups: dict
            dict where the keys are groups of classes and values are the size of the tile to be sent for inference
        inference_user_settings : dict
            User settings for inference, post process settings, not required
        event : threading.Event, optional
        """
        from celer_sight_ai.io.image_reader import (
            crop_and_pad_image,
            generate_complete_spiral_tiles,
        )

        max_retries = 3
        retry_delay = 5  # in seconds
        logger.debug("Before inference")
        image_uuid = image_object.unique_id
        # if its not ultra high res, read the image directly
        image_array = None

        import requests

        from celer_sight_ai import config

        # if inference_user_settings is none, load the default
        if inference_user_settings is None:
            import yaml

            # read yml file from disk to send model settings for inference
            with open("model_configs/default_model.yml") as f:
                inference_user_settings = yaml.load(f, Loader=yaml.FullLoader)
        if not supercategory:
            supercategory = config.supercategory
        config.global_signals.startInferenceAnimationSignal.emit(image_object.unique_id)

        all_possible_tiles = image_object.get_all_possible_tiles(
            tile_groups, skip_lower_than_overlap=True
        )

        for tile_group in all_possible_tiles:
            for tile in all_possible_tiles[tile_group]:
                # start inference retrival if needed, this will triger on the second tile
                # if its just one tile, then it will trigger on the parent function of InferenceHandler
                if config.inference_buffer > 0 and not config.STARTED_RETRIEVAL:
                    if config.user_cfg["USER_WORKERS"]:
                        self.MainWindow.MyInferenceHandler.start_inference_retrival()
                    config.STARTED_RETRIEVAL = True
                if config.stop_inference:
                    return (None, "")
                # if the current number of images being send is more than 5, wait for one to finish
                while (
                    self.images_being_sent > 2
                    or config.inference_buffer
                    > config.user_cfg["MAX_CONCURENT_INFERENCE_REQUESTS"]
                ):
                    if config.stop_inference:
                        return (None, "")
                    if event:
                        if event.is_set():
                            return (None, "")
                    time.sleep(0.1)
                self.images_being_sent += 1  # keep a count of concurrent images being sent, better to use up to 5 per time
                config.inference_buffer += 1
                tile_group_metadata = tile_groups[tile_group]
                self.send_image_for_inference_partial(
                    image_object,
                    supercategory,
                    tile_group,
                    tile_group_metadata,
                    tile,
                    event,
                    max_retries,
                )

        if not config.user_cfg["USER_WORKERS"]:
            # check for results now
            # in a for loop search
            # when result find image and paste
            time.sleep(3)
            self.MainWindow.MyInferenceHandler.start_inference_retrival(
                ignore_running_inference=True
            )

    def retrieve_inference_data(self, inference_uuids):
        """
        Get the status of the inference job
        """
        url = configHandle.retrieve_inference_data_address()
        data = {"inference_request_ids": inference_uuids}
        r = self.session.get(url, json=data)
        r.raise_for_status()
        return r.json()

    # dont run threaded, parent function needs to be threaded
    @login_required
    def send_large_zipped_image_annotated(
        self,
        image_object,
        with_dialog=False,
        quality="low",
        start_percentage=0,
        end_percentage=100,
        state="corrected",  # partially_annotated , fully_annotated => during analysis, contribute partial , contributed complete
    ):
        # gather all masks and compute COCO annotation in a dictionary
        import base64
        import io
        import tempfile
        import zlib
        from pathlib import Path

        import numpy as np
        import zstandard
        from PIL import Image
        from requests import Request
        from requests_toolbelt.multipart.encoder import MultipartEncoder

        from celer_sight_ai.configHandle import (
            get_send_large_zipped_image_annotated_address,
        )
        from celer_sight_ai.io.image_reader import (
            create_large_compressed_image_from_ultra_high_res_tiled_image,
        )

        with tempfile.TemporaryDirectory() as tempdir:
            dict_to_send = {}
            image_path = image_object.get_path()

            if image_object._is_ultra_high_res:
                if with_dialog:
                    config.global_signals.loading_dialog_set_text.emit(
                        f"Preparing : {os.path.basename(image_path)} "
                    )
                file_to_transfer = (
                    create_large_compressed_image_from_ultra_high_res_tiled_image(
                        image_path, temp_dir=tempdir, compress=False
                    )
                )

            else:
                # convert image to 8bit, 3 channel, jpeg
                if with_dialog:
                    config.global_signals.loading_dialog_set_text.emit(
                        f"Preparing : {os.path.basename(image_path)} "
                    )
                image_data = image_object.getImage(to_uint8=True, to_rgb=True)
                # write to disk as a jpg
                image_path_base = os.path.basename(image_path).split(".")[0] + ".jpg"
                file_to_transfer = tempdir + "/" + image_path_base
                cv2.imwrite(file_to_transfer, image_data)

            cctx = zstandard.ZstdCompressor(level=3, threads=-1)
            file_to_transfer_prior = file_to_transfer
            # remove extension and replace it with .zst
            file_path = Path(file_to_transfer_prior)
            extension = file_path.suffix
            file_to_transfer = file_to_transfer.replace(extension, ".zst")
            # get only the filename
            file_to_transfer_filename = os.path.basename(file_to_transfer)
            file_to_transfer = tempdir + "/" + file_to_transfer_filename
            with open(file_to_transfer_prior, "rb") as ifh, open(
                file_to_transfer, "wb"
            ) as ofh:
                cctx.copy_stream(
                    ifh, ofh, read_size=1024 * 1024, write_size=1024 * 1024
                )

            image_dict = {}
            user_dict = {}
            # image_dict["image_data"] = compressed_jpeg_bytes
            image_dict["width"] = image_object.SizeX
            image_dict["height"] = image_object.SizeY
            image_dict["image_uuid"] = str(image_object.unique_id)
            image_dict["supercategory"] = config.supercategory
            image_dict["physical_pixel_size_x"] = image_object.PhysicalSizeX
            image_dict["physical_pixel_size_y"] = image_object.PhysicalSizeY
            image_dict["physical_pixel_size_x_unit"] = image_object.PhysicalSizeXUnit
            image_dict["physical_pixel_size_y_unit"] = image_object.PhysicalSizeYUnit
            # if the state is fully_annotated, mark all categories as audited
            if state == "fully_annotated":
                image_dict["audited_categories"] = list(
                    self.MainWindow.custom_class_list_widget.classes.keys()
                )
            else:
                image_dict["audited_categories"] = []

            dict_to_send["image"] = image_dict

            user_dict["lab_id"] = config.user_attributes.lab_uuid
            user_dict["state"] = state
            dict_to_send["user"] = user_dict
            if os.environ.get("CELER_SIGHT_TESTING", False):
                # if we are testing, the object has to be mock
                # which makes temporary
                dict_to_send["mock"] = True
            else:
                dict_to_send["mock"] = False
            dict_to_send["ext_compressed"] = os.path.splitext(
                file_to_transfer_filename
            )[
                1
            ]  # extension
            dict_to_send["ext"] = os.path.splitext(file_to_transfer_prior)[
                1
            ]  # extension

            send_large_zipped_image_annotated_url = (
                get_send_large_zipped_image_annotated_address()
            )

            # Custom callback for monitoring progress
            def callback(bytes_read, total_size):
                if with_dialog:
                    progress_percentage = (bytes_read / total_size) * 100
                    percentage = (
                        progress_percentage * (end_percentage - start_percentage) / 100
                    ) + start_percentage
                    config.global_signals.loading_dialog_signal_update_progress_percent.emit(
                        int(percentage)
                    )

            def file_generator(file_path):
                total_size = os.path.getsize(file_path)
                uploaded = 0
                with open(file_path, "rb") as file:
                    while True:
                        data = file.read(4096)  # Read in chunks of 4KB
                        if not data:
                            break
                        uploaded += len(data)
                        if callback:
                            callback(uploaded, total_size)  # Update progress
                        yield data

            if with_dialog:
                config.global_signals.loading_dialog_set_text.emit(
                    f"Sending data : {os.path.basename(file_to_transfer)} "
                )
            # print_size:
            annotations = []
            for mask in image_object.masks:
                annotation_dict = {
                    "data": [
                        self.MainWindow.numpy_to_python(np.array(i).astype(np.uint32))
                        for i in mask.get_array_for_storing()
                    ],
                    "supercategory": config.supercategory,
                    "category": self.MainWindow.custom_class_list_widget.classes[
                        mask.class_id
                    ].text(),
                    "image_width": image_object.SizeX,
                    "image_height": image_object.SizeY,
                    "type": mask.mask_type,
                    "image_uuid": str(image_object.unique_id),
                    "annotation_uuid": str(mask.unique_id),
                }
                annotations.append(annotation_dict)
            # compress really large annotations
            # compressor = zstandard.ZstdCompressor()
            # compressor.compress(json.dumps(annotations).encode('utf-8'))
            dict_to_send["annotations"] = annotations
            # if annotations are empty, skip image
            if len(annotations) == 0:
                config.global_signals.notificationSignal.emit(
                    "No annotations found, skipping image"
                )
                return True, ""
            print(f"Size of file to transfer {os.path.getsize(file_to_transfer)}")
            resp = self.session.post(
                send_large_zipped_image_annotated_url,
                data=file_generator(file_to_transfer),
                headers={
                    "User-Agent": "python-requests/2.31.0",
                    "Connection": "keep-alive",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Content-Type": "application/octet-stream",
                    "Metadata": json.dumps(dict_to_send),
                },
            )
            if resp.status_code == 200:
                return True, ""
            elif resp.status_code == 400:
                return False, resp.text
        return False, "Error in sending image annotated"

    @login_required
    def get_user_info(self):
        from celer_sight_ai.configHandle import get_user_info_address

        user_info_address = get_user_info_address()
        response = config.client.session.get(user_info_address)
        response.raise_for_status()
        user_info = response.json()
        self.MainWindow.Licence_label_value.setText(user_info["licence"])

    @login_required
    def get_optimal_annotation_range(self, category):
        """
        Retrieves the optimal annotation range from the server.

        Returns:
            dict: The optimal annotation range data.

        Raises:
            requests.exceptions.RequestException: If there's an error with the request.
        """
        from celer_sight_ai.configHandle import get_optimal_annotation_range_address

        api_addr = get_optimal_annotation_range_address()
        try:
            response = self.session.get(api_addr, json={"category": category})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving optimal annotation range: {e}")
            raise

    @login_required
    @config.threaded
    def send_image_annotated(self, image_object, image_arr, quality="low"):
        """Sends the images that
        are modified after the inference is completed and user
        has started quantifying the images
        """
        # gather all masks and compute COCO annotation in a dictionary
        import base64
        import io
        import zlib

        import numpy as np
        from PIL import Image

        from celer_sight_ai.configHandle import get_send_image_annotated_address

        # for the during annotation correction, images will be converted to 8bit
        # for speed purposes

        # increase contrast
        if quality == "high":
            success, image_arr_bytes = cv2.imencode(".png", image_arr)
        else:
            # to jpeg
            quality = 95
            image_arr = cv2.convertScaleAbs(image_arr, alpha=2.5, beta=10)
            success, image_arr_bytes = cv2.imencode(
                ".jpg", image_arr, [int(cv2.IMWRITE_JPEG_QUALITY), quality]
            )

        compressed_data = zlib.compress(image_arr_bytes.tobytes())

        dict_to_send = {}

        image_dict = {}
        # image_dict["image_data"] = compressed_jpeg_bytes
        image_dict["width"] = image_arr.shape[1]
        image_dict["height"] = image_arr.shape[0]
        image_dict["image_uuid"] = str(image_object.unique_id)
        image_dict["supercategory"] = config.supercategory
        dict_to_send["image"] = image_dict

        annotations = []
        for mask in image_object.masks:
            annotation_dict = {
                "lab_id": config.user_attributes.lab_uuid,
                "data": self.MainWindow.numpy_to_python(mask.get_array_for_storing()),
                "supercategory": config.supercategory,
                "category": self.MainWindow.custom_class_list_widget.classes[
                    mask.class_id
                ].text(),
                "image_width": image_arr.shape[1],
                "image_height": image_arr.shape[0],
                "type": mask.mask_type,
                "image_uuid": str(image_object.unique_id),
                "annotation_uuid": str(mask.unique_id),
            }
            annotations.append(annotation_dict)
        dict_to_send["annotations"] = annotations
        # post a request with image_arr and annotations in data

        send_image_annotated_url = (
            get_send_image_annotated_address() + f"/{config.user_attributes.username}"
        )
        # prepare headers for http request
        files = {"image": ("array.png.gz", compressed_data, "application/octet-stream")}
        resp = self.session.post(
            send_image_annotated_url,
            data={"metadata": json.dumps(dict_to_send)},
            files=files,
        )
        print(f"Request completed, result status is {resp}")
        if resp.status_code == 200:
            return True
        else:
            logger.info(
                f"Error in sending image annotated for image id {image_object.image_id}"
            )

    def crashLogsToServer(self):
        try:
            import requests

            from celer_sight_ai.configHandle import get_send_crash_logs_address

            myLogFiletxt = os.path.join(getLocal(), "celer_sight.log")
            myLOGfile = open(myLogFiletxt)
            stringLog = myLOGfile.read()

            if not config.user_attributes.username:
                config.user_attributes.username = "notLogedUser"
            # send with post a stringLog as data to the endpoint with requests
            self.session.post(
                get_send_crash_logs_address(),
                data={"username": config.user_attributes.username, "log": stringLog},
            )
        except Exception as e:
            print(e)
            pass

    def contribToNets(self, net, contrib):
        logger.info("Skipping contribution")
        return
        try:
            import requests

            # send with post a stringLog as data to the endpoint with requests
            requests.post(
                self.mainAddr + "/api/v1/contrib_to_nets/",
                data={
                    "username": config.user_attributes.username,
                    "net": net,
                    "contrib": contrib,
                },
            )
        except Exception as e:
            print(e)
            pass

    def check_for_duplicates(
        self, image_hashes: list = [], hash_algorithm: str = "sha256_256"
    ):
        """
        Check for duplicates in the server and return the non duplicate items.
        """
        from celer_sight_ai.configHandle import get_check_for_duplicates_address

        check_for_duplicates_address = get_check_for_duplicates_address()
        resp = self.session.get(
            check_for_duplicates_address,
            json={
                "image_hashes": image_hashes,
                "lab_id": config.user_attributes.lab_uuid,
                "hash_method": hash_algorithm,
            },
        )
        return resp.json().get("duplicate_hashes", [])
