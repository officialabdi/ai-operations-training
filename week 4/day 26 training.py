
import asyncio
from unittest import result

async def greet(name, delay):
    print(f"starting greeting for {name}")
    await asyncio.sleep(delay)
    print(f"hello, {name}")

async def main():
    await asyncio.gather(
        greet("Luigi", 2),
        greet("Maria", 1)
    )

asyncio.run(main())

import asyncio
import time

async def send_confirmation_email(customer_name, reservation_time):
    await asyncio.sleep(1.5)
    print(f"email sent to {customer_name} for {reservation_time}")
    return f"{customer_name}: confirmed"

async def process_batch(reservation):
    tasks = []
    for customer, time_slot in reservation:
        task = send_confirmation_email(customer, time_slot)
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results
async def main():
    reservations = [
        ("marco",   "sat 7:00pm"),
        ("Sarah",   "Sat 7:30pm"),
        ("John",    "Sat 8:00pm"),
        ("Aoife",   "Sat 8:00pm"),
        ("Declan",  "Sat 8:30pm"),
        ("Fatima",  "Sat 9:00pm"),
    ]
    print(f"processing {len(reservations)} reservations...\n")
    start = time.time()
    results = time.time()
    results = await process_batch(reservations)
    end = time.time()

    print(f"\n batch complete: {len(results)} emails sent in {end - start:.2f} seconds")
    print(f"Sequential would have taken: {len(reservations) * 1.5:.1f} seconds")

asyncio.run(main())    