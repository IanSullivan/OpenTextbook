import requests as req
from github import Github
import git
g = Github("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")
repo = Github.Repo('https://github.com/IanSullivan/OpenTextbook.git')
# make changes to README.md
repo.index.add('README.md')
repo.index.commit("My commit message")
repo.git.checkout("-b", "new_branch")
repo.git.push("--set-upstream","origin","new_branch")
contents = repo.get_contents("/Philosophy")
for content_file in contents:
     url = content_file.download_url
     res = req.get(url)
     title = content_file.name
     raw_text = res.content.decode()
     title = title.replace(" ", "_")
     title = title.replace("?", "")
     title = title.replace(":", " ")
     with open(str(title) + '.txt', 'w') as f:
          f.write(raw_text)
