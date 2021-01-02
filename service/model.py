image_net_model = tf.keras.applications.xception.Xception(weights='imagenet',include_top=True)

pre_final_model = tf.keras.Model(
    image_net_model.input,
    image_net_model.get_layer("avg_pool").output
)

pca = None

def init_pca():
    pca = PCA(n_components=3)
    #TODO: Add preparing for data

def query_image(pil_image):
    arr_img = tf.keras.preprocessing.image.img_to_array(pil_image)
    processed_img = tf.keras.applications.xception.preprocess_input(arr_img)

    cur_predictions=model.predict(np.array([processed_img]))
    imagnet_label = decode_predictions(cur_predictions,top=1)[0][0][1]
    pre_final_predictions = pre_final_model.predict(np.array([processed_img]))
    tranformed = pca.tranform(pre_final_predictions)

    return imagnet_label, tranformed

def store_data():
    pass

def list_data():
    pass
