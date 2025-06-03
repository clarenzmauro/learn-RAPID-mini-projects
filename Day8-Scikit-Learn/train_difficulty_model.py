import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 1. load data
print("Loading data...")
try:
    df = pd.read_csv('question_difficulty_dataset.csv')
except FileNotFoundError:
    print("Error: question_difficulty_dataset.csv not found")
    exit()

print(f"Dataset loaded. Shape: {df.shape}")
print(df.head())

# ensure columns are correct
if 'question_text' not in df.columns or 'difficulty_level' not in df.columns:
    print("Error: CSV must contain 'question_text' and 'difficulty_level' columns")
    exit()

# handle potential NaN values in text 
df['question_text'] = df['question_text'].fillna('')

# prepare data
X = df['question_text'] # features
y = df['difficulty_level'] # target

# split data into training and testing sets
# test_size = 0.2 means 20% of the data will be used for testing, and 80% will be used for training
# random_state ensures reproducibility of the split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y # stratify for balanced classes in splits
)
print(f"Training set size: {len(X_train)}, Test set size: {len(X_test)}")

# 3. define the model pipeline
# pipeline chains multiple steps: vectorizer and classifier
print("Defining model pipeline...")
model_pipeline = Pipeline([
    ('vectorizer', CountVectorizer(stop_words='english', ngram_range=(1,2))), # ngram_range=(1,2) means unigrams and bigrams
    ('classifier', MultinomialNB())
])
# CountVectorizer parameters:
#   stop_words='english': removes common english words like "the", "a", "is"
#   ngram_range=(1,2): considers single words (unigrams) and pairs of words (bigrams) as features

# 4. train the model
print("Training the model...")
model_pipeline.fit(X_train, y_train)
print("Model training complete.")

# 5. evaluate the model
print("\nEvaluating the model...")
y_pred_test = model_pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred_test)
print(f"Accuracy on Test Set: {accuracy:.4f}")

print("\nClassification Report on Test Set:")
print(classification_report(y_test, y_pred_test, zero_division=0))
# zero_division=0 handles cases where a class might not have predictions in small datasets

# 6. save the model
model_filename = 'difficulty_prediction_pipeline.joblib'
print(f"\nSaving the trained model pipeline to {model_filename}...")
joblib.dump(model_pipeline, model_filename)
print(f"Model pipeline saved successfully as {model_filename}.")

print("\n--- Script Finished ---")