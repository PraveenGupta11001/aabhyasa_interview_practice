from celery_app import app
from automation.automator import main as run_main  # Your async function

@app.task
def run_automation():
    import asyncio
    asyncio.run(run_main())
