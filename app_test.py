import pandas as pd
import streamlit as st

# Load dataframes
emp_df = pd.read_excel(
    "employeDataProfile.xlsx", sheet_name="employee_comp", index_col="ID_EMP"
)
training_df = pd.read_excel(
    "employeDataProfile.xlsx", sheet_name="training_list", index_col="TRAIN_ID"
)


# Function to select training based on employee level
def select_training(level, comp_list):
    selected_df = training_df[training_df["LEVEL"] == level]
    return selected_df[selected_df["COMPETENCY"].str.contains("|".join(comp_list))]


# Title
st.title("Employee recommendation test")

# Employee selection
name = st.selectbox("Employee Name", emp_df["NAME"], index=None)
st.header("Employee Info")
employee_df = emp_df.loc[emp_df["NAME"] == name, ["LEVEL", "POSITION"]]
st.dataframe(employee_df, use_container_width=True)

# Training Recommendation
st.header("Training Recommendation")
emp_row = emp_df[emp_df["NAME"] == name]
if not emp_row.empty:
    bad_comp_value = emp_row["BAD_COMP"].iloc[0]
    if isinstance(bad_comp_value, str):
        comp_list = bad_comp_value.split(";")
    else:
        # Handle non-string values, e.g., floats
        comp_list = [
            "Default Value"
        ]  # Provide a default value or handle it based on your application logic
    lvl = emp_row["LEVEL"].iloc[0]
    recommended_training = select_training(lvl, comp_list)["COURSE_NAME"]
    if not recommended_training.empty:
        recommended_training = recommended_training.drop_duplicates()
        st.dataframe(
            recommended_training.reset_index(drop=True).rename(lambda x: f"{x+1}."),
            use_container_width=True,
        )
    else:
        st.write("No recommended training found.")
else:
    st.write("Employee not found.")
