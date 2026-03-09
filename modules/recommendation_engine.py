from urllib.parse import quote_plus


def recommend_study_materials(topic, level):

    query = quote_plus(topic)

    resources = [

        {
            "title": f"{topic} - Wikipedia",
            "description": f"Overview and fundamental concepts about {topic}.",
            "url": f"https://en.wikipedia.org/wiki/{query}"
        },

        {
            "title": f"{topic} Lessons - Khan Academy",
            "description": f"Interactive lessons and exercises to learn {topic}.",
            "url": f"https://www.khanacademy.org/search?page_search_query={query}"
        },

        {
            "title": f"{topic} Tutorials - GeeksforGeeks",
            "description": f"Step-by-step explanations and examples about {topic}.",
            "url": f"https://www.geeksforgeeks.org/?s={query}"
        }

    ]

    return resources