from gc import collect
from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('skimage', include_py_files=True)
