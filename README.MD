# Healthcare Coding Explorer

A Streamlit dashboard that flags unusual diagnosis coding patterns in synthetic Medicare claims — and explains each flag in plain English.

## What it does

Scans beneficiary claims year over year and flags patterns worth a second look, with a 0-100 anomaly score:

1. Diagnosis count jumps sharply year over year
2. A chronic condition appears one year and vanishes the next
3. Risk score jumps with no inpatient claim to explain it
4. Same condition coded by an unusually high number of different providers

This is a personal learning / portfolio project — a product-style rebuild of a coding-integrity problem, built entirely on public synthetic data.

## Who it's for

A health plan coding-integrity lead who needs to quickly find *which* beneficiaries to review first, and *why* they were flagged.

## Data source

CMS DE-SynPUF (Data Entrepreneurs' Synthetic Public Use Files), Sample 1, 2008-2010.
Fully synthetic, fictional Medicare beneficiaries — free from CMS for software development and training.

Raw data files are NOT in this repo. They stay locally in `data_raw/` (see `.gitignore`).

## Important note

Synthetic data only. Never real claims, never anything from work / employer systems.

Demo on synthetic data. Flags are patterns worth a second look, not findings of incorrect coding.

## Status

Work in progress. Day 1: repo set up and Streamlit app shell running.

## How to run locally

1. Clone this repo
2. Install: `pip install streamlit pandas`
3. Run: `streamlit run app.py`
4. Open: http://localhost:8501

