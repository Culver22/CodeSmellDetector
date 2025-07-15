# CodeSmellDetector

This Program is a Python tool designed to analyse common code smells - indicators of potential issues that would impact
code quality, readability and maintainability. The project includes a user-friendly GUI, built with Tkinter, for 
easy interaction and inspection.

### Features

- Detect Long Functions: Flags functions that exceed a configurable number of lines, helping identify bloated methods.


- Detect Large Classes: Identifies classes with an excessive number of methods that might benefit from refactoring.


- Detect Functions with Too Many Parameters: Flags functions with complex parameter lists, which are often harder to 
  maintain.
  

- Detect Deep Nesting: Finds functions with deeply nested control structures, a common source of code complexity.


### Demo

Upon execution the user will be presented with a simple GUI:

![img_1.png](img_1.png)

From here clicking 'Browse' will enable the user to choose a python file (.py) from their system:

![img_2.png](img_2.png)

After choosing a file, the filepath will be shown in the GUI - confirming their choice. They may then click 'Run Smell
Detection':

![img_4.png](img_4.png)

They are then able to 'Browse' again, if not - closing the 'Code Smell Detector' window will end the program


To Add:

Add a function in order to exclude blank lines and docstrings in long function smell test


### Sources
https://www.tutorialspoint.com/python/tk_button.htm (Buttons)
https://www.geeksforgeeks.org/python/file-explorer-in-python-using-tkinter/ (File explorer)