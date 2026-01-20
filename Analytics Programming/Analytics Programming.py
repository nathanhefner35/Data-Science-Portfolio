import pandas as pd

file_path = r"C:\Users\Nathan\Downloads\D598 Data Set.xlsx"
data = pd.ExcelFile(file_path)

df = data.parse('1-150 V2')

duplicates = df[df.duplicated()]
print(f"Number of duplicate rows: {duplicates.shape[0]}")

statistics_df = df.groupby('Business State').agg(['mean', 'median', 'min', 'max']).reset_index()

statistics_df.columns = [
    '_'.join(col).strip() if isinstance(col, tuple) else col
    for col in statistics_df.columns
]
statistics_df.rename(columns={"Business State_": "Business State"}, inplace=True)

print("Statistics DataFrame:")
print(statistics_df)

negative_debt_to_equity = df[df['Debt to Equity'] < 0]
print("Businesses with Negative Debt-to-Equity Ratios:")
print(negative_debt_to_equity)

debt_to_income = pd.DataFrame({
    'Debt to Income Ratio': df['Total Long-term Debt'] / df['Total Revenue']
})

df_concatenated = pd.concat([df, debt_to_income], axis=1)

print("DataFrame with Debt-to-Income Ratio Concatenated:")
print(df_concatenated.head())