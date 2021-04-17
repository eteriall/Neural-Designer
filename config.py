from os import environ


def env_setup():
    environ["RESOURCES_DIR"] = "resources"
    environ["FONTS_TXT_FILE"] = "installed_fonts.txt"
    environ["PALETTES_JSON_FILE"] = "palettes.json"
    environ["GRADIENTS_JSON_FILE"] = "gradients.json"
    environ[ "DATABASE_URL"] = "postgresql://keupihyyearszi:11affb377b7fef5c10096174e25af1f9807f10780609b862cad1a3235352b078@ec2-54-195-246-55.eu-west-1.compute.amazonaws.com:5432/da7lh1nqp712fl"
