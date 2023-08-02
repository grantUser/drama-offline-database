# Drama Database Update

This project contains a Python script that updates a drama database using the MyDramaList API.

Similar project in the anime field:
https://github.com/manami-project/anime-offline-database

## Usage

To use the script, follow these steps:

1. Make sure you have Python installed on your system.

2. Place the `drama-database.json` file containing your initial database in the same directory as `main.py`.

3. Run the `main.py` script using the following command:

```bash
python main.py
```

The script will update the database by fetching details of new dramas from the MyDramaList API and saving the changes to the drama-database.json file.

## GitHub Actions

This project is configured with GitHub Actions workflows to automate the database update at regular intervals and on every push to the "master" and "main" branches. Below is the content of the workflow file (.github/workflows/database.yml):

GitHub Actions workflows are triggered every hours (cron) and can also be manually triggered from the GitHub Actions interface (workflow_dispatch). Additionally, the workflow is triggered on every push to the "master" and "main" branches. The workflow runs on the "ubuntu-latest" image, sets up Python, installs dependencies from requirements.txt, runs the main.py script to update the database, and then commits and pushes the changes to the remote repository.

Please be cautious as this script updates the existing database, so it's recommended to have a backup in case something goes wrong.
