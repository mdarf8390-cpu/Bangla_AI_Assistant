from ai.learning import LearningEngine


brain = LearningEngine()


brain.learn("youtube")

brain.learn("youtube")

brain.learn("spotify")

brain.learn("youtube", "lofi")

brain.learn("youtube", "lofi")

brain.learn("youtube", "python")


print(brain.favorite_app())

print(brain.favorite_query("youtube"))

print(brain.statistics())