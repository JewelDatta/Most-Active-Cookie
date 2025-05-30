# Most Active Cookie

A command-line tool to find the most active cookie(s) for a given date from a log file.

## Project Structure
```
most-active-cookie/
│
├── most_active_cookie.py       # Main script
├── tests/                      # Unit tests
│   └── test_most_active_cookie.py
├── Makefile                    # Build & test automation
├── README.md                   # Project documentation
└── cookie_log.csv              # Sample CSV input
└── requirements.txt # Python dependencies
```

## Install dependencies:

```
pip install -r requirements.txt
```

## Usage

### 1. Build a Standalone Executable

```
make build
```

### 2. How to run from CLI
```
./dist/most_active_cookie most_active_cookie.py -f path/to/cookie_log.csv -d YYYY-MM-DD

```
#### Example
```
./dist/most_active_cookie -f cookie_log.csv -d 2018-12-09
```

## Running Tests

```
make test
```

## Run with coverage report:

```
make coverage
```

## Linting and Type Checks

```
make lint     # Run pylint
make mypy     # Run mypy type checks
```

## Clean Build Files

```
make clean
```

Example Input as cookie_log.csv
 
```
cookie,timestamp
AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00
SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00
5UAVanZf6UtGyKVS,2018-12-09T07:25:00+00:00
AtY0laUfhglK3lC7,2018-12-09T06:19:00+00:00
SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00
4sMM2LxV07bPJzwf,2018-12-08T21:30:00+00:00
fbcn5UAVanZf6UtG,2018-12-08T09:30:00+00:00
4sMM2LxV07bPJzwf,2018-12-07T23:30:00+00:00
```

## Output

AtY0laUfhglK3lC7
