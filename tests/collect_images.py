import os
import sys
from glob import glob
from os import path as osp
from typing import Union


# collect all folders in the fixtures directory
fix_url = "fixtures"

def get_channel_patterns_image_urls() -> list[str]:
    """
    The function `get_image_urls_channel_patterns()` returns a list of all image URLs in the
    "channel_pattern" directory.

    Returns:
      a list of all the image URLs found in the "channel_pattern" directory under the "image_urls"
    subdirectory.
    """
    all_urls = glob(osp.join(fix_url, "channel_pattern", "image_urls", "*"))
    return all_urls


def get_channel_patterns_single_dir_url() -> str:
    """
    The function `get_image_urls_channel_patterns()` returns a list of all image URLs in the
    "channel_pattern" directory.

    Returns:
      a list of all the image URLs found in the "channel_pattern" directory under the "image_urls"
    subdirectory.
    """
    single_dir = glob(osp.join(fix_url, "channel_pattern", "single_dir_url", "*"))[0]
    return single_dir


def get_channel_multi_dir_urls() -> list:
    "Return a list of dirs out of which each dir contains a channel pattern"
    dir_urls = glob(osp.join(fix_url, "channel_pattern", "multi_dir_urls", "*"))
    return dir_urls


def get_fixture_red_images() -> list:
    "Return a list of red images"
    red_images = glob(osp.join(fix_url, "fixture_adding_removing_images_test", "*"))
    return red_images
