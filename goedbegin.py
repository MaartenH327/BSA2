import pandas as pd

# Sample dataset
data = {
    "student_id": [1, 1, 2, 2, 3, 4, 4],
    "program": ["CS", "Math", "CS", "Physics", "CS", "Math", "Physics"],
    "enrollment_date": ["2024-01-10", "2024-01-15", "2024-02-01", "2024-02-10", "2024-03-05", "2024-04-01", "2024-04-10"],
    "withdrawal_date": [None, "2024-02-20", None, "2024-02-15", None, "2024-04-20", None]
}

df = pd.DataFrame(data)

# Pivot enrollment and withdrawal separately
enrollment_pivot = df.pivot_table(index="student_id", columns="program", values="enrollment_date", aggfunc="first")
withdrawal_pivot = df.pivot_table(index="student_id", columns="program", values="withdrawal_date", aggfunc="first")

# Create an enrollment status pivot (1 = currently enrolled, 0 = withdrawn)
def is_currently_enrolled(enrollment, withdrawal):
    return 1 if pd.notna(enrollment) and pd.isna(withdrawal) else 0

status_pivot = enrollment_pivot.combine(withdrawal_pivot, is_currently_enrolled)
status_pivot = status_pivot.add_prefix("Currently_Enrolled_")

# Rename columns for clarity
enrollment_pivot = enrollment_pivot.add_prefix("Enrolled_")
withdrawal_pivot = withdrawal_pivot.add_prefix("Withdrawn_")

# Merge all pivot tables
df_wide = enrollment_pivot.merge(withdrawal_pivot, left_index=True, right_index=True, how="left")
df_wide = df_wide.merge(status_pivot, left_index=True, right_index=True, how="left")

# Reset index for better readability
df_wide = df_wide.reset_index()

print(df_wide)
