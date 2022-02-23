import streamlit as st
import pandas as pd


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(encoding="utf-8", index=False)


def get_stats_for(df):
    return pd.DataFrame(df.describe())

@st.cache
def read_as_df(path):
    df = pd.read_csv(path)
    return df


data_frame_holders = {
    "Chronos": read_as_df("static/data/chronos.csv"),
    "Cn": read_as_df("static/data/cn.csv"),
    "Expression": read_as_df("static/data/expression.csv"),
}
csv_data_holders = {
    "Chronos": convert_df(data_frame_holders["Chronos"]),
    "Cn": convert_df(data_frame_holders["Cn"]),
    "Expression": convert_df(data_frame_holders["Expression"]),
}


def data_set():
    dataset = st.container()
    
    with dataset:
        col1, col2 = st.columns(2)
        with col1:
            option = st.selectbox("Please select the dataset", data_frame_holders.keys())

            df = data_frame_holders[option]
            #Filters are based on all columns
            #Filters are shown in sidebar
            chosen_columns = st.sidebar.multiselect("Choose Columns: ", df.columns)
            if len(chosen_columns) == 0:
                chosen_columns = df.columns

        #Meta about selected filters
        st.sidebar.write(len(chosen_columns), " columns are selected from total " , len(df.columns))

        #Filters based on all columns using their min and max values respectively
        chosen_column_values = {}
        for c in chosen_columns:
            try:
                chosen_value = st.sidebar.slider(
                    c,
                    float(df[c].min()),
                    max_value=float(df[c].max()),
                    step=0.1,
                    value=float(df[c].max()),
                )
                chosen_column_values[c] = float(chosen_value)
            except ValueError as e:
                print("Error1", e)
        with col2:
            #Download button to download as csv
            st.write('Download option')
            st.download_button(
                label="Download data as CSV",
                data=csv_data_holders[option],
                file_name=option + ".csv",
                mime="text/csv",
            )
        #Apply selected filters and display top 20 values from it
        df = data_frame_holders[option]
        df = df[chosen_columns]
        for c in chosen_column_values:
            try:
                df = df[df[c].astype(float) <= chosen_column_values[c]]
            except ValueError as e:
                print("Error2", e)
        st.dataframe(df.head(30))

        #Display insights of dataset selected based on filters
        st.write('Meta data about selected data set')
        st.dataframe(get_stats_for(df))
