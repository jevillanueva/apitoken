def validateHTTPS(url: str, schema: str = "") -> str:
    """Validate if the url is https or http and return the url with the correct schema

    Args:
        url (str): Url to validate
        schema (str, optional): Schema to validate. Defaults to "".

    Returns:
        str: Url with the correct schema
    """
    if schema == "":
        return url
    else:
        if schema == "https":
            url = url.replace("http://", "https://", 1)
        return url
