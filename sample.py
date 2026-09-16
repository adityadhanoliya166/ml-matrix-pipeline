import pandas as pd

# Create a sample messy dataset with missing values, typos, whitespace, and currency symbols
data = {
    " Customer Name ": ["  Alice ", "Bob", "Charlie ", "Alice ", "Eve"],
    " Age ": [25, None, 35, 25, 40],
    " Salary ": ["$50,000", "$60,000", None, "$50,000", "$120,000 "],
    " Joined Date ": ["2023-01-01", "2023-02-15", "2023-03-10", "2023-01-01", "2023-05-20"]
}

df = pd.DataFrame(data)

# Save to main folder
df.to_csv("messy_data.csv", index=False)
print("SUCCESS: Created 'messy_data.csv' in your project folder!")