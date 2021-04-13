import cloudinary
from cloudinary import uploader, CloudinaryImage
import requests
import re

cloudinary.config(cloud_name='neural-designers', api_key='642977737224499', api_secret='DLAoYdeD2TDlvly9gq8UQSn8P7o')


def parse_svg_paths(svg):
    return list(map(lambda x: "<" + x, filter(lambda x: x.startswith("path"), re.split(r"<", svg))))


def remove_elements(*indexes):
    for ind in indexes:
        pass


def vectorize(filename="", detail=0.5, corners=30, colors=1,
              public_id=None):
    if public_id is None:
        result = uploader.upload(filename, width=512, height=512, crop='limit')
        public_id = result['public_id']
        print(f"Public key: {public_id}, url: {result['secure_url']}")
    svg_image = cloudinary.CloudinaryImage(public_id).image(effect=f"vectorize:"
                                                                   f"detail:{detail}"
                                                                   f":corners:{corners}"
                                                                   f":colors:{colors}")
    file_url = svg_image[10:-3] + '.svg'
    svg_file = requests.get(file_url).text
    svg_file = svg_file[svg_file.find("<g>") + 3:svg_file.rfind("</g>")]
    return svg_file


svg = vectorize(public_id='yd0cnq0dxzgjscg1afct')
path = parse_svg_paths(svg)[-1]
