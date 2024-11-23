from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files("bioio", include_py_files=True)
datas += collect_data_files("bioio-ome-tiff", include_py_files=True)
datas += collect_data_files("bioio-ome-zarr", include_py_files=True)
datas += collect_data_files("bioio-imageio", include_py_files=True)
datas += collect_data_files("bioio-tifffile", include_py_files=True)
datas += collect_data_files("bioio-tiff-glob", include_py_files=True)
