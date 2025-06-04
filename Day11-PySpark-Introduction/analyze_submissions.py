from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count, col

# 1. Create a SparkSession
# .appName() sets a name for your application (visible in Spark UI if running on a cluster)
# .master("local[*]") tells Spark to run locally using all available cores on your machine
spark = SparkSession.builder \
    .appName("AssessmentAnalysis") \
    .master("local[*]") \
    .getOrCreate()

print("SparkSession created successfully.")

# 2. Load the Submission Data from CSV
# .option("header", "true") treats the first row as column headers
# .option("inferSchema", "true") tries to automatically infer data types (can be slow for large files)
try:
    submissions_df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv("dummy_submissions.csv")
except Exception as e:
    print(f"Error loading CSV: {e}")
    spark.stop()
    exit()

print("Submissions DataFrame loaded:")
submissions_df.show(5) # Show first 5 rows
submissions_df.printSchema()

# 3. Perform Basic Analysis
print("\n--- Basic Analysis ---")

# a. Calculate the average score for each question_id
print("\nAverage score per question:")
avg_score_per_question = submissions_df.groupBy("question_id") \
    .agg(avg("score").alias("average_score")) \
    .orderBy("question_id")
avg_score_per_question.show()

# b. Count how many students attempted each question_id
print("\nNumber of attempts per question:")
attempts_per_question = submissions_df.groupBy("question_id") \
    .agg(count("student_id").alias("num_attempts")) \
    .orderBy("question_id")
attempts_per_question.show()

# c. Find the average score for each student_id
print("\nAverage score per student:")
avg_score_per_student = submissions_df.groupBy("student_id") \
    .agg(avg("score").alias("average_student_score")) \
    .orderBy(col("average_student_score").desc()) # Order by score descending
avg_score_per_student.show()

# d. Filter for submissions with a score greater than 90
print("\nSubmissions with score > 90:")
high_scores_df = submissions_df.filter(col("score") > 90)
high_scores_df.show()

# 4. Stop the SparkSession
# It's good practice to stop the SparkSession when you're done,
# especially in scripts, to release resources.
print("\nStopping SparkSession...")
spark.stop()
print("SparkSession stopped.")