#daily jobs

from app.services import increment_daily

async def daily_job(context):
    increment_daily()
