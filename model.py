import pandas as pd
import pandas_ta as ta
import numpy as np
import json
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras import layers, models
import joblib

class TensorModel:
    def __init__(self, csv_path=None, future_window=5, sequence_length=30):
        self.future_window = future_window
        self.sequence_length = sequence_length
        self.model = None
        self.scaler = MinMaxScaler()
        if csv_path:
            self.csv_path = csv_path
            self._load_and_prepare_data()
        else:
            self.model = models.load_model('crypto_signal_model.h5')
            self.scaler = joblib.load('scaler.save')

    def _load_and_prepare_data(self):
        df = pd.read_csv(self.csv_path)
        df['Date'] = pd.to_datetime(df['Date'])
        df.sort_values('Date', inplace=True)
        df.set_index('Date', inplace=True)

        df['rsi'] = ta.rsi(df['Close'], length=14)
        df['ema'] = ta.ema(df['Close'], length=20)
        df['macd'] = ta.macd(df['Close'])['MACD_12_26_9']

        df.dropna(inplace=True)

        df['price_change'] = df['Close'].shift(-self.future_window) - df['Close']

        def get_label(change):
            if change > 0.5:
                return 2  # Up
            elif change < -0.5:
                return 0  # Down
            else:
                return 1  # Stable

        df['label'] = df['price_change'].apply(get_label)

        df.dropna(inplace=True)

        self.df = df
        self._create_sequences()

    def _create_sequences(self):
        X, y = [], []
        features = ['Close', 'Volume', 'rsi', 'ema', 'macd']
        data = self.df[features].values
        data_scaled = self.scaler.fit_transform(data)
        labels = self.df['label'].values

        for i in range(self.sequence_length, len(data_scaled) - self.future_window):
            X.append(data_scaled[i - self.sequence_length:i])
            y.append(labels[i + self.future_window - 1])

        self.X = np.array(X)
        self.y = np.array(y)

    def build_model(self):
        model = models.Sequential()
        model.add(layers.LSTM(64, return_sequences=True, input_shape=(self.X.shape[1], self.X.shape[2])))
        model.add(layers.Dropout(0.2))
        model.add(layers.LSTM(64))
        model.add(layers.Dropout(0.2))
        model.add(layers.Dense(3, activation='softmax'))

        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        self.model = model

    def train(self, epochs=10, batch_size=32):
        if self.model is None:
            self.build_model()
        self.model.fit(self.X, self.y, epochs=epochs, batch_size=batch_size, validation_split=0.2)
        self.model.save('crypto_signal_model.h5')
        joblib.dump(self.scaler, 'scaler.save')

    def predict(self, sequence):
        if isinstance(sequence, str):
            sequence = json.loads(sequence)

        prices_data = sequence.get('prices', [])
        if len(prices_data) < self.sequence_length:
            raise ValueError(f"Sequence must contain at least {self.sequence_length} data points")

        df = pd.DataFrame(prices_data, columns=['timestamp', 'Close', 'Volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df.set_index('timestamp', inplace=True)

        df['rsi'] = ta.rsi(df['Close'], length=14)
        df['ema'] = ta.ema(df['Close'], length=20)
        df['macd'] = ta.macd(df['Close'])['MACD_12_26_9']

        df = df.iloc[-self.sequence_length:]

        df.fillna(method='ffill', inplace=True)
        df.fillna(method='bfill', inplace=True)

        features = ['Close', 'Volume', 'rsi', 'ema', 'macd']
        sequence_data = df[features].values

        sequence_scaled = self.scaler.transform(sequence_data)
        sequence_scaled = np.expand_dims(sequence_scaled, axis=0)

        prediction = self.model.predict(sequence_scaled)
        return np.argmax(prediction, axis=1)[0]