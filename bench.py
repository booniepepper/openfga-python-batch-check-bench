#!/usr/bin/env python

import argparse
import asyncio
from datetime import datetime
import openfga_sdk
import openfga_sdk.sync
import os


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
    store_id='01HE6GBVRANZNBPD49FES6X9YC',
)


requests = []
for _ in range(n_requests):
    key = openfga_sdk.TupleKey()
    request = openfga_sdk.CheckRequest(key)
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
