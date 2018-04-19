import os
import secrets


def randomize(dir, checker):
    for file in os.listdir(dir):
        name = file.split(".")
        if name[0].endswith(checker):
            pass
        else:
            os.rename(
                f"{dir}/{file}",
                f"{dir}/{secrets.token_urlsafe(8)}{checker}.{name[1]}"
            )
