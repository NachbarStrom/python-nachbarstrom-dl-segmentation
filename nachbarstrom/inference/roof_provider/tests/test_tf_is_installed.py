def test_tf_is_installed():
    try:
        import tensorflow
    except ModuleNotFoundError as error:
        raise ModuleNotFoundError("TensorFlow must be installed.", error)
