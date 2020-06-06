
import streamlit as st
import pandas as pd
from sklearn.datasets import load_iris, load_diabetes, load_digits, load_wine, load_breast_cancer
import sqlalchemy as sql


def process_loader(loader):
    try:
        st.write(loader.get('DESCR'))
        df = pd.DataFrame(data=loader.get('data'),
                          columns=loader.get('feature_names'))
        df['target'] = loader.get('target')

        return df
    except Exception as e:
        st.write('Exception')
        st.write(e)
        st.write('Loader')
        st.write(loader)


def main():
    data = None

    st.subheader('Data Loading')
    loading_type = st.selectbox(
        'Loading Type', ['API', 'FILE', 'SQL', 'DATASETS'])

    if loading_type == 'FILE':
        file_type = st.selectbox('File Type', ['CSV', 'EXCEL', 'JSON'])
        file_path = st.file_uploader(label='File')
        if file_path != None:
            if file_type == 'CSV':
                csv_decoding = st.checkbox('Encoding')
                if csv_decoding:
                    enc = st.selectbox('Encoding Method', ['UTF-8', 'LATIN-1'])
                    data = pd.read_csv(file_path, encoding=enc)

                else:
                    data = pd.read_csv(file_path)

            if file_type == 'EXCEL':
                data = pd.read_excel(file_path)

            if file_type == 'JSON':
                json_box = st.checkbox('Normalize')
                json_orient = st.selectbox('Orient', ['records'])
                if json_box:
                    data = pd.read_json(file_path)

    if loading_type == 'API':
        url = st.text_input('Endpoint URL')
        if url != '' and 'http://' in url:
            data = pd.read_json(url)
        elif url != '' and 'https://' in url:
            data = pd.read_json(url)
        else:
            st.write('No URL detected')

    if loading_type == 'SQL':
        db_conn = {
            'engine': '',
            'username': '',
            'password': '',
            'host': '',
            'port': '',
            'database': ''
        }
        for k, v in db_conn.items():
            db_conn[k] = st.text_input(
                k.capitalize(), type='password' if k == 'password' else 'default')
        if True == all([x != '' for x in db_conn.values()]):
            con = sql.create_engine(
                '{engine}://{username}:{password}@{host}:{port}/{database}'.format(**db_conn), echo=False)
            query = st.text_area('Query')
            if 'SELECT' in query or 'select' in query:
                data = pd.read_sql(query, con=con)

    if loading_type == 'DATASETS':
        ds = st.selectbox(
            'Datasets', ['Iris', 'Diabets', 'Digits', 'Wine', 'Breast Cancer'])

        if ds == 'Iris':
            data = process_loader(load_iris())

        if ds == 'Diabets':
            data = process_loader(load_diabetes())

        if ds == 'Digits':
            data = process_loader(load_digits())

        # if ds == 'Linnerud':
        #     data = process_loader(load_linnerud())

        if ds == 'Wine':
            data = process_loader(load_wine())

        if ds == 'Breast Cancer':
            data = process_loader(load_breast_cancer())


###############################################################################################################################
    st.write(data)
    return data
