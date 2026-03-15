# Project Sentinel: Compliance-First Financial ETL

## Overview
**Project Sentinel** is a production-grade Data Engineering pipeline designed to ingest high-sensitivity SEC Insider Trading disclosures while maintaining 100% PII (Personally Identifiable Information) security. Licensed under the MIT License.

## The "Blindfold" Architecture
This system is built on the principle of **Defensive Anonymization**:
1. **Extraction:** Real-time data is pulled from the Yahoo Finance API.
2. **Cryptographic Masking:** Identities are transformed using **Salted SHA-256 Hashing**. 
3. **Automated Unit Testing:** A built-in integrity check scans the data before export to ensure zero raw PII leakage.
4. **Data Quality Gate:** The CI/CD pipeline validates the output file existence and size before committing to the repository.

## Security Controls
* **Salted Hashing:** Prevents rainbow table attacks by injecting a high-entropy "Salt" from GitHub Secrets.
* **Ephemeral Execution:** Data is processed in a temporary cloud runner; no raw data ever touches local storage.
* **Audit Trail:** Every transformation is logged and timestamped via GitHub Actions.

## Tech Stack
* **Engine:** Python 3.10 (Pandas, Pytest-style logic)
* **API:** yfinance
* **CI/CD:** GitHub Actions (Node.js 24 Runtime)
* **License:** MIT
