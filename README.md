# Curve Plotter

# Installation

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

Here's an improved version of the user guide with corrections and enhancements for clarity:

# User Guide

![curve_plotter_final](https://github.com/javpasto/curve_plotter/assets/24668344/4d35cd31-e39b-4946-aecd-a31a33a762ed)

1. **Defining Curve Functions**: Each curve must have a unique name. For 2D plots (defined in **6**), both x and y functions must be specified. For 3D plots, x, y, and z functions must be specified. The color can be selected from the combo box; the default color is blue.
2. **Defining Range Parameters**: The lower bound must be less than the upper bound. The step size, defined in **6**, determines the spacing between points.
3. **Defining Additional Parameters**: Each parameter must have a unique name.
4. **Defining Vectors**: Each vector must have a unique name, an initial point, and a value. Values should be entered with dimensions separated by commas. For 2D plots (defined in **6**), the initial point and value should each consist of two numbers separated by a comma. For 3D plots, they should each consist of three numbers separated by commas. The color can be selected from the combo box; the default color is red.
5. **Defining Plot Limits**: Each lower bound must be less than the corresponding upper bound. The default bounds are -10 for the lower bound and 10 for the upper bound.
6. **Setting Steps**: The step size determines the accuracy of the computations. More steps will increase accuracy but will take more time. The default step size is 10,000. The 2D plot option allows for plotting in 2D; by default, plotting is in 3D. The "Plot Curve" button generates the plot based on the defined objects.

The lexicon consists of reserved letters (e.g., $\alpha$ = al, $\beta$ = be), known constants (e.g., π, e), and known functions (e.g., cos, sin).
