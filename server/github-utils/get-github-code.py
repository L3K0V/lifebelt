from github import GitHub

gh = GitHub(client_id='YOUR_ID_HERE', client_secret='OUR_LITTLE_SECRET_HERE')
print(gh.authorize_url(state='a-random-string'))
