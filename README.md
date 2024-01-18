# ConfigStore

## Start
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
## Test

```
pip install -e .
```

```
pytest
```

## TODO

- "rollback" functionality
- permission to write to _/var/local/_
- use `commit.authored_date` for timestamps
