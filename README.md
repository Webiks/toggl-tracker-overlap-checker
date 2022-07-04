# Toggl Tracker Overlap Checker

Check for reports overlap in exported CSV reports from toggl tracker.

## Getting Started

### Dependencies

* Python 3.6+ and pandas

### Installing

Clone the repository:

```bash
cd projects
git clone https://github.com/Webiks/toggl-tracker-overlap-checker.git
```

(optional) Create and activate virtual environment:

```bash
cd projects/toggl-tracker-overlap-checker
python -m venv .venv
.venv/bin/activate
```

If you are running from windows then last line should be:

```bash
.venv/Scripts/activate.bat
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Run the script

In Toggl Tracker website:

* Go to reports
* Select detailed
* Select last month
* Click on export report (top/right download icon)
* Click on "download CSV"
* Wait for download to complete

Run the script with exported report:

```bash
cd projects/toggl-tracker-overlap-checker
python check.py [downloaded report] -o [output filename]
```

For example:

```bash
python check.py Toggl_time_entries_2022-06-01_to_2022-06-30.csv -o toggl_overlaps_2022-06.csv
```
