import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import mean_squared_error


class NeuralModule(nn.Module):
    def __init__(self, activation_layer=nn.LeakyReLU):
        super(NeuralModule, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(24, 18),
            activation_layer(),
            nn.Linear(18, 6),
            nn.Linear(6, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.model(x)
        return torch.flatten(x)


class FilmPuddingModel:
    def __init__(self):
        self.model = NeuralModule().float()

        self.patience = 100
        self.batch_size = 32
        self.learning_rate = 0.001
        self.optimiser = optim.Adam(self.model.parameters(),
                                    lr=self.learning_rate)
        self.loss_func = nn.MSELoss()

    def _construct_data_loader(self, x, y, shuffle):
        d_x = torch.as_tensor(x, dtype=torch.float)
        d_y = torch.as_tensor(y, dtype=torch.float)
        data_pairs = list(zip(d_x, d_y))
        return torch.utils.data.DataLoader(data_pairs,
                                           batch_size=self.batch_size,
                                           shuffle=shuffle)

    def fit(self, train_x, train_y, val_x, val_y, print_mode=False):
        train_loader = self._construct_data_loader(train_x, train_y,
                                                   shuffle=True)
        val_loader = self._construct_data_loader(val_x, val_y, shuffle=False)

        epoch = 0
        epochs_without_improvement = 0

        best_mse = 0
        best_state_dict = self.model.state_dict()

        while epochs_without_improvement < self.patience:
            total_loss = 0
            for i, data in enumerate(train_loader, 0):
                self.optimiser.zero_grad()

                x, y = data
                output = self.model(x)
                loss = self.loss_func(output, y)
                loss.backward()
                self.optimiser.step()
                total_loss += loss.item()

            if print_mode:
                print(F"Loss after batch iteration {epoch + 1}: {total_loss}")

            val_scores = torch.empty(0)
            with torch.no_grad():
                for val_data in val_loader:
                    val_inputs, _ = val_data
                    new_val_scores = self.model(val_inputs)
                    val_scores = torch.cat((val_scores, new_val_scores))

            val_mse = mean_squared_error(val_y, val_scores)
            if print_mode:
                print(F"AUC of ROC for validation set: {val_mse}")

            if val_mse > best_mse:
                best_state_dict = self.model.state_dict()
                epochs_without_improvement = 0
                best_mse = val_mse
                if print_mode:
                    print("NEW BEST MODEL\n")
            else:
                epochs_without_improvement += 1

            epoch += 1

        if print_mode:
            print(F"Final best validation MSE: {best_mse}")
        self.model.load_state_dict(best_state_dict)

        train_scores = torch.empty(0)
        train_shuffled_labels = torch.empty(0)
        with torch.no_grad():
            for train_data in train_loader:
                train_inputs, train_sub_label = train_data
                new_train_scores = self.model(train_inputs)

                train_scores = torch.cat((train_scores, new_train_scores))
                train_shuffled_labels = torch.cat(
                    (train_shuffled_labels, train_sub_label))
        train_mse = mean_squared_error(train_shuffled_labels, train_scores)
        if print_mode:
            print(F"Training MSE for best model: {train_mse}\n")

    def predict(self, x):
        return self.model(torch.as_tensor(x, dtype=torch.float)).data.numpy()

    def evaluate(self, x, y_real):
        prediction = self.predict(x)
        print(x)
        print(F"MSE: {mean_squared_error(y_real, prediction)}")
