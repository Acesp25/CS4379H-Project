# CS 4379H - Team Project
**Group 2:** Aaron Espinoza, Skylar McCauley, John Mattes

## Getting Started

### Prerequisites
* conda
* Python 3.14.8+
* pip

### Installation

#### Make a new virt env:

`conda create --name myenv`

`conda activate myenv`

* Feel free to replace "myenv" with whatever name you want to give to your new conda virtual environment.

#### Clone the repository:

`git clone https://github.com/Acesp25/CS4379H-Project.git`

`cd CS4379H-Project`

#### Install dependencies:

`pip install -r requirements.txt`

### Usage

* Depending on your operating system, use either "python" or "python3" for the following commands.

#### First change directory to "src":

`cd CS4379H-Project/src`

#### To run the project as intended:

`python3 -m cli_tool`

#### To run *ONLY* the (refactored) original program:

`python3 -m original_refactored`

#### To run *ONLY* the compact PLS variant:

`python3 -m compact_pls`

#### To run *ONLY* the dropped hex encoding variant:

`python3 -m drop_hex_encode`

#### To run *ONLY* the variant without PLS:

`python3 -m no_pls`

### Features

TODO: Add descriptive information about the different variants after they are built.

### Acknowledgements

We built our project on top of the work by Sahil Gangurde and Krishnakant Tiwari who go by the GitHub usernames of "lost_martian" and "Iamkkant". All credit for the original program goes to them. Here is a link to their original work: https://github.com/lostmartian/LSB-Steganography-using-Pixel-Locator-Sequence-With-AES.
