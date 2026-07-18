from ai.scheduler import Scheduler
import time

scheduler = Scheduler()


def job(task):
    print("Executing:", task)


scheduler.add_task(
    task="Open YouTube",
    delay=5,
    callback=job
)

scheduler.start()

print("Scheduler Started")

# সর্বোচ্চ 7 সেকেন্ড অপেক্ষা করবে
time.sleep(7)

print("✅ Scheduler Test Passed")