from os import environ


def env_setup():
    environ["RESOURCES_DIR"] = "resources"
    environ["FONTS_TXT_FILE"] = "installed_fonts.txt"
    environ["PALETTES_JSON_FILE"] = "palettes.json"
    environ["GRADIENTS_JSON_FILE"] = "gradients.json"
    environ["DATABASE_URL"] = "postgresql://ofsxjjrazrzyds:6d167a66366" \
                              "8124bb6815c31c79f350e0c05d9dff940870db5" \
                              "8521e08306dc4d@ec2-34-254-69-72.eu-west-1" \
                              ".compute.amazonaws.com:5432/d2ls7ao75v0t38"
