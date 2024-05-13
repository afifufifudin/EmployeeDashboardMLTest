import pandas as pd
import numpy as np
import sys
import streamlit as st

# load dataframe
emp_df = pd.read_excel(
    "employeDataProfile.xlsx", sheet_name="employee_comp", index_col="ID_EMP"
)
training_df = pd.read_excel(
    "employeDataProfile.xlsx", sheet_name="training_list", index_col="TRAIN_ID"
)


def select_level(dataframe, level):
    selected_df = training_df[training_df["LEVEL"] == level]
    return selected_df


def are_similar(df1, df2):
    if df1.shape != df2.shape:
        return False

    if not df1.columns.equals(df2.columns):
        return False

    if not df1.equals(df2):
        return False

    return True


name_list = emp_df["NAME"].tolist()

st.title("Employee recommendation test")
# st.write("Hi...! :)")

name = st.selectbox("Employee Name", name_list, index=None)
st.header("Employee Info")

employee_df = emp_df.loc[emp_df["NAME"] == name]  # take row from dataframe
st.checkbox("Use container width", value=True, key="use_container_width")
st.dataframe(
    employee_df[["LEVEL", "POSITION"]],
    use_container_width=st.session_state.use_container_width,
)
# st.write(employee_df[["NAME", "LEVEL", "POSITION"]])

st.header("Training Recommendation")

if name not in emp_df["NAME"].values:
    print("not found")
    sys.exit()
else:
    emp = emp_df.loc[emp_df["NAME"] == name]  # take row from dataframe
    comp = str(emp["BAD_COMP"].iloc[0])
    target_list = comp.split(";")
    lvl = int(emp["LEVEL"].iloc[0])
    selected_df = select_level(training_df, lvl)
    list_exist = (
        selected_df["COMPETENCY"]
        .apply(lambda x: any(item in x for item in target_list))
        .any()
    )
    try:
        recommendation = []
        for item in target_list:
            try:
                training_id = selected_df.index[
                    selected_df["COMPETENCY"] == item
                ].tolist()[0]
                things = selected_df.loc[training_id, "COURSE_NAME"]
                recommendation.append(things)
            except IndexError as e:
                print("Error:", e)
                print("Index", item, "is out of range")
    except Exception as e:
        print("An error has occurred: ", e)
    num = 0
    for x in recommendation:
        num += 1
        text = "{}.) {}".format(num, x)
        st.write(text)
