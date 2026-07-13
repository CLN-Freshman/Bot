import sys
import os

def handler(event, context):
    return {
        "statusCode": 200,
        "body": "Hello from Vercel!"
    }