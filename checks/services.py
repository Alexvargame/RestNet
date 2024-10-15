import asyncio
import random
import time

import httpx
import os
import random



from .models import Check

async def get_rendered_files(file,sleep):
    while sleep>0:
        await asyncio.sleep(random.randint(1,5))
        if file:
            file.status='rendered'
            print('f', file.pdf_file)
            sleep-=1
    return file

#
# async def get_printed_files(file,sleep):
#     while sleep > 0:
#         await asyncio.sleep(random.randint(1, 5))
#         if file:
#             print('fffff',file.pdf_file,file.status)
#             file.status = 'printed'
#             print('f', file.pdf_file,'напечатан на притере', file.printer_id)
#             sleep -= 1
#     return file
async def get_files(query):#)uery,courent_page):
    sleep=random.randint(1,3)
    print(f'Start:{time.strftime("%X")}')
    print('qq',[(q.pdf_file,q.order['date_created']) for q in query])
    query=await asyncio.gather(
        *[get_rendered_files(file,sleep) for file in query],
        return_exceptions=True
    )
    print(f'Finish:{time.strftime("%X")}')
    return query

# async def print_files(query):
#     sleep=random.randint(1,10)
#     print(f'Start:{time.strftime("%X")}')
#
#     print_query = await asyncio.gather(
#         *[get_printed_files(file,sleep) for file in query],
#         return_exceptions=True
#     )
#     print(f'Finish:{time.strftime("%X")}')
#     return print_query


