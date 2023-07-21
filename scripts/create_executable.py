import sysconfig
import PyInstaller.__main__
from os import pathsep
from PyInstaller.utils.hooks import collect_submodules
from sys import exit
import os

PYTHON_SITE = sysconfig.get_paths()["purelib"]
reportlab_submodules = collect_submodules('reportlab.graphics.barcode')

arguments = [
    '--onefile',
    '--name=MeasureAnalysis',
    f'--add-data=template/template.html{pathsep}template',
    f'--add-data=template/NotoSans-Regular.ttf{pathsep}template',
    '--hidden-import=sklearn.neighbors._typedefs',
    '--hidden-import=sklearn.utils.sparsetools._graph_validation',
    '--hidden-import=sklearn.utils.sparsetools._graph_tools',
    '--hidden-import=sklearn.utils.lgamma',
    '--hidden-import=sklearn.utils._cython_blas',
    '--hidden-import=sklearn.neighbors._quad_tree',
    '--hidden-import=sklearn.tree._utils',
    '--hidden-import=threadpoolctl',
    './main.py'
]

if os.name == "nt":
    arguments.append(f'--add-data={PYTHON_SITE}/sklearn/.libs/vcomp140.dll{pathsep}sklearn/.libs')
    arguments.append('--hidden-import=pkg_resources.py2_warn')

for submodule in reportlab_submodules:
    arguments.append(f'--hidden-import={submodule}')

PyInstaller.__main__.run(arguments)
