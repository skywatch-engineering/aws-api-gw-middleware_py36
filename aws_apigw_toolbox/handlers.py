import simplejson as json

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Credentials": True
}


def auth_context_on_error(e: Exception) -> dict:
    return {
        "statusCode": 401,
        "body": json.dumps({
            "errors": [{"message": "Unauthorized.\n" + str(e)}]
        }),
        "headers": headers
    }


def payload_parser_on_error(e: Exception) -> dict:
    return {
        "statusCode": 400,
        "body": json.dumps({
            "errors": [{"message": "Bad request.\n" + str(e)}]
        }),
        "headers": headers
    }


def to_response_api_gw(r: dict) -> dict:
    if r and isinstance(r, dict):
        if r.get('statusCode') and isinstance(r['statusCode'], int):
            if r.get('body'):
                if isinstance(r['body'], dict):
                    try:
                        body_str = json.dumps(r['body'])
                    except Exception as e:
                        response = {
                            "statusCode": 500,
                            "body": json.dumps({
                                "errors": [{
                                    "message": "Error while returning response. Return body as string instead.\n"
                                               + str(e)
                                }]
                            }),
                            "headers": headers
                        }
                    else:
                        response = {
                            "statusCode": r['statusCode'],
                            "body": body_str,
                            "headers": {
                                **headers,
                                **(r.get('headers') or {})
                            }
                        }
                elif isinstance(r['body'], str):
                    response = {k: v for k, v in r.items() if k in ['statusCode', 'body', 'headers']}
                else:
                    response = {
                        "statusCode": r['statusCode'],
                        "body": str(r['body']),
                        "headers": headers
                    }
            else:
                response = {k: v for k, v in r.items() if k in ['statusCode', 'body', 'headers']}

            return response

    message = 'Invalid lambda return. Return "statusCode" (int) and "body" (str or dict, optional)'
    return {
        "statusCode": 500,
        "body": json.dumps({"errors": [{"message": message}]}),
        "headers": headers
    }
