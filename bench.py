#!/usr/bin/env python

import argparse
import asyncio
import openfga_sdk
import openfga_sdk.sync
from openfga_sdk.client.models.check_request import ClientCheckRequest


parser = argparse.ArgumentParser(
    prog='bench.py',
    description='Benchmarks async vs sync batch_check performance',
    epilog='Sources can be found at https://github.com/booniepepper/openfga-python-batch-check-bench/'
)
parser.add_argument('mode', choices=['async', 'sync'])
parser.add_argument('-n', '--n-requests', default=5000)

args = parser.parse_args()
n_requests = int(args.n_requests)

configuration = openfga_sdk.ClientConfiguration(
    api_scheme='http',
    api_host='localhost:8080',
    store_id='01HE8E0SARPJ08K268AEXFA22S',
    authorization_model_id='01HE8E1C37P38PTWTK2FMZBXMB'
)


requests = []
for _ in range(n_requests):
    request = ClientCheckRequest('user:bob', 'member', 'group:x')
    requests.append(request)


async def async_batch_check():
    async with openfga_sdk.OpenFgaClient(configuration) as fga:
        await fga.batch_check(requests)


def sync_batch_check():
    fga = openfga_sdk.sync.OpenFgaClient(configuration)
    fga.batch_check(requests)


def main():
    if (args.mode == 'async'):
        asyncio.run(async_batch_check())
    elif (args.mode == 'sync'):
        sync_batch_check()


if __name__ == '__main__':
    main()
