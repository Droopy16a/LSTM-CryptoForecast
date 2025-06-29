from dist.model import TensorModel
import argparse

def Train():
    parser = argparse.ArgumentParser(description="Train the model")
    parser.add_argument('--csv_path', type=str, default="./coin_Bitcoin.csv", help='Path of the CSV training file')
    parser.add_argument('--epochs', type=int, help='Number of epochs for training')
    parser.add_argument('--new', type=bool, help='Create a new model', default=False)

    args = parser.parse_args()

    csv_path = args.csv_path
    epochs = args.epochs
    new = args.new

    if new:
        tm = TensorModel(csv_path=csv_path)
        tm.train(epochs=epochs)
    else:
        tm = TensorModel()
        tm.csv_path = csv_path
        tm._load_and_prepare_data()
        tm.train(epochs=epochs)

if __name__ == "__main__":
    Train()