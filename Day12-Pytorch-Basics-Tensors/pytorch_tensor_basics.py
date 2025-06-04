import torch
import numpy as np # For comparison and creating tensors from numpy arrays

print(f"PyTorch Version: {torch.__version__}")

# --- 1. Creating Tensors ---
print("\n--- 1. Creating Tensors ---")

# From Python list
data_list = [[1, 2, 3], [4, 5, 6]]
tensor_from_list = torch.tensor(data_list)
print("Tensor from list:\n", tensor_from_list)
print(f"Shape: {tensor_from_list.shape}, Dtype: {tensor_from_list.dtype}")

# From NumPy array
numpy_array = np.array([[7, 8], [9, 10], [11, 12]], dtype=np.float32)
tensor_from_numpy = torch.from_numpy(numpy_array) # Shares memory with numpy array if on CPU
print("\nTensor from NumPy array:\n", tensor_from_numpy)
print(f"Shape: {tensor_from_numpy.shape}, Dtype: {tensor_from_numpy.dtype}")

# Tensors with specific values
zeros_tensor = torch.zeros(2, 4) # 2 rows, 4 columns of zeros
ones_tensor = torch.ones(3, 2, dtype=torch.int16) # Specify dtype
rand_tensor = torch.rand(2, 3) # Uniform random numbers between 0 and 1
print("\nZeros tensor:\n", zeros_tensor)
print("Ones tensor (int16):\n", ones_tensor)
print("Random tensor:\n", rand_tensor)

# --- 2. Tensor Attributes ---
print("\n--- 2. Tensor Attributes ---")
print(f"rand_tensor shape: {rand_tensor.shape}")
print(f"rand_tensor size: {rand_tensor.size()}") # Alias for shape
print(f"rand_tensor dtype: {rand_tensor.dtype}")
print(f"rand_tensor device: {rand_tensor.device}") # Will be 'cpu' by default

# --- 3. Tensor Operations ---
print("\n--- 3. Tensor Operations ---")

# Example: Representing scores for 3 students on 5 questions
# Student 1: [80, 85, 70, 90, 75]
# Student 2: [90, 92, 88, 78, 85]
# Student 3: [70, 65, 80, 72, 81]
scores_data = [
    [80, 85, 70, 90, 75],
    [90, 92, 88, 78, 85],
    [70, 65, 80, 72, 81]
]
scores_tensor = torch.tensor(scores_data, dtype=torch.float32)
print("Student scores tensor:\n", scores_tensor)

# a. Arithmetic Operations
# Add a constant value (e.g., curve all scores by 5 points)
curved_scores = scores_tensor + 5
print("\nCurved scores (+5):\n", curved_scores)

# Multiply by a weighting factor (e.g., if questions had different weights)
weights = torch.tensor([1.0, 1.0, 1.2, 0.8, 1.0]) # Weight for each of the 5 questions
weighted_scores = scores_tensor * weights # Element-wise multiplication (broadcasting)
print("\nWeighted scores (element-wise with broadcasting):\n", weighted_scores)

# b. Indexing and Slicing
# Get scores for the first student (row 0)
student1_scores = scores_tensor[0, :] # or scores_tensor[0]
print("\nScores for Student 1:\n", student1_scores)

# Get scores for the third question for all students (column 2)
question3_scores_all_students = scores_tensor[:, 2]
print("\nScores for Question 3 (all students):\n", question3_scores_all_students)

# Get scores for Student 2, questions 2 to 4 (inclusive for start, exclusive for end)
student2_q2_to_q4 = scores_tensor[1, 1:4] # Q2 is index 1, Q3 is index 2, Q4 is index 3
print("\nScores for Student 2, Questions 2-4:\n", student2_q2_to_q4)

# c. Aggregations
# Average score per student (average across columns for each row)
avg_score_per_student = torch.mean(scores_tensor, dim=1) # dim=1 means average across columns
print("\nAverage score per student:\n", avg_score_per_student)

# Average score per question (average across rows for each column)
avg_score_per_question = torch.mean(scores_tensor, dim=0) # dim=0 means average across rows
print("\nAverage score per question:\n", avg_score_per_question)

# Max score for each question
max_score_per_question = torch.max(scores_tensor, dim=0) # Returns (values, indices)
print("\nMax score per question (values, indices):\n", max_score_per_question)
print("Max values:", max_score_per_question.values)


# d. Reshaping
# View the scores_tensor as a flat 1D vector
flat_scores = scores_tensor.view(-1) # -1 infers the dimension
print(f"\nFlat scores (1D vector, shape {flat_scores.shape}):\n", flat_scores)

# Reshape to 5 rows, 3 columns (if compatible)
reshaped_scores = scores_tensor.reshape(5, 3)
print(f"\nReshaped scores (5x3, shape {reshaped_scores.shape}):\n", reshaped_scores)


# --- 4. Autograd (Brief Example) ---
print("\n--- 4. Autograd ---")
# Create tensors that require gradient tracking
a = torch.tensor([2.0, 3.0], requires_grad=True)
b = torch.tensor([5.0, 1.0], requires_grad=True)
c = a * b  # c = [10.0, 3.0]
d = c.mean() # d = (10 + 3) / 2 = 6.5

print(f"a: {a}, b: {b}, c: {c}, d: {d}")

# Compute gradients
d.backward() # Computes gradients of d with respect to a and b

print(f"Gradient of d w.r.t. a (d(d)/da): {a.grad}") # Should be [2.5, 0.5] (b/2)
print(f"Gradient of d w.r.t. b (d(d)/db): {b.grad}") # Should be [1.0, 1.5] (a/2)

# Gradients are accumulated, so zero them out if doing multiple backward passes in a loop
# a.grad.zero_()
# b.grad.zero_()

print("\n--- Script Finished ---")