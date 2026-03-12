from typing import Any
from django.forms import ValidationError
from django.http import HttpRequest
from time import time


def set_useragent_on_request_middleware(get_response):

    print("initial call")

    def middleware(request: HttpRequest):
        print("before get response")
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        print("after get response")
        return response

    return middleware


class CountRequestMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest) -> Any:
        self.requests_count += 1
        print("requests count", self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print("responses count", self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print("got", self.exceptions_count, "exceptions so far")


class throttling_middleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response
        self.calls_dict = dict()

    def __call__(self, request: HttpRequest) -> Any:
        current_user = request.user
        current_id = current_user.id
        last_request = self.calls_dict.get(current_id)
        interval = time() - last_request if last_request else time()
        print(f"## User id : {current_id}  Interval: {interval}")
        if last_request and interval > 0.5 or not last_request:
            self.calls_dict[current_id] = time()
            response = self.get_response(request)
            return response
        else:
            raise ValidationError(
                f"Exceeding the number of requests. Interval: {interval}"
            )
        # if current_user.is_authenticated:
        # else:
        #     raise ValidationError("The user is not authenticated")
