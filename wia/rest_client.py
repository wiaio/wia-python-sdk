import requests
import wia

'''
wia_post:
    args:
        path:   string specifying url path
        kwargs: variable-length dict which can
                contain data for post request
'''
def post(path, kwargs, device=None):
    key = 'Bearer ' + wia.secret_key
    url = wia.rest_api_base + '/' + path
    headers = {'Authorization': key}
    data = kwargs
    r = requests.post(url, json=data, headers=headers)
    try:
        r = r.json()
    except ValueError:
        pass
    return r

'''
wia_put:
    args:
        path:   string specifying url path
        kwargs: variable-length dict which can
                contain data for put request
'''
def put(path, **kwargs):
    url = wia.rest_api_base + '/' + path
    key = 'Bearer ' + wia.secret_key
    headers = {'Authorization': key}
    data = kwargs
    r = requests.put(url, json=data, headers=headers)
    return r.json()

'''
wia_get:
    args:
        path:   string specifying url path
        sk: secret_key IFF device is retrieving itself
        kwargs: variable-length dict which can
                contain query params
'''
def get(path=None, **kwargs):
    key = 'Bearer ' + wia.secret_key
    url = wia.rest_api_base + '/' + path
    headers = {'Authorization': key}
    r = requests.get(url, headers=headers, params=kwargs)
    return r.json()
'''
wia_delete:
    args:
        path: string specifying url path
'''
def delete(path):
    url = wia.rest_api_base + '/' + path
    key = 'Bearer ' + wia.secret_key
    headers = {'Authorization': key}
    r = requests.delete(url, headers=headers)
    return r