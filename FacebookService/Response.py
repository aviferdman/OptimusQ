# represents a FB Module response
class Response:
    def __init__(self, ok, error_msg, status, body_text, data=None):
        self.ok = ok  # A boolean indicating whether the response was successful (status in the range 200–299) or not
        self.error_msg = error_msg
        self.status = status    # The status message corresponding to the status code. (e.g., OK for 200)
        self.body_text = body_text
        self.data = data