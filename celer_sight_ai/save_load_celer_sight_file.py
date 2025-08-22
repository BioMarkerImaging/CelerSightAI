from PyQt6 import QtWidgets
import os
import json
import struct
import zstandard as zstd
import numpy as np
from PIL import Image
import logging
from celer_sight_ai import config

logger = logging.getLogger(__name__)

def save_celer_sight_file_decider(mainwindow, filename=None):
    if config.CURRENT_SAVE_FILE:
        mainwindow.save_celer_sight_file(filename=config.CURRENT_SAVE_FILE)
    else:
        mainwindow.save_celer_sight_file()

def save_celer_sight_file(mainwindow, filename=None):
    """
    Runs to save the plaba file (save as)
    """
    import base64
    import json
    import struct

    import zstandard as zstd
    from PIL import Image

    from celer_sight_ai import config

    # open a file save dialog
    if not filename:
        # check on qsettings, if there is a previous location saved, use that

        last_save = ""
        if config.settings.value("last_save_location"):
            last_save = config.settings.value("last_save_location")
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            None, "Save File as", last_save, "BMI Celer Sight File (*.bmics)"
        )
        # save the location of the parent dir
        config.settings.setValue("last_save_location", os.path.dirname(filename))
    if not filename:
        return
    try:
        image_arrays = []
        image_paths = []
        # with dialog get save location
        # filename = ...
        data_dict = {}
        # Get all classes
        all_classes_widgets = [
            mainwindow.custom_class_list_widget.getItemWidget(i)
            for i in range(mainwindow.custom_class_list_widget.count())
        ]
        data_dict["classes"] = []
        # calculate overall progress
        tot_images = 0
        for gk in mainwindow.DH.BLobj.groups:
            go = mainwindow.DH.BLobj.groups[gk]
            for ck in go.conds:
                co = go.conds[ck]
                for io in co.images:
                    tot_images += 1
        config.global_signals.start_progress_bar_signal.emit(
            {
                "title": "Saving file...",
                "window_title": "Saving in Progress",
                "main_text": "",
            }
        )
        QtWidgets.QApplication.processEvents()
        iii = 0
        for cw in all_classes_widgets:
            cls_item = {}
            cls_item["name"] = cw.class_label.text()
            cls_item["unique_id"] = cw.unique_id
            cls_item["parent_class_uuid"] = cw.parent_class_uuid
            cls_item["is_particle"] = cw.is_particle
            cls_item["_is_class_visible"] = cw._is_class_visible
            cls_item["is_user_defined"] = cw.is_user_defined
            cls_item["color"] = cw.color
            data_dict["classes"].append(cls_item)

        # for every class widget, create an entry in classes
        # get all groups into metadata
        group_objects = []
        for gk in mainwindow.DH.BLobj.groups:
            group_item = {}
            go = mainwindow.DH.BLobj.groups[gk]
            group_item["groupName"] = gk
            group_item["unique_id"] = go.unique_id
            condition_objects = []
            for ck in go.conds:
                condition_object = {}
                co = go.conds[ck]
                condition_object["condition_name"] = ck
                condition_object["groupName"] = gk
                condition_object["condition_name_set"] = co.condition_name_set
                condition_object["unique_id"] = co.unique_id
                image_objects = []
                for io in co.images:  # id, not key.
                    out_image_object = {}
                    # full image path
                    complete_file_path = os.path.join(
                        str(io.fileRootFolder), io.fileName
                    )
                    image_paths.append(complete_file_path)
                    # if the image is remote, raise error and abort
                    if io.is_remote():
                        config.global_signals.errorSignal(
                            "Session contains remote images and can not be saved."
                        )
                    out_image_object["unique_id"] = io.unique_id
                    # get all relevant
                    # attributes for the image
                    out_image_object["AcquisitionDate"] = io.AcquisitionDate
                    out_image_object["DimensionOrder"] = io.DimensionOrder
                    out_image_object["ExperiementName"] = io.ExperiementName
                    out_image_object["ExposureTime"] = io.ExposureTime
                    out_image_object["ExposureTimeUnit"] = io.ExposureTimeUnit
                    out_image_object["ID"] = io.ID
                    out_image_object["_is_video"] = io._is_video
                    out_image_object["_is_ultra_high_res"] = io._is_ultra_high_res
                    out_image_object["PhotometricInterpretation"] = (
                        io.PhotometricInterpretation
                    )
                    out_image_object["PhysicalSizeX"] = io.PhysicalSizeX
                    out_image_object["PhysicalSizeXUnit"] = io.PhysicalSizeXUnit
                    out_image_object["PhysicalSizeY"] = io.PhysicalSizeY
                    out_image_object["PhysicalSizeYUnit"] = io.PhysicalSizeYUnit
                    out_image_object["SignificantBits"] = io.SignificantBits
                    out_image_object["SizeC"] = io.SizeC
                    out_image_object["SizeT"] = io.SizeT
                    out_image_object["SizeX"] = io.SizeX
                    out_image_object["SizeY"] = io.SizeY
                    out_image_object["SizeZ"] = io.SizeZ
                    out_image_object["Software"] = io.Software
                    out_image_object["bitDepth"] = io.bitDepth

                    out_image_object["channel_list"] = io.channel_list
                    out_image_object["computedInference"] = io.computedInference
                    out_image_object["treatment_uuid"] = io.treatment_uuid
                    out_image_object["fileName"] = str(io.fileName)
                    out_image_object["fileRootFolder"] = str(io.fileRootFolder)
                    out_image_object["group_uuid"] = io.group_uuid
                    out_image_object["hasBeenUploaded"] = io.hasBeenUploaded
                    out_image_object["imgID"] = io.imgID
                    out_image_object["is_stack"] = io.is_stack
                    # Get all current image objects
                    mask_objects = []
                    for mo in io.masks:
                        mask_object = {}
                        mask_object["class_id"] = mo.class_id
                        mask_object["class_group_id"] = mo.class_group_id
                        mask_object["spatial_id"] = mo.spatial_id
                        mask_object["score"] = mo.score
                        mask_object["image_uuid"] = mo.image_uuid
                        mask_object["includedInAnalysis"] = mo.includedInAnalysis
                        mask_object["mask_type"] = mo.mask_type
                        mask_object["is_suggested"] = mo.is_suggested
                        mask_object["_annotation_track_id"] = (
                            mo._annotation_track_id
                        )
                        mask_object["intensity_metrics"] = mo.intensity_metrics
                        if hasattr(mo, "particle_metrics"):
                            mask_object["particle_metrics"] = mo.particle_metrics
                        if hasattr(mo, "polygon_array"):
                            mask_object["polygon_array"] = []
                            arr = mo.get_array_for_storing()
                            arr = mainwindow.numpy_to_python(arr)
                            mask_object["polygon_array"].append(arr)
                        mask_object["unique_id"] = mo.unique_id
                        mask_object["visibility"] = mo.visibility
                        mask_objects.append(mask_object)
                    out_image_object["mask_objects"] = mask_objects
                    out_image_object["raw_image_extrema_set"] = (
                        io.raw_image_extrema_set
                    )
                    out_image_object["raw_image_max_value"] = io.raw_image_max_value
                    out_image_object["raw_image_min_value"] = io.raw_image_min_value
                    out_image_object["resolution"] = io.resolution
                    out_image_object["resolutionunit"] = io.resolutionunit
                    try:
                        out_image_object["thumbnail"] = io.thumbnail.hex()
                    except:
                        # in case an error is raised for the thumbnail, just set to none
                        # because it will get regenerated again when the file is loaded again
                        pass

                    out_image_object["_during_inference"] = io._during_inference
                    out_image_object["userModifiedAnnotation"] = (
                        io.userModifiedAnnotation
                    )
                    out_image_object["thumbnailGenerated"] = io.thumbnailGenerated
                    image_objects.append(out_image_object)
                    config.global_signals.update_progress_bar_progress_signal.emit(
                        {"percent": int((iii / tot_images) * 100)}
                    )
                    iii += 1

                    QtWidgets.QApplication.processEvents()
                condition_object["image_objects"] = image_objects
                condition_objects.append(condition_object)
            group_item["condition_objects"] = condition_objects
            group_objects.append(group_item)
        data_dict["grouped_data"] = group_objects
        config.global_signals.complete_progress_bar_signal.emit()
        from datetime import datetime

        data_dict = mainwindow.serialize_object(data_dict)
        now = datetime.now()
        metadata = {
            "version": "2",
            "user": config.user_attributes.username,
            "date": now.strftime("%B %d, %Y"),
        }
        with open(filename, "wb") as f:
            # Write Header Metadata
            metadata_json = json.dumps(metadata).encode("utf-8")
            f.write(struct.pack("I", len(metadata_json)))
            f.write(metadata_json)

            # record experiment settings
            analysis_type = None
            if (
                config.global_params.analysis
                == mainwindow.new_analysis_object.analysis_map["mean_intensity"]
            ):
                analysis_type = "intensity"
            elif (
                config.global_params.analysis
                == mainwindow.new_analysis_object.analysis_map["particles"]
            ):
                analysis_type = "particles"

            exp_settings = {
                "supercategory": config.supercategory,
                "analysis": analysis_type,
            }
            exp_settings = json.dumps(exp_settings).encode("utf-8")
            f.write(struct.pack("I", len(exp_settings)))
            f.write(exp_settings)

            # Write Dictionary Data
            dict_bytes = json.dumps(data_dict, default=mainwindow.handle_bytes).encode(
                "utf-8"
            )
            f.write(struct.pack("I", len(dict_bytes)))
            f.write(dict_bytes)

            # # Write Thumbnail
            # thumbnail_bytes = out_image_object["thumbnail"]
            # f.write(struct.pack("I", len(thumbnail_bytes)))
            # f.write(thumbnail_bytes)
            # Write Number of Images
            f.write(struct.pack("I", len(image_paths)))
            cctx = zstd.ZstdCompressor()
            # Write Metadata and Individual Images
            for img_path in image_paths:
                # Read and compress the image data
                with open(img_path, "rb") as img_file:
                    image_data = img_file.read()
                    compressed_data = cctx.compress(image_data)
                # get the size of the compressed data, if data is larger than 4GB use "Q" otherwise "I"
                compressed_data_size = len(compressed_data)
                if compressed_data_size > 4294967295:
                    # write stract type
                    mode = "Q"
                    struct.write(struct.pack("B", mode))
                    struct.write(struct.pack(mode, compressed_data_size))
                else:
                    mode = "I"
                    f.write(struct.pack("c", mode.encode("utf-8")))
                    f.write(struct.pack(mode, compressed_data_size))

                # Write the compressed image data
                f.write(compressed_data)

        config.CURRENT_SAVE_FILE = filename
        config.global_signals.successSignal.emit("Saved successfully.")
        QtWidgets.QApplication.processEvents()
        return group_objects, filename
    except Exception as e:
        logger.error(e)
        config.global_signals.fatalErrorSignal.emit("Failed to save file")
        config.global_signals.complete_progress_bar_signal.emit()
        # remove the file if it was created
        if os.path.exists(filename):
            os.remove(filename)

