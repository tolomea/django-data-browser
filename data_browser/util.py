def annotation_path(path):
    res = "_".join(["ddb"] + path)
    assert "__" not in res
    return res
