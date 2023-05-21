import time
from datetime import timedelta
import asyncio

async def generate_chart_message(ctx, estimated_time):
    start_time = time.time()
    previous_message = None
    remaining_time = estimated_time

    while True:
        elapsed_time = time.time() - start_time

        if remaining_time <= 0:
            message = "Generating your chart is taking longer than estimated :c\n\nPlease wait patiently! :timer:"
            await previous_message.edit(content=message)
            break

        remaining_time = max(0, estimated_time - elapsed_time)

        message = f":chart_with_upwards_trend: Generating the chart...\n\nEstimated Time: {timedelta(seconds=int(remaining_time))} :hourglass_flowing_sand:\n\nPlease wait patiently! :timer:"

        if previous_message is None:
            previous_message = await ctx.send(message)
        else:
            await previous_message.edit(content=message)

        # Delay the loop to avoid excessive updates
        await asyncio.sleep(1)  # Adjust the delay interval as needed

    return previous_message
