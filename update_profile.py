import os
import requests
from datetime import datetime

def fetch_repos(username):
    url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=100"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

def get_top_projects(repos):
    # Sort repos by stars
    sorted_repos = sorted(repos, key=lambda x: x['stargazers_count'], reverse=True)
    top_projects = []
    for repo in sorted_repos[:5]: # Top 5 projects
        top_projects.append(f"- [**{repo['name']}**]({repo['html_url']}) - ⭐ {repo['stargazers_count']} | {repo['description'] or 'No description'}")
    return "\n".join(top_projects)

def get_recent_activity(username):
    url = f"https://api.github.com/users/{username}/events/public"
    response = requests.get(url)
    if response.status_code == 200:
        events = response.json()
        activity = []
        # Group by repo and limit
        count = 0
        for event in events:
            if event['type'] == 'PushEvent' and count < 5:
                repo_name = event['repo']['name'].split('/')[-1]
                repo_link = f"https://github.com/{event['repo']['name']}"
                commit_msg = event['payload']['commits'][0]['message'].split('\n')[0]
                activity.append(f"- 🚀 Pushed to [**{repo_name}**]({repo_link}): *{commit_msg}*")
                count += 1
        return "\n".join(activity)
    return "No recent activity found."

def update_readme():
    username = "zmzhace"
    repos = fetch_repos(username)
    
    top_projects_content = get_top_projects(repos)
    activity_content = get_recent_activity(username)
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("README.md.template", "r", encoding="utf-8") as f:
        template = f.read()

    # Replace placeholders
    readme = template.replace("<!-- START_SECTION:projects -->\n<!-- 这是自动化脚本更新内容的占位符 -->\n<!-- END_SECTION:projects -->", 
                              f"<!-- START_SECTION:projects -->\n{top_projects_content}\n<!-- END_SECTION:projects -->")
    
    readme = readme.replace("<!-- START_SECTION:activity -->\n<!-- 这是自动化脚本更新内容的占位符 -->\n<!-- END_SECTION:activity -->", 
                              f"<!-- START_SECTION:activity -->\n{activity_content}\n<!-- END_SECTION:activity -->")
    
    readme = readme.replace("<!-- DATE -->", current_date)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

if __name__ == "__main__":
    update_readme()
