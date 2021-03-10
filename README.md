# backend-v1.0
backend 


### Run bash on heroku:

Run bash on heroku

```heroku run bash --app vizy-testing-sam```


### Installation instructions:

Install python, pipenv and all required packages

```pipenv install --dev```

Install postgres?

### Git Branch management:
#### List all branches:
```git branch```

#### Create new branch: 
```git branch new-branch```

#### Switch branches: 
```git checkout new-branch```

#### Merge changes form dev branch to master:
1. Switch to master: ```git checkout master```
2. Merge from dev branch into master: ```git merge dev-branch```

### Add Heroku remotes to Git (using Heroku CLI)
Add remote heroku-testing-sam: ```heroku git:remote -a vizy-testing-sam -r heroku-testing-sam```

Add remote heroku-testing-ben: ```heroku git:remote -a vizy-testing-ben -r heroku-testing-ben```

Add remote heroku-testing: ```heroku git:remote -a vizy-testing -r heroku-testing```

Add remote heroku-staging: ```heroku git:remote -a vizy-staging -r heroku-staging```

Add remote heroku-production: ```heroku git:remote -a vizy-production -r heroku-production```

### Push to Github:
```git push origin <branch-from>:<branch-to>```

### Push to Heroku app:
Push devsam to heroku-testing-sam: ```git push heroku-testing-sam devsam:master```

Push devben to heroku-testing-ben: ```git push heroku-testing-ben devben:master```

Push master to heroku-testing: ```git push heroku-testing master```

Push master to heroku-staging: ```git push heroku-staging master```

Push master to heroku-production: ```git push heroku-production master```

### Viewing realtime logs from Heroku:
```heroku logs --tail --app app-name```

### Direct database to database copy on Heroku:
```heroku pg:copy vizy-production::DATABASE_URL DATABASE_URL --app vizy-testing-sam```
https://devcenter.heroku.com/articles/heroku-postgres-backups#direct-database-to-database-copies

