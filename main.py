from modules import dataloading, dataprocessing, xgbwrapper, eda
import streamlit as st

options = {
    'Loading Data': dataloading,
    'EDA': eda,
    'Pre-Processing': dataprocessing,
    'Modeling': xgbwrapper
}
st.sidebar.title('Dsahboard')

sidebar_select = st.sidebar.multiselect(
    'Menu', options=list(options.keys()), key='menu_option')


if 'Loading Data' in sidebar_select:
    data = options.get('Loading Data').main()


if 'EDA' in sidebar_select:
    options.get('EDA').main(data)


if 'Pre-Processing' in sidebar_select:
    processed_data = options.get('Pre-Processing').main(data)

if 'Modeling' in sidebar_select:
    options.get('Modeling').main(processed_data)


st.sidebar.markdown("""
            `@cristianexer`
            """)
