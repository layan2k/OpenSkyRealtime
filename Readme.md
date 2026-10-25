# OpenSky Realtime

OpenSky Realtime fetches the current aircraft state data from the OpenSky
Network API and appends the selected flight-position fields to a PostgreSQL
database.

## How it works

Running `main.py` calls `opensky.fetch_data()`, which:

1. Requests data from `<OPENSKY_API>/states/all`.
2. Converts the response into a pandas DataFrame.
3. Keeps aircraft identity, position, altitude, speed, and timestamp fields.
4. Converts the API timestamps to datetime values.
5. Appends the records to the PostgreSQL `flight_position` table.

## Requirements

- Python 3.10 or newer
- A PostgreSQL database
- Access to the OpenSky Network API

Python dependencies are pinned in [`requirements.txt`](requirements.txt).

## Setup

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
```

On Windows:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

Create a `.env` file in the project root with the following settings:

```dotenv
OPENSKY_API=https://opensky-network.org/api
DATABASE_USERNAME=your_postgres_username
DATABASE_PASSWORD=your_postgres_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=your_database_name
```

Do not commit `.env`; it is excluded by `.gitignore`.

## Run

From the project root, run:

```bash
python main.py
```

Successful runs report the number of rows appended to PostgreSQL. Network
request and database errors are printed and terminate the process with a
non-zero exit status.

## Stored data

The application writes to the `flight_position` table using pandas
`DataFrame.to_sql(..., if_exists="append")`. The stored columns are:

| Column | Description |
| --- | --- |
| `icao24` | Aircraft ICAO 24-bit transponder address |
| `callsign` | Aircraft callsign |
| `origin_country` | Country of origin |
| `time_position` | Time when the position was generated |
| `last_contact` | Time when the aircraft was last contacted |
| `latitude` | Latitude in degrees |
| `longitude` | Longitude in degrees |
| `baro_altitude` | Barometric altitude |
| `geo_altitude` | Geometric altitude |
| `velocity` | Ground speed |

The timestamps returned by the API are Unix timestamps and are converted to
datetime values before insertion.

## Project files

| File | Purpose |
| --- | --- |
| `main.py` | Application entry point |
| `opensky.py` | API request, transformation, and database insertion logic |
| `requirements.txt` | Pinned Python dependencies |
| `.env` | Local API and database configuration |
