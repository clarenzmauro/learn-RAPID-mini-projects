import torch
import torch.nn as nn # Neural network module
import torch.nn.functional as F # Contains activation functions like relu, sigmoid

print(f"PyTorch Version: {torch.__version__}")

# --- Define a Simple Neural Network Model ---
class SimpleAssessmentModel(nn.Module):
    def __init__(self, input_features, hidden_units, output_classes):
        """
        Initializes the layers of the model.
        Args:
            input_features (int): Number of features in the input data.
            hidden_units (int): Number of neurons in the hidden layer.
            output_classes (int): Number of output classes (e.g., 1 for binary classification logit).
        """
        super().__init__() # Call the parent nn.Module's constructor

        # Define the layers
        # Layer 1: Fully connected layer from input_features to hidden_units
        self.fc1 = nn.Linear(input_features, hidden_units)

        # Layer 2: Fully connected layer from hidden_units to output_classes
        self.fc2 = nn.Linear(hidden_units, output_classes)

        # (Optional) You could add more layers, dropout, batch normalization etc. here
        # For example, another hidden layer:
        # self.fc_hidden2 = nn.Linear(hidden_units, hidden_units // 2)
        # self.fc_output = nn.Linear(hidden_units // 2, output_classes)

        print("SimpleAssessmentModel initialized with:")
        print(f"  Input features: {input_features}")
        print(f"  Hidden units: {hidden_units}")
        print(f"  Output classes: {output_classes}")
        print(f"  Layer 1 (fc1): {self.fc1}")
        print(f"  Layer 2 (fc2): {self.fc2}")


    def forward(self, x):
        """
        Defines the forward pass of the model.
        How data flows through the layers.
        Args:
            x (torch.Tensor): The input tensor.
        Returns:
            torch.Tensor: The output tensor (logits).
        """
        # Pass input through the first fully connected layer
        x = self.fc1(x)
        # Apply an activation function (e.g., ReLU - Rectified Linear Unit)
        x = F.relu(x)

        # (If you had more layers, they would go here)
        # x = self.fc_hidden2(x)
        # x = F.relu(x)
        # x = self.fc_output(x)

        # Pass through the second (output) fully connected layer
        x = self.fc2(x)

        # For binary classification, we typically output logits.
        # A sigmoid activation would be applied *after* this output,
        # often combined with the loss function (like BCEWithLogitsLoss) for numerical stability.
        # If this were multi-class classification with N classes, fc2 would output N logits,
        # and a softmax would typically be applied.
        return x

# --- Instantiate and Test the Model (Conceptual) ---
print("\n--- Instantiate and Test Model ---")

# Define model parameters based on our hypothetical assessment task
INPUT_FEATURES = 10  # e.g., 10 numerical features extracted from an answer
HIDDEN_UNITS = 32    # Number of neurons in the hidden layer (can be tuned)
OUTPUT_CLASSES = 1   # For binary classification (Correct/Incorrect), we output 1 logit
                     # If it were 3 difficulty levels, this would be 3.

# Create an instance of our model
model = SimpleAssessmentModel(input_features=INPUT_FEATURES,
                              hidden_units=HIDDEN_UNITS,
                              output_classes=OUTPUT_CLASSES)

# Print the model structure
print("\nModel Structure:")
print(model)

# Create some dummy input data (batch of 2 samples, each with INPUT_FEATURES)
# This simulates what you might feed into the model.
# Batch size is the first dimension.
dummy_batch_size = 4
dummy_input_data = torch.randn(dummy_batch_size, INPUT_FEATURES) # Random data for testing
print(f"\nShape of dummy input data: {dummy_input_data.shape}") # Should be [batch_size, input_features]

# Pass the dummy data through the model's forward pass
# (No training involved, just seeing the data flow)
with torch.no_grad(): # Disable gradient calculation for inference/testing
    output_logits = model(dummy_input_data)

print(f"\nShape of output logits: {output_logits.shape}") # Should be [batch_size, output_classes]
print("Output logits (raw scores from the model):\n", output_logits)

# If this were for binary classification, you might apply sigmoid to get probabilities
# output_probabilities = torch.sigmoid(output_logits)
# print("\nOutput probabilities (after sigmoid):\n", output_probabilities)

print("\n--- Script Finished ---")