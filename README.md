# Curve Plotter

## Installation

First, download Python:

[Download Python](https://www.python.org/downloads/)

Then, install pip:

[Install pip](https://pip.pypa.io/en/stable/installation/)

## Libraries Installation

Next, you can run the `setup.py` file to install all the necessary libraries, or you can download them directly (in any order):

- **Install wxPython**: [wxPython](https://pypi.org/project/wxPython/)
- **Install numpy**: [numpy](https://numpy.org/install/)
- **Install matplotlib**: [matplotlib](https://matplotlib.org/stable/install/index.html)
- **Install sympy**: [sympy](https://pypi.org/project/sympy/)
- **Install graphviz**: [graphviz](https://pypi.org/project/graphviz/)

## Generate Distributable

Run the following command in the terminal where your project is located.

```sh
pyinstaller --onefile --windowed curve_plotter.py
```

The executable file will be generated in the `/dist` folder.

If the firewall prevents you from generating the `.exe` file, you should add an exception in the security settings for the project folder.
