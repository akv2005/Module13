import asyncio
import time
async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования.')
    for boil in range(1,5):
        await asyncio.sleep(5/power)
        print(f'Силач {name} поднял : {boil}')
    print(f'Силач {name} закончил соревнование.')

def decor_time(tour):
    async def decor():
        start = time.time()
        rez = await tour()
        finish = time.time()
        print(f'\nФункция {tour.__name__} работала {round(finish-start, 4)} сек.')
        return rez
    return decor

@decor_time
async def start_tournament():
    strongman1 = asyncio.create_task(start_strongman('Pasha', 3))
    strongman2 = asyncio.create_task(start_strongman('Denis', 4))
    strongman3 = asyncio.create_task(start_strongman('Apollon', 5))
    await strongman1
    await strongman2
    await strongman3

asyncio.run(start_tournament())