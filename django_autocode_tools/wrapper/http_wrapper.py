#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from django.http import HttpResponse, JsonResponse

# from requests import post as requests_post, adapters as requests_adapters

http_server_version = 'Apache/2.4.12'


# requests_adapters.DEFAULT_RETRIES = 3


# ===============================================================

# def post_http_request(url, data_dict):
#     headers = {'Content-Type': 'application/json;charset=utf-8'}
#     rsp = requests_post(url, data=json_dumps(data_dict), headers=headers, verify=False)
#     return rsp


# ===============================================================

class HttpRsp(HttpResponse):
    def __init__(self, *args, **kwargs):
        super(HttpRsp, self).__init__(*args, **kwargs)
        self['Server'] = http_server_version
        self['Cache-Control'] = 'no-store'


class JsonRsp(JsonResponse):
    def __init__(self, data={}, status=200, *args, **kwargs):
        super(JsonRsp, self).__init__(data, **kwargs)
        self.status_code = status
        if 200 != status:
            self.reason_phrase = 'ERR'
        self['Server'] = http_server_version
        self['Cache-Control'] = 'no-store'

        # 允许跨域
        self["Access-Control-Allow-Origin"] = 'http://localhost:8081'

        self["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
        self["Access-Control-Allow-Credentials"] = "true"
        self[
            "Access-Control-Allow-Headers"] = "Content-Type,Access-Control-Allow-Credentials, Access-Control-Allow-Headers, Authorization, X-Requested-With, X-CSRF-Token,x-csrftoken"
