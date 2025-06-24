import torch
import torch.nn as nn

class PriceRegimeTransformer(nn.Module):
    def __init__(self, input_dim=5, emb_dim=128, num_heads=4, num_layers=3, num_classes=4, dropout=0.1):
        super(PriceRegimeTransformer, self).__init__()

        self.embedding = nn.Linear(input_dim, emb_dim)
        self.positional_encoding = PositionalEncoding(emb_dim)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=emb_dim,
            nhead=num_heads,
            dim_feedforward=emb_dim * 4,
            dropout=dropout,
            batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)

        self.classifier = nn.Sequential(
            nn.Linear(emb_dim, emb_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(emb_dim, num_classes)
        )

    def forward(self, x):
        # x: (batch_size, seq_len, input_dim)
        x = self.embedding(x)
        x = self.positional_encoding(x)
        x = self.transformer_encoder(x)

        # Use representation from the final timestep
        out = x[:, -1, :]  # (batch_size, emb_dim)
        logits = self.classifier(out)  # (batch_size, num_classes)
        return logits


class PositionalEncoding(nn.Module):
    def __init__(self, emb_dim, max_len=5000):
        super(PositionalEncoding, self).__init__()
        pe = torch.zeros(max_len, emb_dim)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        div_term = torch.exp(torch.arange(0, emb_dim, 2).float() * (-torch.log(torch.tensor(10000.0)) / emb_dim))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)  # (1, max_len, emb_dim)
        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[:, :x.size(1)]
        return x
