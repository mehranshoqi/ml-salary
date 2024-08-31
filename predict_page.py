import streamlit as st
import numpy as np
import pickle


def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():

    st.title("Predict")

    countries = (
        "United States",
        "India",
        "United Kingdom",
        "Germany",
        "Canada",
        "Brazil",
        "France",
        "Spain",
        "Australia",
        "Netherlands",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden",
    )

    education = (
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad",
    )
    col1, col2 = st.columns(2)

    with col1:
        country = st.selectbox("Country", countries)

    with col2:
        education = st.selectbox("Education", education)
    st.markdown("""
        <style>
        .stSlider > div > div > div > div {
            background: black;
        }
        </style>
        """, unsafe_allow_html=True)

    expericence = st.slider("Experience (in years)", 0, 50, 12)


    st.markdown("""
        <style>
        .stButton>button {
            background-color: blue;
            color: white;
            width: 300px;
        }
        .stButton>button:hover {
            background-color: white;
            color: red;
        }
        .stButton>button:active {
            background-color: white;
            color: red;
        }
        </style>
        """, unsafe_allow_html=True)

    ok = st.button("Calculate Salary")

    if ok:
        X = np.array([[country, education, expericence ]])
        X[:, 0] = le_country.transform(X[:,0])
        X[:, 1] = le_education.transform(X[:,1])
        X = X.astype(float)

        salary = regressor.predict(X)
        st.success(f"The estimated salary is ${salary[0]:.2f}")
