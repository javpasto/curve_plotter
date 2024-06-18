import subprocess
import sys

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_package("wxPython")
install_package("numpy")
install_package("matplotlib")
install_package("sympy")
install_package("graphviz")
install_package("numpy")
install_package("numpy")
