
import streamlit as st


def bar_of_nulls(data):
    st.write('Missing Values')
    st.bar_chart(data.isnull().sum().to_frame().rename(
        columns={0: 'Missing values'}))


def data_types(data):
    st.write('Data Types')
    st.write(data.dtypes.to_frame().rename(
        columns={0: 'Types'}))


def describe(data):
    st.write('Describe')
    st.write(data.describe())


def main(data):

    st.subheader('Exploratory Data Analysis')

    funcs = {
        'Missing values': bar_of_nulls,
        'Data Types': data_types,
        'Describe': describe
    }

    describe_options = st.multiselect('Describe', list(
        funcs.keys()), key='describing_data')

    for desc in describe_options:
        funcs.get(desc)(data)

    st.write(data)
