# MIT License | Copyright (c) 2026 Compliance Flow ETL
import yfinance as yf
import hashlib
import pandas as pd
import os
import sys

def salt_and_hash(text, salt=os.getenv('COMPLIANCE_SALT', 'DEFAULT_STATIC_SALT')):
    # Ensure text is a string before hashing
    text_str = str(text) if text is not None else ""
    salted_text = text_str + (salt if salt else "FALLBACK_SALT")
    return hashlib.sha256(salted_text.encode()).hexdigest()

def test_masking_integrity(df):
    """Unit Test: Ensures no raw PII leaked into the dataframe"""
    # Expanded list to catch common identifiers
    forbidden_terms = ["Tim Cook", "Apple", "CEO", "Director", "Officer"] 
    for column in df.columns:
        # Check if any forbidden term exists as a substring in the column
        if df[column].astype(str).str.contains('|'.join(forbidden_terms), case=False, na=False).any():
            raise ValueError(f"SECURITY BREACH: Sensitive term or PII detected in column '{column}'!")
    print("Unit Test Passed: No raw PII detected.")

def main():
    ticker_symbol = "AAPL"
    try:
        ticker = yf.Ticker(ticker_symbol)
        
        # FIX: Changed get_insiders() to the property .insiders
        df = ticker.insiders 
        
        if df is None or df.empty:
            print(f"Warning: No insider data found for {ticker_symbol}. API may be restricted.")
            return

        # Data Cleaning: Ensure columns exist before masking
        if 'Insider' not in df.columns or 'Position' not in df.columns:
            print("Error: Unexpected data format from API.")
            sys.exit(1)

        # Apply masking
        df['mask_executive_id'] = df['Insider'].apply(salt_and_hash)
        df['mask_position_id'] = df['Position'].apply(salt_and_hash)
        
        # Drop original PII columns
        secure_df = df.drop(columns=['Insider', 'Position'])
        
        # Run automated safety check
        test_masking_integrity(secure_df)

        secure_df.to_csv('masked_insider_trading.csv', index=False)
        print(f"Compliance Flow: {len(secure_df)} records secured successfully.")

    except Exception as e:
        print(f"Pipeline Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
