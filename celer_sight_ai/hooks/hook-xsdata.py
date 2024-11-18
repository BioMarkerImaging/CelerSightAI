from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files("xsdata_pydantic_basemodel", include_py_files=True)
datas += collect_data_files("xsdata_pydantic", include_py_files=True)
datas += collect_data_files("xsdata", include_py_files=True)

