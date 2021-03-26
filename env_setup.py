from os import environ


def env_setup():
    environ["RESOURCES_DIR"] = "resources"
    environ["FONTS_TXT_FILE"] = "installed_fonts.txt"
    environ["PALETTES_JSON_FILE"] = "palettes.json"
    environ["GRADIENTS_JSON_FILE"] = "gradients.json"
