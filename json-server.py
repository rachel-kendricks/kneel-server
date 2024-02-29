import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status

from views import get_all_orders, get_single_order, create_order


class JSONServer(HandleRequests):
    def do_GET(self):
        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "orders":
            if url["pk"] != 0:
                response_body = get_single_order(url["pk"], url)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            response_body = get_all_orders(url)
            return self.response(response_body, status.HTTP_200_SUCCESS.value)
        else:
            return self.response(
                "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )

    def do_POST(self):
        url = self.parse_url(self.path)

        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "orders":
            successfully_updated = create_order(request_body)
            if successfully_updated:
                return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)

        else:
            return self.response(
                "Requested resource not found",
                status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
            )


#
# THE CODE BELOW THIS LINE IS NOT IMPORTANT FOR REACHING YOUR LEARNING OBJECTIVES
#
def main():
    host = ""
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()