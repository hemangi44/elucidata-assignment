import streamlit as st
import pandas as pd
from data_set_runner import data_frame_holders,  read_as_df 
import plotly.graph_objects as go
import plotly.express as px

metadata_df = read_as_df("static/data/metadata.csv")


def data_plot():
    dataset = st.container()
    with dataset:
        #Title for plot 
        st.title("Plot all data points")
        col1, col2, col3 = st.columns(3)
        with col1:
            left_dataset_selected = st.selectbox("Please select the left dataset", data_frame_holders.keys())
            left_dataset_selected_df = data_frame_holders[left_dataset_selected]

            #Removing Sample_ID column from display list as it is not gene and it fails in df merge below due to duplicate key
            columns = set(left_dataset_selected_df.columns)
            columns.remove('Sample_ID')
            left_gene_selected = st.selectbox("Please select the left Gene", columns)

        with col2:
            right_dataset_selected = st.selectbox("Please select the right dataset", data_frame_holders.keys())
            right_dataset_selected_df = data_frame_holders[right_dataset_selected]

            right_gene_selected = st.selectbox("Please select the right Gene", columns)

        
        with col3:
            columns = set(metadata_df.columns)
            columns.remove('Sample_ID')
            metadata_selected = st.selectbox("Please select the Metadata Column", columns)
        
        #Display user choice 
        st.write('Showing Scatter plot of ',left_dataset_selected , left_gene_selected ,' with ', right_dataset_selected , right_gene_selected)

        #Data population based on user choice
        df_merged = pd.merge(left_dataset_selected_df[['Sample_ID' ,left_gene_selected ]] , right_dataset_selected_df[['Sample_ID' , right_gene_selected]], on = "Sample_ID" , how = 'inner')

        df_merged = pd.merge(df_merged , metadata_df[['Sample_ID' , metadata_selected]] , on = "Sample_ID" , how = 'inner')

        #Dropping Nan values
        df_merged.dropna(inplace=True)

        # Create scatter plot figure
        fig = px.scatter(df_merged , x = df_merged.columns[1] , y = df_merged.columns[2], color = metadata_selected)
        st.plotly_chart(fig, use_container_width=True)

        st.write('Showing violin plot of ',left_dataset_selected , left_gene_selected ,' with ', metadata_selected)

        #Data population for violoin chart
        df_merged_with_meta = pd.merge(left_dataset_selected_df[['Sample_ID' ,left_gene_selected ]] ,  metadata_df[['Sample_ID' , metadata_selected]], on = "Sample_ID" , how = 'inner')

        #Dropping Nan values
        df_merged_with_meta.dropna(inplace=True)

        #Create violin plot figure
        fig = px.violin(df_merged_with_meta,x = df_merged_with_meta.columns[1], y=df_merged_with_meta.columns[2], box=True, points='all', color = metadata_selected ,  hover_data=df_merged_with_meta.columns)
        st.plotly_chart(fig, use_container_width=True)
