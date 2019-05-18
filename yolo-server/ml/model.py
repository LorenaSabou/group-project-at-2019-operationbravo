import cv2


def get_model(weights_path, config_path):
    """
    Returns the corresponding dark net model.
    :param weights_path: the weights path
    :param config_path: the config path
    :return: the dark net model
    """
    net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
    return net
