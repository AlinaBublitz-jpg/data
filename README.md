# Data Analysis and Manipulation Project

## Introduction

The Data Analysis and Manipulation Project is a Python-based tool designed for comprehensive data analysis and manipulation. Utilizing a database connection, this tool enables users to perform a wide range of operations including creating tables, loading data from CSV files, analyzing data to find the best fits, testing datasets, and writing test results back to the database.

## Table of Contents

-   [Introduction](#introduction)
-   [Installation](#installation)
-   [Usage](#usage)
-   [Features](#features)
-   [Dependencies](#dependencies)
-   [Documentation](#documentation)
-   [Troubleshooting](#troubleshooting)

## Installation

Before running the project, ensure that Python is installed on your system. Follow these steps to set up the project environment:

1. Clone the project repository to your local machine.
2. Open your terminal and navigate to the project directory.
3. Install the necessary Python packages by running:

```sh
pip install -r requirements.txt
```

## Usage

To use the Data Analysis and Manipulation tool, follow these steps:

1. Ensure you have the necessary permissions to read/write to the database and access the CSV files.
2. Run the `main.py` script by typing the following command in your terminal:

```sh
python src/main.py
```

## Features

-   **Database Integration:** Connects to a database to perform read/write operations.
-   **Data Analysis:** Analyzes curves to find the best fits.
-   **Data Handling:** Handles data operations like creating tables and loading data from CSV files.
-   **Results Writing:** Writes the test results back to the database.

## Dependencies

-   Python (3.x recommended)
-   Additional Python packages as listed in `requirements.txt`.

## Documentation

The project documentation is embedded within the code through comments.

## Troubleshooting

-   Ensure all Python dependencies are installed.
-   Verify database connection credentials and permissions.
-   Check the paths to CSV files and ensure they are accessible.
