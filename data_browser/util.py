def annotation_path(path):
    res = "_".join(["ddb"] + path)
    res = res.replace("__", "_0")
    return res
