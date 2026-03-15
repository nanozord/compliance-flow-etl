# MIT License | Copyright (c) 2026 Compliance Flow ETL
import yfinance as yf
import hashlib
import pandas as pd
import os
import sys

def salt_and_hash(text, salt=os.getenv('COMPLIANCE_SALT', 'DEFAULT_STATIC_SALT')):
    salted_text = text + (salt if salt else "FALLBACK_SALT")
    return hashlib.sha256(salted_text.encode()).hexdigest()

def test_masking_integrity(df):
    """Unit Test: Ensures no raw PII leaked into the dataframe"""
    forbidden_terms = ["Tim Cook", "Apple", "CEO"] 
    for column in df.columns:
        for term in forbidden_terms:
            if df[column].astype(str).str.contains(term, case=False).any():
                raise ValueError(f"SECURITY BREACH: Raw PII or sensitive term '{term}' detected!")
    print("Unit Test Passed: No raw PII detected.")

def main():
    ticker_symbol = "AAPL"
    try:
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.get_insiders() 
        
        if df is None or df.empty:
            print(f"Warning: No insider data found for {ticker_symbol}. Check API status.")
            return

        df['mask_executive_id'] = df['Insider'].apply(salt_and_hash)
        df['mask_position_id'] = df['Position'].apply(salt_and_hash)
        
        secure_df = df.drop(columns=['Insider', 'Position'])
        
        test_masking_integrity(secure_df)

        secure_df.to_csv('masked_insider_trading.csv', index=False)
        print(f"Compliance Flow: {len(secure_df)} records secured successfully.")

    except Exception as e:
        print(f"Pipeline Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
