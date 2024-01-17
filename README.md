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

- `store_conf` should handle lists of `device_name` mapping to multiple files
- "rollback" functionality
- permission to write to _/var/local/_
