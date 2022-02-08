# -*- coding: utf-8 -*-

import aiohttp


async def send_report(service_id: int, target_id: int, webhook: str, result=dict, success: bool = True):

    content = {
        "service_id": service_id,
        "block_content": result,
        "target_id": target_id,
        "success": success
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(webhook, json=content) as response:
            await response.json()
