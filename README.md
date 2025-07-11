# LSTM-CryptoForecast

# 💹 Crypto Visualizer & Prediction Model

This Python application fetches, visualizes, and predicts cryptocurrency price trends using LSTM neural networks. It combines real-time data scraping, a custom PyQt6 UI, and deep learning to give intuitive insights into market movements.

## 🧠 Features

- 📈 Live cryptocurrency price visualization with custom UI  
- 🧠 LSTM-based prediction model trained on technical indicators  
- 🛠️ Easy-to-use CLI for training and real-time display  
- ☁️ Automatic data scraping from Crypto.com API using CloudScraper  
- 🧮 Computation of RSI, EMA, MACD indicators using `pandas_ta`  
- 💾 Model saving/loading using TensorFlow and `joblib`  

## 📦 Requirements

Install all dependencies via:

```bash
pip install -r requirements.txt
```
## 🚀 Usage

Show Live Crypto Data
```bash
python main.py --crypto BTC --interval d
```
- `--crypto`: Cryptocurrency symbol (e.g., BTC, ETH)
- `--interval`: Time interval (h, d, w, m, y)

Train the Model
```bash
python train.py --csv_path ./coin_Bitcoin.csv --epochs 20
```
- `--csv_path`: Path to the training CSV file
- `--epochs`: Number of training epochs
- `--new`: Set True to build a new model

## 🧾 File Structure

- `main.py` – Main entry point for the live visualizer
- `train.py` – CLI script to train or retrain the model
- `model.py` – TensorFlow model logic (load, train, predict)
- `script.py` – Scraper and Crypto.com API interface
- `widget.py` – PyQt6 GUI class for graph and controls
- `crypto.json` – Cached list of available tokens

## 📊 Prediction Output

The model predicts one of three classes:

- `0`: Price drop
- `1`: Stable price
- `2`: Price increase

The GUI updates the plot color accordingly:

- 🟢 Green: Up
- 🟡 Yellow: Stable
- 🔴 Red: Down

## 📍 Notes

You must have a valid CSV for training that includes columns like : `SNo`, `Name`, `Symbol`, `Date`, `High`, `Low`, `Open`, `Close`, `Volume`, `Marketcap`

[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)
