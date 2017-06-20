#! /usr/bin/env python
import argparse
import hammock.client

CLIENT_CLASS_NAME = 'Client'
CLIENT_DEFAULT_URL = 'http://srv1-api.service.strato:1234'


def generate_client_code(target_path):
    """Generate the srv1-client code."""
    import srv1.resources

    client_code = hammock.client.ClientGenerator(class_name=CLIENT_CLASS_NAME,
                                                 default_url=CLIENT_DEFAULT_URL,
                                                 resources_package=srv1.resources).code

    with open(target_path, 'w') as client_code_file:
        client_code_file.write(client_code + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate srv1-client code')
    parser.add_argument('target_path', type=str, help='The client code target path')
    args = parser.parse_args()

    generate_client_code(args.target_path)
