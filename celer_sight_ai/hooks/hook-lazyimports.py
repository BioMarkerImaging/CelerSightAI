from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files("lazy_import", include_py_files=True)
