import json
import argparse

import requests

import user_exceptions as ex

url = "https://mickschroeder.com/api/citation/cite.php"
desc = 'Citation Generator'
args = [{'name': '-id',
         'type': str,
         'dest': 'id',
         'required': True,
         'help': 'publication id'}]


def create_parser(desc, args):
    parser = argparse.ArgumentParser(description=desc)
    for arg in args:
        parser.add_argument(arg['name'], type=arg['type'], dest=arg['dest'], required=arg['required'], help=arg['help'])
    return parser


def parse_args(parser):
    args = parser.parse_args()
    return args


def get_json(req):
    try:
        result = req.json()

    except json.decoder.JSONDecodeError as error:
        print("JSON Decode Error: {}".format(error))

    return result


def get_request(url, params):
    try:
        req = requests.get(url, params=params)

    except requests.exceptions.MissingSchema as error:
        print("Missing Schema error: {}".format(error))
    except requests.exceptions.ConnectionError as error:
        print("Connecting error: {}".format(error))
    except requests.exceptions.HTTPError as error:
        print("HTTP Error: {}".format(error))
    except requests.exceptions.InvalidURL as error:
        print("Invalid URL: {}".format(error))

    return req


def print_result(result):
    if result['html_citation'] == '' or result['html_citation'] == 'Not Found.':
        print("No result was found for this query. Try another -id")
    else:
        print(result['html_citation'])


if __name__ == '__main__':
    parser = create_parser(desc, args)
    args = parse_args(parser)

    req = get_request(url, [("q", args.id)])
    result = get_json(req)

    print_result(result)
