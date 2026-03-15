# Compliance Flow ETL

## Overview
**Compliance Flow ETL** is a data engineering pipeline designed to ingest high-sensitivity SEC Insider Trading disclosures while maintaining 100% PII (Personally Identifiable Information) security. 

## Architecture
This system implements a "Blindfolded" data processing pattern:
1. **Extraction:** Real-time executive trading data is pulled from the Yahoo Finance API.
2. **Cryptographic Masking:** Sensitive identities are transformed using **Salted SHA-256 Hashing** at the point of ingestion. 
3. **Automated Testing:** An integrity check scans the final dataset to ensure zero raw PII leakage.
4. **Validation:** A CI/CD Data Quality gate verifies file integrity before storage.

## Tech Stack
* **Language:** Python 3.10
* **API:** yfinance
* **CI/CD:** GitHub Actions
* **License:** MIT
