from flask import Flask
import requests
from drawing.colors import color_palette
from drawing.drawer import draw_svg_design

app = Flask(__name__)


@app.route('/palettes')
def palettes():
    palette = color_palette()
    colors = list(map(lambda x: f'rgb({x[0]}, {x[1]}, {x[2]})', palette))
    return '\n'.join(map(lambda x: f"<p style='background-color:{x}'>asdf</p>", colors)) + f'\n{palette}'

@app.route('/generate')
def logo_generator():
    return draw_svg_design()


if __name__ == "__main__":
    app.run()
