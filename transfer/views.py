# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
import requests


class Token:
    headers = {
        'X-Auth-Token': None
    }

    @classmethod
    def update_token(cls):
        url = 'https://iam.cn-north-1.myhuaweicloud.com/v3/auth/tokens'
        response = requests.post(url, data=str({
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "name": "getToken",
                            "password": "token123",
                            "domain": {
                                "name": "ljhsdsg"
                            }
                        }
                    }
                },
                "scope": {
                    "project": {
                        "name": "cn-north-4"
                    }
                }
            }
        }), headers={
            'Content-Type': 'application/json'
        })
        cls.headers['X-Auth-Token'] = response.headers['X-Subject-Token']
        return cls.headers

    @classmethod
    def get_token(cls):
        if cls.headers['X-Auth-Token']:
            return cls.headers
        else:
            cls.update_token()
            return cls.headers


class UploadImageAPI(APIView):
    url = "https://4c7298efd5d44a09b1affdafcf7ee5d6.apigw.cn-north-4.huaweicloud.com/v1/infers/0d69f607-0105-4767-8157-38ac4a927bd0"

    @classmethod
    def post(cls, request):
        raw_file = {'images': request.FILES.get('images').open(mode='rb')}
        response = requests.post(cls.url, files=raw_file, headers=Token.get_token())
        if response.status_code == 401:
            return Response(requests.post(cls.url, files=raw_file, headers=Token.update_token()
                                          ).text,
                            status=response.status_code)
        return Response(response.text, status=response.status_code)
