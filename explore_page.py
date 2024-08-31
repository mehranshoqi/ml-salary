import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


@st.cache
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
    df = df[df["ConvertedComp"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedComp"] <= 250000]
    df = df[df["ConvertedComp"] >= 10000]
    df = df[df["Country"] != "Other"]

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    df = df.rename({"ConvertedComp": "Salary"}, axis=1)
    return df

df = load_data()

def show_explore_page():
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6','#c4e17f','#76d7c4','#ff6f61','#6b5b95']
    st.title("Explore Salaries")
    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=False, startangle=0, colors=colors)
    ax1.axis("equal")  

    st.write("""#### Number of Data from different countries""")

    st.pyplot(fig1)
    
    st.write(
        """
    #### Mean Salary Based On Country
    """
    )
    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)

    # Create an Altair bar chart with pink color
    chart = alt.Chart(data.reset_index()).mark_bar(color='#ff9999').encode(
        x=alt.X('Salary:Q', title='Mean Salary'),
        y=alt.Y('Country:N', sort='-x', title='Country')
    ).properties(
        width=600,
        height=400
    )

    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)


    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().reset_index()

    # Create an Altair chart
    chart = alt.Chart(data).mark_line(color='#ff9999').encode(
        x='YearsCodePro',
        y='Salary'
    ).properties(
        width=600,
        height=400
    )

    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)


