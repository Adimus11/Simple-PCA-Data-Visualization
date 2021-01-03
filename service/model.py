from config import UPLOAD_FOLDER
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.xception import decode_predictions
from sklearn.preprocessing import StandardScaler
import pandas as pd
from os import walk
from sklearn.decomposition import PCA

image_net_model = tf.keras.applications.xception.Xception(weights='imagenet',include_top=True)

pre_final_model = tf.keras.Model(
    image_net_model.input,
    image_net_model.get_layer("avg_pool").output
)

pca = None

def get_pca():
    if pca is None:
        pca = PCA(n_components=3)
    return pca

def get_features_dict(pre_final, results_dict, target):
    for it, element in enumerate(np.nditer(pre_final.T), start=1):
        if not results_dict.get(f"feature_{it}"):
            results_dict[f"feature_{it}"] = []
        results_dict[f"feature_{it}"].append(element)
        results_dict["targets"].append(target)

        return results_dict

def get_principal_components(target_dict, features, fit=False):
    pd_results = pd.DataFrame.from_dict(target_dict)
    x = pd_results.loc[:, features].values
    x = StandardScaler().fit_transform(x)
    if fit:
        return get_pca().fit_transform(x)
    else:
        return get_pca().tranform(x)

def get_predictions(image):
    arr_img = tf.keras.preprocessing.image.img_to_array(image)
    processed_img = tf.keras.applications.xception.preprocess_input(arr_img)

    cur_predictions=image_net_model.predict(np.array([processed_img]))
    imagenet_label = decode_predictions(cur_predictions,top=1)[0][0][1]
    pre_final_predictions = pre_final_model.predict(np.array([processed_img]))
    return pre_final_predictions, imagenet_label

def init_data():
    results_dict = {"preditcions": [], "targets": []}
    for _, _, filenames in walk(UPLOAD_FOLDER):
        for filename in filenames:
            # image load
            image = tf.keras.preprocessing.image.load_img(UPLOAD_FOLDER+filename, target_size=(299,299))
            pre_final, prediction = get_predictions(image)
            target = filename.split("-")[0]
            results_dict = get_features_dict(pre_final, results_dict, target)
            results_dict["preditcions"].append(prediction)
            
    features = list(results_dict.keys())
    preditcions = features.pop("preditcions")
    
    #Apply PCA
    principalComponents = get_principal_components(results_dict, features, fit=True)
            

def query_image(pil_image, name):
    pre_final, prediction = get_predictions(pil_image)
    target_dict = get_features_dict(pre_final, {"preditcions": [], "targets": []}, name)

    features = list(target_dict.keys())
    preditcions = features.pop("preditcions")

    pd_results = pd.DataFrame.from_dict(target_dict)
    x = pd_results.loc[:, features].values
    x = StandardScaler().fit_transform(x)
    tranformed = get_principal_components(target_dict, features)

    return prediction, tranformed

def store_data():
    pass

def list_data():
    pass
