# F1 Predictions Scoreboard
This is a small program written in python that can be used to check how good your guess of the F1 standings is. It uses [raylib](https://electronstudio.github.io/raylib-python-cffi/README.html) 
for the graphics and [requests](https://requests.readthedocs.io/en/latest/) to collect the standings data from the [official driver standings](https://www.formula1.com/en/results.html/2023/drivers.html).

## Installation
- First, clone this project or download the source file .zip from the releases and extract it wherever you like on your computer.
- If you do not have have python installed on your computer, you will need to download and install it from [here](https://www.python.org/downloads/) before continuing. *Remember* when installing python it
  is important to check the box in the installer to add python to your computer's PATH.
- This program relies on the raylib and request libraries. These can be installed through pip, the file **install_dependencies.bat** will do this for you, just double click it, if the libraries install successfully
  then you can delete this file.
- You are now ready to run the program, just double click the **RUN.bat** file!

## Usage
If you wish to add your own custom prediction, go into the recources folder and open the **guesses.ini** file, this file uses a comma seperated values format for the guesses, with the name of the guess in the first
column then the three letter initials of the drivers in capital letters ordered from first to last as the guess. See the file for an example.
