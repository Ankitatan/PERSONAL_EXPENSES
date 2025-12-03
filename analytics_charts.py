# analytics_charts.py
import altair as alt
import pandas as pd

def bar_category(df: pd.DataFrame, title: str = "Spending by Category"):
    if df.empty:
        return alt.Chart(pd.DataFrame({"category":[],"total_spent":[]})).mark_bar()
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("category:N", sort='-y', title="Category"),
        y=alt.Y("total_spent:Q", title="Total Spent"),
        tooltip=["category","total_spent"]
    ).properties(title=title, height=420)
    return chart

def line_monthly(df: pd.DataFrame, title: str = "Monthly Spending"):
    if df.empty:
        return alt.Chart(pd.DataFrame({"month":[],"total_spent":[]})).mark_line()
    df = df.copy()
    df["month"] = df["month"].astype(int)
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X("month:O", title="Month"),
        y=alt.Y("total_spent:Q", title="Total Spent"),
        tooltip=["month","total_spent"]
    ).properties(title=title, height=360)
    return chart

def pie_payment_mode(df: pd.DataFrame, title: str = "Spending by Payment Mode"):
    if df.empty:
        return alt.Chart(pd.DataFrame({"payment_mode":[],"total_spent":[]})).mark_arc()
    df = df.copy()
    df["angle"] = df["total_spent"] / df["total_spent"].sum()
    chart = alt.Chart(df).mark_arc(innerRadius=50).encode(
        theta="angle:Q",
        color="payment_mode:N",
        tooltip=["payment_mode","total_spent"]
    ).properties(title=title, height=360)
    return chart

def table_top_transactions(df):
    # returns df as-is; Streamlit can render a dataframe or st.table
    return df

def weekday_bar(df, title="Spending by Weekday"):
    if df.empty:
        return alt.Chart(pd.DataFrame({"weekday":[],"total_spent":[]})).mark_bar()
    df = df.copy()
    # map weekday number to name (0=Sunday)
    names = {0:"Sun",1:"Mon",2:"Tue",3:"Wed",4:"Thu",5:"Fri",6:"Sat"}
    df["weekday_name"] = df["weekday"].astype(int).map(names)
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("weekday_name:N", sort=list(names.values()), title="Weekday"),
        y=alt.Y("total_spent:Q", title="Total Spent"),
        tooltip=["weekday_name","total_spent","txn_count"]
    ).properties(title=title, height=360)
    return chart
