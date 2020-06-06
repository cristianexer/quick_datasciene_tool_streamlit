
import streamlit as st
from sklearn.model_selection import train_test_split
import xgboost as xgb
import pandas as pd
from sklearn import metrics
from matplotlib import pyplot as plt


def main(data):

    st.subheader('XGBoost')
    features = st.multiselect(
        'Features', data.columns.tolist(), default=data.columns.tolist())
    target = st.selectbox('Target', data.columns.tolist())

    st.write('Train Test Split')
    test_size = st.slider('Test split size', min_value=0.00,
                          max_value=1.00, step=0.01, value=0.33)
    random_state = st.number_input('Random state', value=42)
    X_train, X_test, y_train, y_test = train_test_split(
        data[features], data[target], test_size=test_size, random_state=random_state)

    xgb_type = st.selectbox('XGB Class', ['XGBClassifier', 'XGBRegressor'])

    hyperparams_check = st.checkbox('Hyper Tunning')

    params = dict(
        base_score=None,
        booster=None,
        colsample_bylevel=None,
        colsample_bynode=None,
        colsample_bytree=None,
        gamma=None,
        gpu_id=None,
        importance_type='gain',
        interaction_constraints=None,
        learning_rate=None,
        ax_delta_step=None,
        max_depth=None,
        min_child_weight=None,
        missing=None,
        monotone_constraints=None,
        n_estimators=100,
        n_jobs=None,
        num_parallel_tree=None,
        objective='binary:logistic',
        random_state=None,
        reg_alpha=None,
        reg_lambda=None,
        scale_pos_weight=None,
        subsample=None,
        tree_method=None,
        validate_parameters=None,
        verbosity=None
    )

    if hyperparams_check:
        hyper_options = st.multiselect('Hyperparameters', list(params.keys()))
        for hyper_option in hyper_options:
            params[hyper_option] = st.text_input(
                hyper_option, value=params.get(hyper_option))

    if xgb_type == 'XGBClassifier':
        mod = xgb.XGBClassifier(**params)

    if xgb_type == 'XGBRegressor':
        mod = xgb.XGBRegressor(**params)

    metric = st.multiselect('Metrics', ['Classification Report', 'MAE'])

    train_button = st.button('Train')
    if train_button:
        mod.fit(X_train, y_train)

        preds = pd.DataFrame({
            'y_true': y_test,
            'y_pred': mod.predict(X_test)
        })
        st.write('True vs Predicted')
        st.write(preds)

        if 'Classification Report' in metric:
            st.write('Classification Report')
            clsf = metrics.classification_report(
                preds.y_true, preds.y_pred, output_dict=True)
            st.write(pd.DataFrame(clsf).T)

        if 'MAE' in metric:
            st.write(
                f'MAE: {metrics.mean_absolute_error(preds.y_true, preds.y_pred)}')

            # store the winning model in a new variable

        st.write('Fature Importance')
        xgc = mod
        # saving the feature names to the model
        xgc.get_booster().feature_names = features
        # Create the feature importances plot
        fig, ax = plt.subplots(1, 3, figsize=(15, 5))
        # plot importances with feature weight
        xgb.plot_importance(
            booster=xgc,
            importance_type='weight',
            title='Feature Weight',
            show_values=False,
            height=0.5,
            ax=ax[0],
        )
        # plot importances with split mean gain
        xgb.plot_importance(
            booster=xgc,
            importance_type='gain',
            title='Split Mean Gain',
            show_values=False,
            height=0.5,
            ax=ax[1]
        )
        # plot importances with sample coverage
        xgb.plot_importance(
            xgc,
            importance_type='cover',
            title='Sample Coverage',
            show_values=False,
            height=0.5,
            ax=ax[2]
        )
        plt.tight_layout()
        st.pyplot(fig=fig)
