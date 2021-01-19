from config import UPLOAD_FOLDER
import numpy as np
import tensorflow as tf
import uuid
from tensorflow.keras.applications.xception import decode_predictions
from sklearn import preprocessing
import pandas as pd
from os import walk
from sklearn.decomposition import PCA
import pickle
import os

from redis_client import store_object, get_objects, clear_all

image_net_model = tf.keras.applications.xception.Xception(weights='imagenet',include_top=True)

pre_final_model = tf.keras.Model(
    image_net_model.input,
    image_net_model.get_layer("avg_pool").output
)

pca = None

def get_pca():
    global pca
    if pca is None:
        pca = PCA(n_components=3, whiten=True)
    return pca

def load_pca():
    global pca
    with open(os.path.join(UPLOAD_FOLDER,"pca_components"), "rb+") as pca_file:
        pca = pickle.load(pca_file)

def get_features_dict(pre_final, results_dict, target):
    for it, element in enumerate(np.nditer(pre_final[0]), start=1):
        if not results_dict.get(f"feature_{it}"):
            results_dict[f"feature_{it}"] = []
        results_dict[f"feature_{it}"].append(element)
    results_dict["targets"].append(target)

    return results_dict

def get_principal_components(target_dict, features):
    pd_results = pd.DataFrame.from_dict(target_dict)
    x = pd_results.loc[:, features].values
    x = preprocessing.normalize(x, norm='l2')
    reduced = get_pca().transform(x)
    reduced = preprocessing.normalize(reduced, norm='l2')
    return reduced

def get_predictions(image):
    cur_img=tf.keras.preprocessing.image.img_to_array(image)
    cur_img = tf.keras.preprocessing.image.smart_resize(cur_img, (299, 299), interpolation='bilinear')
    processed_img = tf.keras.applications.xception.preprocess_input(cur_img)

    cur_predictions=image_net_model.predict(np.array([processed_img]))
    imagenet_label = decode_predictions(cur_predictions,top=1)[0][0][1]
    pre_final_predictions = pre_final_model.predict(np.array([processed_img]))
    return pre_final_predictions, imagenet_label

def as_web_objects(components, names, predictions, file_names, predefined=False):
    result = []
    for components, name, prediction, file_name in zip(components, names, predictions, file_names):
        result.append(
            {
                "x": components[0],
                "y": components[1],
                "z": components[2],
                "name": name,
                "prediction": prediction,
                "url": f"/image/{file_name}",
                "predefined": predefined,
            }
        )
    
    return result

def init_data():
    clear_all()
    results_dict = {"preditcions": [], "targets": []}
    files = []
    for _, _, filenames in walk(UPLOAD_FOLDER):
        for filename in filenames:
            if len(filename.split(".")) < 2:
                continue
            # image load
            image = tf.keras.preprocessing.image.load_img(os.path.join(UPLOAD_FOLDER,filename))
            pre_final, prediction = get_predictions(image)
            target = filename.split("-")[0]
            results_dict = get_features_dict(pre_final, results_dict, target.title())
            results_dict["preditcions"].append(prediction)
            files.append(filename)
            
    preditcions = results_dict["preditcions"]
    targets = results_dict["targets"]
    results_dict.pop("targets")
    results_dict.pop("preditcions")
    features = list(results_dict.keys())
    #Apply PCA
    principalComponents = get_principal_components(results_dict, features)

    parsed = as_web_objects(principalComponents, targets, preditcions, files, predefined=True)

    for object in parsed:
        store_object(object, uuid.uuid4())
            

def query_image(image_path, name):
    image = tf.keras.preprocessing.image.load_img(os.path.join(UPLOAD_FOLDER, image_path))
    pre_final, prediction = get_predictions(image)
    target_dict = get_features_dict(pre_final, {"preditcions": [prediction], "targets": []}, name)

    preditcions = target_dict["preditcions"]
    targets = target_dict["targets"]
    target_dict.pop("targets")
    target_dict.pop("preditcions")
    features = list(target_dict.keys())

    tranformed = get_principal_components(target_dict, features)

    print(image_path)
    print(preditcions, targets, tranformed)

    return preditcions, targets, tranformed

def store_image(pil_image, file_name, name, id):
    preditcions, names, tranformed = query_image(pil_image, name)
    object = as_web_objects(tranformed, names, preditcions, [file_name])
    store_object(object[0], id)

def list_data():
    return get_objects()
