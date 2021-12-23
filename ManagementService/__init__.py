import logging
import json

import azure.functions as func
from .ManagementServiceLibrary.main import main_trigger

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    json_response = main_trigger(req)
    str_response = json.dumps(json_response)

    return func.HttpResponse(
             body=str_response,
             status_code=200
        )
