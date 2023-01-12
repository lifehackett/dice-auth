import requests_oidc
import yaml
import pprint


# token = {
#      'access_token': 'eswfld123kjhn1v5423',
#      'refresh_token': 'asdfkljh23490sdf',
#      'token_type': 'Bearer',
#      'expires_in': '-30',     # initially 3600, need to be updated by you
# }

CACHE_FILE_PATH = 'auth/cache.yaml'


pp = pprint.PrettyPrinter(indent=2)


def save_token(token):
    print(f'\u001b[42m*** *** *** *** TOKEN *** *** *** *** \033[0m')

    pp.pprint(token)
    try:
        with open(CACHE_FILE_PATH, "w") as f:
            yaml.dump({
                'refresh_token': token['refresh_token'],
                'token_type': token['token_type']
            }, f, Dumper=yaml.Dumper, indent=2)
    except FileNotFoundError as e:
        with open(CACHE_FILE_PATH, 'x'):
            save_token(token)


def get_token(token):
    try:
        with open(CACHE_FILE_PATH, "r") as f:
            results = yaml.load(f, Loader=yaml.Loader) or {}
            return results
    except FileNotFoundError as e:
        with open(CACHE_FILE_PATH, "x"):
            return {'refresh_token': None, 'token_type': None}


def run():
    session = requests_oidc.make_oidc_session(
        oidc_url="https://auth.nonprod.dustid.net/.well-known/openid-configuration",
        client_id="restish",
        port=8484,
        updater=save_token
    )

    response = session.post(
        'https://dice-dev.nonprod.dustid.net/api/transactions/search', headers={'X-Scope-OrgID': 'f3e6ede6-5f68-4a19-9a65-79e9e7d66a8f'})
    print(f'\u001b[42m*** *** *** *** REQUEST *** *** *** *** \033[0m')

    pp.pprint(response.request.__dict__)
    print(f'\u001b[42m*** *** *** *** RESPONSE *** *** *** *** \033[0m')

    pp.pprint(response.json())


if __name__ == '__main__':
    run()
