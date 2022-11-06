def validateHTTPS(url: str, schema: str = ""):
    if schema == "":
        return url
    else:
        if schema == "https":
            url = url.replace("http://","https://",1)
        return url
    