import streamlit as st
import pandas as pd

# Load and prepare the data
data_path = "Store_Window_Sizes_Updated.xlsx"
raw_df = pd.read_excel(data_path, skiprows=3)
raw_df.columns = [
    "Store Number", "Store Name",
    "Primary_Large", "Primary_Medium", "Primary_Small",
    "Secondary_Large", "Secondary_Medium", "Secondary_Small"
]
df = raw_df.copy()
df["Store Number"] = df["Store Number"].astype(str).str.strip()
df["Store Name"] = df["Store Name"].astype(str).str.strip()

st.title("Store Window Size Lookup")

user_input = st.text_input("Enter store numbers or names (comma-separated):")

if user_input:
    entries = [entry.strip().lower() for entry in user_input.split(",")]

    def describe_windows(row):
        summary = []
        if row["Primary_Large"] == "X":
            summary.append("large primary")
        if row["Primary_Medium"] == "X":
            summary.append("medium primary")
        if row["Primary_Small"] == "X":
            summary.append("small primary")
        if row["Secondary_Large"] == "X":
            summary.append("large secondary")
        if row["Secondary_Medium"] == "X":
            summary.append("medium secondary")
        if row["Secondary_Small"] == "X":
            summary.append("small secondary")
        return ", ".join(summary).capitalize() if summary else "No windows listed"

    matched = df[df.apply(lambda row: str(row["Store Number"]).strip().lower() in entries or str(row["Store Name"]).strip().lower() in entries, axis=1)]

    if not matched.empty:
        for _, row in matched.iterrows():
            st.write(f"**{row['Store Name']}** — {describe_windows(row)}")
    else:
        st.warning("No matching stores found.")
