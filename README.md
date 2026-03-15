# compliance-flow-etl

## Overview
**compliance-flow-etl** is a production-grade data engineering pipeline designed to ingest high-sensitivity SEC Insider Trading disclosures while maintaining 100% PII security through automated masking and validation.

## Architecture
This system implements a "Defensive Anonymization" pattern:
1. **Extraction:** Real-time executive trading data is pulled from the Yahoo Finance API.
2. **Cryptographic Masking:** Identities are transformed using **Salted SHA-256 Hashing** at the point of ingestion to prevent rainbow table attacks.
3. **Automated Unit Testing:** A built-in integrity check scans the final dataset to ensure zero raw PII leakage.
4. **Data Quality Gate:** The CI/CD pipeline validates file size and presence before committing to the repository.

## Tech Stack
* **Language:** Python 3.10 (Pandas, Hashlib)
* **API:** yfinance
* **Orchestration:** GitHub Actions
* **License:** MIT
