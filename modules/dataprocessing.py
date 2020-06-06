
import streamlit as st


def drop_columns(data):
    to_keep = st.multiselect(
        'Columns to keep', data.columns.tolist(), key='data_to_keep')
    return data[to_keep]


def main(data):

    st.subheader('Pre-Processing')

    options_list = [
        'Drop Columns'
    ]
    options = st.multiselect('Options', options_list)

    if options_list[0] in options:
        data = drop_columns(data)

    st.write(data)

    return data
