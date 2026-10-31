from app.nlp.semantic_memory import find_relevant_memory


memories = [
    {
        "category": "Places",
        "title": "Favourite place",
        "description": "Shimla is my favourite place."
    },
    {
        "category": "Interests",
        "title": "Gardening",
        "description": "I enjoy growing flowers in my garden."
    },
    {
        "category": "People",
        "title": "Granddaughter",
        "description": "My granddaughter visits me every Sunday."
    }
]


test_questions = [
    "Where do I enjoy travelling?",
    "What do I like doing with plants?",
    "Who visits me every Sunday?",
    "What is my favourite place?",
    "What is my favourite food?"
]


for question in test_questions:

    result = find_relevant_memory(
        question,
        memories
    )

    print("\nQuestion:", question)

    if result:
        print("Retrieved:", result["memory"]["title"])
        print("Similarity:", result["similarity"])
    else:
        print("No relevant memory found.")