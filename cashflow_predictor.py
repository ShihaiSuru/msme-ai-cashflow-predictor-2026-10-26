#!/usr/bin/env python3
"""
MSME AI Cash Flow Predictor
Starter demo script for forecasting cash flow for Indian MSMEs.

Analyzes sample UPI, invoice, and expense data to generate simple forecasts.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data():
    """Generate realistic sample data for an Indian MSME (e.g., small trader or manufacturer)."""
    dates = pd.date_range(start='2026-09-01', periods=60, freq='D')
    
    # Sample UPI inflows (sales collections)
    upi_inflows = np.random.normal(25000, 8000, 60)
    upi_inflows = np.clip(upi_inflows, 5000, 80000)
    
    # Sample expenses
    expenses = np.random.normal(18000, 5000, 60)
    expenses = np.clip(expenses, 3000, 45000)
    
    # Occasional large GST payments
    gst_payments = np.zeros(60)
    gst_payments[30] = 45000  # Mid-month GST
    gst_payments[59] = 38000
    
    df = pd.DataFrame({
        'date': dates,
        'upi_inflow': upi_inflows,
        'expenses': expenses,
        'gst_outflow': gst_payments
    })
    
    df['net_cashflow'] = df['upi_inflow'] - df['expenses'] - df['gst_outflow']
    df['running_balance'] = df['net_cashflow'].cumsum() + 150000  # Starting balance
    
    return df

def forecast_cashflow(df, days=30):
    """Simple moving average + seasonal forecast for next N days."""
    avg_inflow = df['upi_inflow'].tail(30).mean()
    avg_expense = df['expenses'].tail(30).mean()
    
    # Add slight growth assumption for MSME
    growth_factor = 1.02
    
    forecasts = []
    last_balance = df['running_balance'].iloc[-1]
    
    for i in range(1, days + 1):
        forecast_date = df['date'].iloc[-1] + timedelta(days=i)
        forecast_inflow = avg_inflow * growth_factor
        forecast_expense = avg_expense
        # Assume GST every 30 days roughly
        gst = 40000 if i % 30 == 0 else 0
        
        net = forecast_inflow - forecast_expense - gst
        last_balance += net
        
        forecasts.append({
            'date': forecast_date.strftime('%Y-%m-%d'),
            'predicted_inflow': round(forecast_inflow, 2),
            'predicted_expense': round(forecast_expense, 2),
            'predicted_gst': gst,
            'predicted_net': round(net, 2),
            'predicted_balance': round(last_balance, 2)
        })
    
    return pd.DataFrame(forecasts)

def estimate_working_capital(df, forecast_df):
    """Estimate working capital needs based on forecast lows."""
    min_balance = forecast_df['predicted_balance'].min()
    current_balance = df['running_balance'].iloc[-1]
    buffer_needed = max(0, 100000 - min_balance)  # Target min buffer of 1L
    
    return {
        'current_balance': round(current_balance, 2),
        'forecast_min_balance': round(min_balance, 2),
        'recommended_working_capital_buffer': round(buffer_needed, 2),
        'avg_monthly_gst': round(df['gst_outflow'].sum() / 2, 2)  # Approx
    }

def main():
    print("=" * 60)
    print("MSME AI Cash Flow Predictor - Demo")
    print("Focused on Indian MSMEs | Created 2026-10-26")
    print("=" * 60)
    
    # Load / generate data
    df = generate_sample_data()
    print(f"\nSample data loaded: {len(df)} days of transactions")
    print(f"Current running balance: ₹{df['running_balance'].iloc[-1]:,.2f}")
    
    # Generate forecast
    forecast = forecast_cashflow(df, days=30)
    print("\n--- 30-Day Cash Flow Forecast ---")
    print(forecast[['date', 'predicted_net', 'predicted_balance']].to_string(index=False))
    
    # Working capital analysis
    wc = estimate_working_capital(df, forecast)
    print("\n--- Working Capital Analysis ---")
    for k, v in wc.items():
        print(f"{k.replace('_', ' ').title()}: ₹{v:,.2f}" if isinstance(v, (int, float)) else f"{k}: {v}")
    
    print("\nTip: Connect real UPI / bank data via Account Aggregator for production use.")
    print("This is a starter demo for MSME fintech tools.")

if __name__ == "__main__":
    main()
