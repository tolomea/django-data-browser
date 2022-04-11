from django.utils.text import slugify


def annotation_path(path):
    res = "_".join(["ddb"] + path)
    res = res.replace("__", "_0")
    return res


def str_to_field(s):
    return slugify(s).replace("-", "_")
