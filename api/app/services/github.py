import httpx
import time
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "guilherme994")
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"
CACHE_TTL = 86400  # 1 hora em segundos

_cache = {
    "data": None,
    "timestamp": 0,
}

QUERY = """
{
  user(login: "%USERNAME%") {
    pinnedItems(first: 6, types: REPOSITORY) {
      nodes {
        ... on Repository {
          name
          description
          url
          homepageUrl
          stargazerCount
          primaryLanguage {
            name
            color
          }
          repositoryTopics(first: 5) {
            nodes {
              topic {
                name
              }
            }
          }
        }
      }
    }
  }
}
""".replace("%USERNAME%", GITHUB_USERNAME)


def fetch_pinned_repos():
    now = time.time()

    if _cache["data"] and (now - _cache["timestamp"]) < CACHE_TTL:
        return _cache["data"]

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json",
    }

    response = httpx.post(
        GITHUB_GRAPHQL_URL,
        json={"query": QUERY},
        headers=headers,
    )

    response.raise_for_status()

    nodes = response.json()["data"]["user"]["pinnedItems"]["nodes"]

    projects = []
    for repo in nodes:
        projects.append({
            "name": repo["name"],
            "description": repo["description"],
            "url": repo["url"],
            "homepage": repo["homepageUrl"],
            "stars": repo["stargazerCount"],
            "language": repo["primaryLanguage"]["name"] if repo["primaryLanguage"] else None,
            "language_color": repo["primaryLanguage"]["color"] if repo["primaryLanguage"] else None,
            "topics": [t["topic"]["name"] for t in repo["repositoryTopics"]["nodes"]],
        })

    _cache["data"] = projects
    _cache["timestamp"] = now

    return projects
