def s(path):
    return "__".join(path)


def annotation_path(path):
    return ["_".join(["ddb"] + path)]
