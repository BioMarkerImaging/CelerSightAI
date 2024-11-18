from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files("aicsimageio", include_py_files=True)
