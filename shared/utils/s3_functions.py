def remove_file_from_s3(sender, instance, field_name, **kwargs):
    """Removes the a given file from S3 bucket

    Args:
        sender (model): the model that will be sending
        instance (object): the instance of the model
        field_name (str): the field name of the file
    """

    field = getattr(instance, field_name)
    field.delete(save=False)


def get_file_url(instance, field_name):
    """Gets the file url from S3

    Args:
        instance (object): the instance of the given model
        field_name (str): the field name where the url is placed

    Returns:
        Any | None: either returns the file url or None if no file is present
    """

    file_field = getattr(instance, field_name)
    if file_field:
        return file_field.url
    else:
        return None
