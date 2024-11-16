    
from pyhelm3 import Client, Chart
import asyncio 
from kubernetes_asyncio import client, config
from kubernetes_asyncio.client import ApiException
import logging

async def main():
    client = Client()
    await client.uninstall_release(release_name='citizen-dashboard')

if __name__ == "__main__":
    asyncio.run(main())