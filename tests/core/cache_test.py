from core.cache import cache


cache.set(
    "user_name",
    "Arfat"
)


print(
    cache.get("user_name")
)


cache.set(
    "temp",
    "hello",
    expire=2
)


print(
    cache.exists("temp")
)


cache.delete(
    "temp"
)


print(
    cache.get("temp")
)