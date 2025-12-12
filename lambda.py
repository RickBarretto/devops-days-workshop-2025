

def lambda_handler(event, context):
    """It's working"""

    print("hello world")

    return {
        "statusCode": 200,
        "headers": { "Content-Type": "application/json" },
        "body": "{\"message\": \"It's working!\"}"
    }
