def safe_fs_search(root, dir, query):
    if not dir:
        logging.error('Directory argument is required')
        return
    return fs_search(root=root, dir=dir, query=query)