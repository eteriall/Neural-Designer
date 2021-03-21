from flask import Flask
import seaborn as sns
import requests
from drawing.colors import color_palette

app = Flask(__name__)


@app.route('/')
def index():
    palette = color_palette()
    colors = list(map(lambda x: f'rgb({x[0]}, {x[1]}, {x[2]})', palette))
    return '\n'.join(map(lambda x: f"<p style='background-color:{x}'>asdf</p>", colors)) + f'\n{palette}'


if __name__ == "__main__":
    app.run()
