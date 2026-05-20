import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import json

print(f"🟢 Rerun at: {datetime.now()}")

DATA_PATH = "./output_data.parquet"

@st.cache_data
def load_data(path):
    df = pd.read_parquet(path)
    return df

df = load_data(DATA_PATH)
filtered_df = df.copy()

# Define the file path
file_path = "./cat_data_counts.parquet"
# Validate that the file exists before reading
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Parquet file not found at: {file_path}")
# Load the Parquet file into a DataFrame
df_catMaster = pd.read_parquet(file_path)
# Display the first few rows
#print(df_catMaster.head())

st.set_page_config(page_title="SG Jobs Data Dashboard", layout="wide")

st.title("SG Jobs Data Dashboard")
st.caption("Data Source: SG Jobs Data (2023) | Updated: 2024-06-30")

#st.header("Dashboard Overview")
st.subheader("Business Objective : To propose the most efficient way to channel funds for training and career events")
st.subheader("Target Users : Skillsfuture Development Agencies / SWDA")
st.markdown("""
- Channel subsidies to target the correct industries to fill the talent gaps.
- Focus on the Job Categories with most vacancies. 
""")
st.subheader("Data Set")

#st.write(f"Rows loaded: {len(df):,} | Columns: {len(df.columns)}")
#st.dataframe(df.head(20), width="stretch")


#Wendy's version
#st.sidebar.header("Filters")
#unique_categories = sorted(df_catMaster["category"])
#selected_cats = st.sidebar.multiselect("Category", unique_categories, default=[])

#if selected_cats:
    #filtered_df = filtered_df[filtered_df["categories"].isin(selected_cats)]
    
    # 1. Join your list into a regex pattern: "cat1|cat2|cat3"
  #  pattern = '|'.join(selected_cats)
    # 2. Use str.contains with that pattern
   # filtered_df = filtered_df[filtered_df["categories"].str.contains(pattern, case=False, na=False)]

   #Martin's version
st.sidebar.header("Filters")

# JobStatus Sidebar
unique_jobStatus = sorted(df["status_jobStatus"].dropna().unique())
selected_jobStatus = st.sidebar.multiselect("Job Status", unique_jobStatus, default=["Open","Re-open"])

if selected_jobStatus:
    filtered_df = filtered_df[filtered_df["status_jobStatus"].isin(selected_jobStatus)]

#parsed_data = [item for sublist in filtered_df['categories'] for item in json.loads(sublist)]
#cat_data = pd.DataFrame(parsed_data)
top_5_cat_data = df_catMaster.head()

# Job Categories Sidebar

#parsed_data = [item for sublist in filtered_df['categories'] for item in json.loads(sublist)]
#cat_data = pd.DataFrame(parsed_data)
top_5_cat_data = df_catMaster.head()
unique_categories = sorted(df_catMaster["category"].dropna().unique())
selected_cats = st.sidebar.multiselect("Category", unique_categories, default=["Information Technology"])

if selected_cats:
    #filtered_df = filtered_df[filtered_df["categories"].isin(selected_cats)]
    
    # 1. Join your list into a regex pattern: "cat1|cat2|cat3"
    pattern = '|'.join(selected_cats)
    # 2. Use str.contains with that pattern
    filtered_df = filtered_df[filtered_df["categories"].str.contains(pattern, case=False, na=False)]

# Position Category Sidebar
unique_positionCat = sorted(df["position_category"].dropna().unique())
selected_positionCat = st.sidebar.multiselect("Position Category", unique_positionCat, default=[])

if selected_positionCat:
    filtered_df = filtered_df[filtered_df["position_category"].isin(selected_positionCat)]


#st.header("Filtered Results")
st.write(f"Matching rows: {len(filtered_df):,} | Columns: {len(filtered_df.columns)}")
st.dataframe(filtered_df.head(20), width="stretch")

#df_job1.pivot_table(index=["position_category"], values=["numberOfVacancies"],aggfunc=sum)
# Create the pivot in Pandas first
pivot_df = filtered_df.pivot_table(
    index="position_category", 
    values="numberOfVacancies", 
    aggfunc="sum"
)

#pivot_df = df.pivot_table(
#    index="position_category", 
#    values="numberOfVacancies", 
#    aggfunc="sum"
#)

# Display it beautifully
st.write("### Top Job Categories for Open Positions")
st.dataframe(top_5_cat_data, use_container_width=True)

# Display it beautifully
st.write(f"### Job Vacancies by Position Category for {selected_cats}")
st.dataframe(pivot_df, use_container_width=True)

#df_job1.pivot_table(index=["position_category", "positionLevels"], values=["numberOfVacancies"],aggfunc=sum)
# Create the pivot in Pandas first
pivot_df1 = filtered_df.pivot_table(
    index=["position_category", "positionLevels"],
    values="numberOfVacancies", 
    aggfunc="sum"
)

# Display it beautifully
st.write("### Job Vacancies by Position Category, Position Level")
st.dataframe(pivot_df1, use_container_width=True)

