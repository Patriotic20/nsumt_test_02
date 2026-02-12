import pandas as pd

# 1. Load the original CSV
df = pd.read_csv('data/quizzes.csv')

# 2. Define the mapping from CSV columns to your Database Model columns
# We exclude 'start_time' as it's not in your model/copy command
mapping = {
    'user_id': 'user_id',
    'group_id': 'group_id',
    'subject_id': 'subject_id',
    'quiz_name': 'title',            # Maps to title
    'question_number': 'question_number',
    'quiz_time': 'duration',          # Maps to duration
    'quiz_pin': 'pin',                # Maps to pin
    'is_activate': 'is_active',       # Maps to is_active
    'id': 'id',
    'created_at': 'created_at',
    'updated_at': 'updated_at'
}

# 3. Select only the necessary columns in the exact order of your \copy command
# This effectively removes 'start_time' and renames the others
fixed_df = df[list(mapping.keys())].rename(columns=mapping)

# 4. Save the corrected file
fixed_df.to_csv('data/quizzes_fixed.csv', index=False)

print("Successfully created 'quizzes_fixed.csv' with 11 columns.")