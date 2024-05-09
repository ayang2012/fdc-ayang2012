# Fig Data Challenge

This project demonstrates a quick data pipeline to process small csv files.
```
├── data/
└── src
    ├── fig_data_challenge
    │   └── main.py
    └── tests
        ├── test_data/
        └── test_main.py
```
The above file structure displays the main files used for running the script. The data/ folder contains the xlsx file we are processing. The src/ folder contains the actual engine for processing. The tests/ for ensuring the scripts are running properly.

![alt text](image.png)

The above is the ERD for this challenge. It can be modified additionally in the future given a better understanding of usual business questions being asked.

## How to run

Navigate to the root folder, then run the following `make setup` and `make run-main`commands

```bash
setup:
	poetry install
	poetry run pre-commit install

run-main:
	poetry run python src/main.py

lint:
	poetry run flake8 src/ tests/

test:
	poetry run pytest

```

There will also be an output file written in the `debug_output` folder with any dropped rows due to NA values.
