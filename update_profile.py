import os
import requests
from datetime import datetime

def get_recent_activity(username):
    url = f"https://api.github.com/users/{username}/events/public"
    headers = {"Authorization": f"token {os.environ.get('GITHUB_TOKEN')}"} if os.environ.get('GITHUB_TOKEN') else {}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        events = response.json()
        activity = []
        count = 0
        for event in events:
            if event['type'] == 'PushEvent' and count < 5:
                payload = event.get('payload', {})
                commits = payload.get('commits', [])
                if not commits:
                    continue
                repo_name = event['repo']['name'].split('/')[-1]
                repo_link = f"https://github.com/{event['repo']['name']}"
                commit_msg = commits[0]['message'].split('\n')[0]
                activity.append(f"- 🚀 Pushed to [**{repo_name}**]({repo_link}): *{commit_msg}*")
                count += 1
        return "\n".join(activity)
    else:
        print(f"Failed to fetch events: {response.status_code} - {response.text}")
    return "No recent activity found."

def update_readme():
    username = "zmzhace"
    activity_content = get_recent_activity(username)
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("README.md.template", "r", encoding="utf-8") as f:
        template = f.read()

    # Replace placeholders
    readme = template.replace("<!-- START_SECTION:activity -->\n<!-- 这是自动化脚本更新内容的占位符 -->\n<!-- END_SECTION:activity -->", 
                              f"<!-- START_SECTION:activity -->\n{activity_content}\n<!-- END_SECTION:activity -->")
    
    readme = readme.replace("<!-- DATE -->", current_date)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

if __name__ == "__main__":
    update_readme()
