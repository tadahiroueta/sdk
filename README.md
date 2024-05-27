# SDK
***My sudoku solver made with pure Python***

[Built With](#built-with) · [Installation](#installation) · [Usage](#usage)

## Built With
- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## Installation

1. Install [Python](https://www.python.org/downloads/)

2. Clone repository
    ```sh
    git clone https://github.com/tadahiroueta/sdk.git
    ```

    > It's that simple

## Usage
1. Run
    ```sh
    python sdk.py
    ```
  
2. Type in your unsolved sudoku table
    - Line by line
    - With a space in between numbers
    - Enter a 0 (zero) for unknown numbers
    - For example:

    ```sh
    >>>    0 0 1 0 0 8 0 7 2
    >>>    6 4 9 2 0 0 0 0 0
    >>>    8 0 7 6 3 0 0 4 0
    >>>    0 5 3 0 0 0 0 0 0
    >>>    2 0 0 0 0 4 3 9 0
    >>>    4 0 0 8 2 0 1 0 0
    >>>    0 6 0 0 0 7 4 1 5
    >>>    1 8 5 0 9 2 0 6 0
    >>>    0 7 0 0 0 6 9 2 0
    ```
  
3. Read the solution

    ```sh
    5 3 1 9 4 8 6 7 2
    6 4 9 2 7 5 8 3 1
    8 2 7 6 3 1 5 4 9
    7 5 3 1 6 9 2 8 4
    2 1 8 7 5 4 3 9 6
    4 9 6 8 2 3 1 5 7
    9 6 2 3 8 7 4 1 5
    1 8 5 4 9 2 7 6 3
    3 7 4 5 1 6 9 2 8
    ```
    > Many sudoku problems have multiple correct solutions. The algorithm may give one of these solutions.