def get_array_from_storage(arr):
    from pycocotools import mask as coco_mask

    if isinstance(arr, dict):
        # Convert hex string to bytes and ensure correct RLE format
        rle = {
            "counts": bytes.fromhex(arr["counts"]),
            "size": tuple(arr["size"]),  # Convert to tuple for RLE format
        }
        return coco_mask.decode(rle)
    else:
        return arr

def store_locomotion_data(mainwindow, file_location=None):

    # get file save location from user if not supplied
    if not file_location:
        file_location, _ = QtWidgets.QFileDialog.getSaveFileName(
            None, "Save csv", "", "CSV Files (*.csv)"
        )
    if not file_location:
        return
    # get all data
    mainwindow.MyInferenceHandler.track_all_masks_by_treatment(file_location)
    return

def load_celer_sight_file(mainwindow, file_location=None):
    import base64
    import json
    import shutil
    import struct
    import uuid

    import zstandard as zstd
    from PIL import Image

    from celer_sight_ai import configHandle

    dctx = zstd.ZstdDecompressor()
    # open a file dialog
    if not file_location:
        # check on qsettings, if there is a previous location saved, use that

        last_save = ""
        if config.settings.value("last_save_location"):
            last_save = config.settings.value("last_save_location")
        file_location, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Select a Celer Sight file",
            last_save,
            "BMI Celer Sight File (*.bmics)",
        )
        # save the location of the parent dir
        config.settings.setValue(
            "last_save_location", os.path.dirname(file_location)
        )
    if not file_location:
        return
    if not os.path.exists(file_location):
        return
    prior_location = mainwindow.stackedWidget.currentWidget()
    if prior_location != mainwindow.MainInterface:
        # go to mainwindow
        mainwindow.create_new_enviroment_with_category()
        mainwindow.MainWindow.move_top_level_mainwindow_edge_widgets_to_position()
    try:
        # if we are at the supercategory selection page, move to main page
        mainwindow.stackedWidget.setCurrentWidget(mainwindow.MainInterface)
        # remove all classes
        mainwindow.custom_class_list_widget.delete_all_classes()

        # remove all
        mainwindow.DH.BLobj.delete_all_groups()

        from datetime import datetime

        now = datetime.now()
        # Format it into a string suitable for a folder name
        folder_name = now.strftime("%Y_%m_%d_%H_%M_%S")
        # get the local dir

        with open(file_location, "rb") as f:
            # Read metadata
            metadata_length = struct.unpack("I", f.read(4))[0]
            metadata = json.loads(f.read(metadata_length).decode("utf-8"))

            # if metadata["version"] == "2":, also read experiment settings
            if metadata["version"] == "2":
                exp_settings_length = struct.unpack("I", f.read(4))[0]
                exp_settings = json.loads(
                    f.read(exp_settings_length).decode("utf-8")
                )
                config.supercategory = exp_settings["supercategory"]
                if exp_settings["analysis"] == "intensity":
                    config.global_params.analysis = (
                        mainwindow.new_analysis_object.analysis_map["mean_intensity"]
                    )
                elif exp_settings["analysis"] == "particles":
                    config.global_params.analysis = (
                        mainwindow.new_analysis_object.analysis_map["particles"]
                    )

            # Read dictionary data
            dict_length = struct.unpack("I", f.read(4))[0]
            data_dict = json.loads(f.read(dict_length).decode("utf-8"))

            # # Skip thumbnail
            # thumbnail_length = struct.unpack("I", f.read(4))[0]
            # f.seek(thumbnail_length, 1)

            # # read thumbnails
            # thumbnails = f.read(thumbnail_length)

            # Read the number of images
            num_images = struct.unpack("I", f.read(4))[0]

            images = []

            # create classes
            for c in data_dict["classes"]:
                # add single class first
                mainwindow.custom_class_list_widget.addClass(
                    c["name"],
                    parent_class_uuid=c["parent_class_uuid"],
                    class_uuid=c["unique_id"],
                    is_user_defined=c["is_user_defined"],
                    color=tuple(c.get("color")),
                    is_particle=c["is_particle"],
                )
                # get that class item and patch it
                class_item = mainwindow.custom_class_list_widget.getItemWidget(
                    mainwindow.custom_class_list_widget.count() - 1
                )
                class_item.is_particle = c["is_particle"]
                class_item._is_class_visible = c["_is_class_visible"]
                class_item.is_user_defined = c["is_user_defined"]
                # TODO: patch extra variables manually

            # add groups (if not exists)
            for g in data_dict["grouped_data"]:
                if not mainwindow.DH.BLobj.groups.get(g["groupName"]):
                    mainwindow.DH.BLobj.addGroup(g["groupName"], uuid=g.get("unique_id"))

                for c in g["condition_objects"]:
                    if len(g["condition_objects"]) == 0:
                        continue
                    if not mainwindow.DH.BLobj.groups[g["groupName"]].conds.get(
                        c["condition_name"]
                    ):
                        mainwindow.add_new_treatment_item(
                            c["condition_name"], c.get("unique_id")
                        )
                    for i in c["image_objects"]:
                        # Read Metadata
                        # get strcut type
                        mode_type = struct.unpack("c", f.read(1))[0].decode("utf-8")
                        # Read Image Data
                        if mode_type == "I":
                            img_data_length = struct.unpack(mode_type, f.read(4))[0]
                        else:  # mode_type == "Q"
                            img_data_length = struct.unpack(mode_type, f.read(8))[0]

                        data_decompressed = dctx.decompress(f.read(img_data_length))
                        fileName = i["fileName"]
                        extension = fileName.split(".")[-1]
                        # generate a random name that does not exist so far
                        image_unique_id = i.get("unique_id")
                        if not image_unique_id:
                            image_unique_id = config.get_unique_id()
                        img_location = os.path.join(
                            config.cache_dir, image_unique_id
                        )
                        img_location = img_location + "." + extension
                        with open(img_location, "wb") as ff:
                            # write binary data_decompressed
                            ff.write(data_decompressed)
                        if "thumbnail" in i:
                            thumbnail = bytes.fromhex(i["thumbnail"])
                        else:
                            thumbnail = None

                        # add image
                        mainwindow.DH.BLobj.groups[g["groupName"]].conds[
                            c["condition_name"]
                        ].addImage_FROM_DISK(
                            imagePath=img_location,
                            group_uuid=g.get("unique_id"),
                            cond_uuid=c.get("unique_id"),
                            thumbnail=thumbnail,  # .encode("koi8_u"),
                            image_uuid=image_unique_id,
                        )
                        io = (
                            mainwindow.DH.BLobj.groups[g["groupName"]]
                            .conds[c["condition_name"]]
                            .images[i["imgID"]]
                        )
                        io.treatment_uuid = c.get("treatment_uuid")
                        io.group_uuid = g.get("group_uuid")
                        io._is_video = i.get("_is_video")
                        io._is_ultra_high_res = i.get("_is_ultra_high_res")
                        io.AcquisitionDate = i["AcquisitionDate"]
                        io.DimensionOrder = i["DimensionOrder"]
                        io.ExperiementName = i["ExperiementName"]
                        io.ExposureTime = i["ExposureTime"]
                        io.ExposureTimeUnit = i["ExposureTimeUnit"]
                        io.ID = i["ID"]
                        io.PhotometricInterpretation = i[
                            "PhotometricInterpretation"
                        ]
                        io.PhysicalSizeX = i["PhysicalSizeX"]
                        io.PhysicalSizeXUnit = i["PhysicalSizeXUnit"]
                        io.PhysicalSizeY = i["PhysicalSizeY"]
                        io.PhysicalSizeYUnit = i["PhysicalSizeYUnit"]
                        io.SignificantBits = i["SignificantBits"]
                        io.SizeC = i["SizeC"]
                        io.SizeT = i["SizeT"]
                        io.SizeX = i["SizeX"]
                        io.SizeY = i["SizeY"]
                        io.SizeZ = i["SizeZ"]
                        io.Software = i["Software"]
                        io.bitDepth = i["bitDepth"]

                        io.channel_list = i["channel_list"]
                        io.computedInference = i["computedInference"]

                        io.hasBeenUploaded = i["hasBeenUploaded"]
                        io.imgID = i["imgID"]
                        io.is_stack = i["is_stack"]
                        io.raw_image_extrema_set = i["raw_image_extrema_set"]
                        io.raw_image_max_value = i["raw_image_max_value"]
                        io.raw_image_min_value = i["raw_image_min_value"]
                        io.resolution = i["resolution"]
                        io.resolutionunit = i["resolutionunit"]
                        io._during_inference = i["_during_inference"]
                        io.userModifiedAnnotation = i["userModifiedAnnotation"]
                        io.thumbnailGenerated = i["thumbnailGenerated"]
                        # add masks
                        for m in i["mask_objects"]:
                            arr = m["polygon_array"]
                            if m["mask_type"] == "bitmap":
                                arr = get_array_from_storage(arr)
                            else:
                                # need to convert array within the list into numpy
                                arr = [np.array(a) for a in arr[0]]
                            mainwindow.DH.BLobj.groups[g["groupName"]].conds[
                                c["condition_name"]
                            ].images[-1].addMaskWithClass(
                                arr,
                                class_id=m["class_id"],
                                mask_type=m["mask_type"],
                                unique_id=m["unique_id"],
                                visibility=m["visibility"],
                                includedInAnalysis=m["includedInAnalysis"],
                            )
                            mo = (
                                mainwindow.DH.BLobj.groups[g["groupName"]]
                                .conds[c["condition_name"]]
                                .images[-1]
                                .masks[m["unique_id"]]
                            )
                            mo.class_group_id = m["class_group_id"]
                            mo.spatial_id = m["spatial_id"]
                            mo.score = m["score"]
                            mo.includedInAnalysis = m["includedInAnalysis"]
                            mo.mask_type = m["mask_type"]
                            mo.is_suggested = m["is_suggested"]
                            mo._annotation_track_id = m["_annotation_track_id"]
                            mo.intensity_metrics = m["intensity_metrics"]
                            if hasattr(m, "particle_metrics"):
                                mo.particle_metrics = m["particle_metrics"]

        if mainwindow.custom_class_list_widget.count():
            # set the first class item as the active one
            mainwindow.custom_class_list_widget.setCurrentRow(0)
        if mainwindow.RNAi_list.count():
            QtWidgets.QApplication.processEvents()
            # Select the first item
            first_item = mainwindow.RNAi_list.item(0)
            mainwindow.RNAi_list.setCurrentItem(first_item)
            # Manually call the method that handles item selection
            # Trigger a scene refresh and image preview area refresh
            config.global_signals.refresh_image_preview_graphicsscene_signal.emit()
            config.global_signals.load_main_scene_signal.emit()
            mainwindow.switch_treatment_onchange(
                first_item
            )  # update the image buttons to match the treatment
        return images
    except Exception as e:
        logger.error(e)

        mainwindow.stackedWidget.setCurrentWidget(prior_location)
        # quit session
        mainwindow.quit_project(without_prompt=True)

        config.global_signals.fatalErrorSignal.emit("Failed to read file.")
