# Data Seeds

This folder holds local seed data for the verification service.

Files
- `seed_entities.json`: JSON array of entities used by the FileDataProvider.

Schema (per item)
- `legal_name`: string, required
- `address_line1`: string, required
- `city`: string, required
- `country`: ISO2, uppercase (e.g., US, GB)
- `registration_status`: Active | Inactive | Unknown

Usage
- The API loads this file by default. Override with `DATA_SEED_PATH` env var.
- JSON does not support comments; keep notes here in README.
- Tests and examples reference "Acme Corp" (US) and "Globex LLC" (GB).

