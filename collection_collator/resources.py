from pkg_resources import resource_filename


def get_file(file):
    return resource_filename(__name__, 'resources/'+file)
