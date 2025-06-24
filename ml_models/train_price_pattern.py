import os
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from price_pattern_model import PriceRegimeTransformer
from torch.utils.data import DataLoader, TensorDataset

# --- Rule-based label generation (mock ground truth) ---
def label_window(window):
    pct_change = (window[-1, 3] - window[0, 0]) / window[0, 0]  # close - open
    if pct_change > 0.02:
        return 0  # trending_up
    elif pct_change < -0.02:
        return 1  # trending_down
    elif np.std(window[:, 3]) < 0.5:
        return 2  # mean_reverting
    else:
        return 3  # volatile


# --- Load and prepare data ---
def load_data(preprocessed_dir):
    X, y = [], []
    for fname in os.listdir(preprocessed_dir):
        if not fname.endswith("_X.npy"):
            continue
        windows = np.load(os.path.join(preprocessed_dir, fname))
        for window in windows:
            label = label_window(window)
            X.append(window)
            y.append(label)
    return np.array(X), np.array(y)


# --- Training ---
def train():
    # Load dataset
    data_dir = os.path.join(os.path.dirname(__file__), "../data_pipeline/cache/preprocessed")
    X, y = load_data(data_dir)

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=42)

    # Convert to torch tensors
    X_train = torch.tensor(X_train, dtype=torch.float32)
    y_train = torch.tensor(y_train, dtype=torch.long)
    X_val = torch.tensor(X_val, dtype=torch.float32)
    y_val = torch.tensor(y_val, dtype=torch.long)

    # Wrap in Datasets
    train_dataset = TensorDataset(X_train, y_train)
    val_dataset = TensorDataset(X_val, y_val)

    # DataLoaders (BATCHED)
    batch_size = 16
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size)

    # Model
    model = PriceRegimeTransformer(input_dim=5, num_classes=4)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)
    num_epochs = 10

    # Training loop
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            output = model(batch_X)
            loss = criterion(output, batch_y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        # Validation
        model.eval()
        val_loss = 0
        correct = 0
        total = 0
        with torch.no_grad():
            for batch_X, batch_y in val_loader:
                output = model(batch_X)
                val_loss += criterion(output, batch_y).item()
                correct += (output.argmax(dim=1) == batch_y).sum().item()
                total += batch_y.size(0)

        val_acc = correct / total
        print(f"Epoch {epoch+1}/{num_epochs} | Train Loss: {total_loss:.4f} | Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.4f}")

    # Save model
    torch.save(model.state_dict(), os.path.join(os.path.dirname(__file__), "price_pattern_model.pt"))
    print("Model saved.")



if __name__ == "__main__":
    train()
