""" Helpers for DB models """


def get_tuples(object_list):
    """
    Args:
        object_list (list): Query desired

        return: a list of tuples
    """
    list_of_tuples = [(i.id, i.name) for i in object_list]

    return list_of_tuples
