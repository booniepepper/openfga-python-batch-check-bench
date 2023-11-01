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


configuration = openfga_sdk.ClientConfiguration(
    api_host='api.us1.fga.dev',
    store_id='01H8M76TB3P7EWC6T298WTJX2D',
    credentials=openfga_sdk.credentials.Credentials(
        method='client_credentials',
        configuration=openfga_sdk.credentials.CredentialConfiguration(
            api_issuer='fga.us.auth0.com',
            api_audience='https://api.us1.fga.dev/',
            client_id='P99BJ2XKlB1N8NdIPzN5Ew8mBegEz0FJ',
            client_secret=os.getenv('OPENFGA_CLIENT_SECRET')
        )
    )
)


requests = []
for _ in range(args.n_requests):
    key = openfga_sdk.TupleKey()
    request = openfga_sdk.CheckRequest(key)
    requests.append(request)


async def async_batch_check():
    start = datetime.now()
    async with openfga_sdk.OpenFgaClient(configuration) as fga:
        await fga.batch_check(requests)
    end = datetime.now()
    print("Async elapsed seconds:", end - start)


def sync_batch_check():
    start = datetime.now()
    fga = openfga_sdk.sync.OpenFgaClient(configuration)
    fga.batch_check(requests)
    end = datetime.now()
    print("Sync elapsed seconds:", end - start)


def main():
    if (args.mode == 'async'):
        asyncio.run(async_batch_check())
    elif (args.mode == 'sync'):
        sync_batch_check()


if __name__ == '__main__':
    main()
