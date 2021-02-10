import json
import os


class EnvLoginGatherer:
    # this class is created to simplify gathering information regarding password / username from environment variables
    # EnvLoginGatherer class will probably be the parent class of the class that will encapsulate the crawler.

    def __init__(self, directory="login.json"):
        # Pass reads the json file as it is being initialized.
        # Unless stated otherwise, it assumes pass.py is in the same directory as login.json
        # and that login.json exists / names of the environment variables are stored in login.json file
        # login.json file is not being sent to github for security reasons but I'll include a loginexample.json
        # with fake environment variable names to demonstrate what it should look like
        with open(directory, "r") as f:
            self.data = json.load(f)

    def username(self, platform_name):
        # returns username as a string
        env_var = self.data[platform_name]["username"]
        return os.environ.get(env_var)

    def password(self, platform_name):
        # returns password as a string
        env_var = self.data[platform_name]["password"]
        return os.environ.get(env_var)
