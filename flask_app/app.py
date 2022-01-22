from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import pickle


def load_regression_model():
    file_name = "ml_models/model.p"
    with open(file_name, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model


def format_data_for_model(data: dict):
    cols = np.array(['battery', 'internal_memory', 'num_of_cameras', 'primary_cam','ram', 'screen_size', 'year', 'selfie_cam', '5g_No', '5g_Yes',
       'card_slot_No', 'card_slot_Yes', 'display_type_AMOLED','display_type_Dynamic AMOLED','display_type_Foldable Dynamic AMOLED', 'display_type_IPS',
       'display_type_IPS LCD', 'display_type_LCD', 'display_type_LCD TFT','display_type_LTPS IPS LCD', 'display_type_Liquid Retina IPS LCD','display_type_Retina IPS LCD', 'display_type_Super AMOLED',
       'display_type_Super AMOLED Plus','display_type_Super Retina XDR OLED', 'display_type_TFT', 'gps_No','gps_Yes', '4g_No', '4g_Yes', 'nfc_No', 'nfc_Yes', 'model_11',
       'model_11 pro', 'model_12', 'model_12 pro', 'model_13 pro max','model_3 gs', 'model_4s', 'model_5', 'model_5c', 'model_5s',
       'model_6', 'model_6s', 'model_7', 'model_7+', 'model_8','model_8+', 'model_se', 'model_x', 'model_xr', 'model_xs',
       'model_xs max', 'model_xs pro'])
    formated_data = pd.DataFrame(columns=cols)

    return formated_data


app = Flask(__name__)

@app.route('/predict', methods = ['GET', 'POST'])
def predict():
    data = np.array([[6.000e+02, 6.400e+01, 2.000e+00, 2.000e+00, 4.000e+00, 4.200e+00,
            2.012e+03, 1.000e+00, 1.000e+00, 0.000e+00, 1.000e+00, 0.000e+00,
            0.000e+00, 0.000e+00, 0.000e+00, 1.000e+00, 0.000e+00, 0.000e+00,
            0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00,
            0.000e+00, 0.000e+00, 0.000e+00, 1.000e+00, 0.000e+00, 1.000e+00,
            1.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00,
            0.000e+00, 0.000e+00, 0.000e+00, 1.000e+00, 0.000e+00, 0.000e+00,
            0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00,
            0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00]])
    # data = request.get_json()
    # formated_data = format_data_for_model(data)
    # print(data)
    reg = load_regression_model()
    prediction = reg.predict(data)[0]
    return {"prediction": prediction}


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
