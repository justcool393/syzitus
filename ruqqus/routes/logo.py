import time
import jinja2
import pyotp
import pprint
import sass
import mistletoe
from flask import *
import PIL
import io
from PIL import ImageFont, ImageDraw

from ruqqus.helpers.wrappers import *
from ruqqus.helpers.markdown import *
from ruqqus.classes import *
from ruqqus.mail import *
from ruqqus.__main__ import app, limiter, debug


@app.get("/logo/jumbotron")
@app.get("/logo/jumbotron/<color>")
@app.get("/logo/jumbotron/<color>/<letter>")
@cache.memoize()
def get_logo_jumbotron(color=None, letter=None):

    color = color or app.config["COLOR_PRIMARY"]

    primary_r=int(color[0:2], 16)
    primary_g=int(color[2:4], 16)
    primary_b=int(color[4:6], 16)

    primary = (primary_r, primary_g, primary_b, 255)


    base_layer = PIL.Image.open(f"{app.config['RUQQUSPATH']}/assets/images/logo/logo_base.png")
    text_layer = PIL.Image.new("RGBA", base_layer.size, color=(255,255,255,0))

    #make base layer white with 50% opacity
    ImageDraw.floodfill(
        base_layer,
        (base_layer.size[0]//2, base_layer.size[1]//2),
        value=(255, 255, 255, 128)
        )

    #tilted letter layer
    font = ImageFont.truetype(
        f"{app.config['RUQQUSPATH']}/assets/fonts/Arial-bold.ttf", 
        size=base_layer.size[1]//2
    )

    letter = letter or app.config["SITE_NAME"][0:1].lower()
    box = font.getbbox(letter)

    d = ImageDraw.Draw(text_layer)
    d.text(
        (
            base_layer.size[0] // 2 - box[2] // 2, 
            base_layer.size[0] // 2 - (box[3]+box[1]) // 2
            ),
        letter, 
        font=font,
        fill=primary
        )

    text_layer = text_layer.rotate(
        angle=20, 
        expand=False, 
        fillcolor=(255,255,255,0),
        center=(
            text_layer.size[0]//2,
            text_layer.size[0]//2
            ),
        resample=PIL.Image.BILINEAR)

    #put tilted letter on speech bubble
    base_layer = PIL.Image.alpha_composite(base_layer, text_layer)

    #put speech bubble on background
    background_layer = PIL.Image.new("RGBA", base_layer.size, color=primary)
    unit_block = PIL.Image.alpha_composite(background_layer, base_layer)

    #tilt and re-size unit block
    unit_block = unit_block.rotate(
        angle=25,
        expand=True,
        fillcolor=primary,
        resample=PIL.Image.BILINEAR
        )

    unit_block = unit_block.resize(
        (
            unit_block.size[0]//10,
            unit_block.size[1]//10
            ),
        resample=PIL.Image.BILINEAR
        )

    output=PIL.Image.new(
        "RGBA", 
        (
            unit_block.size[0]*25,
            unit_block.size[1]*15
            ), 
        color=(255,255,255,0)
        )


    for i in range(25):
        for j in range(15):

            output.paste(
                unit_block,
                (
                    unit_block.size[0]*i,
                    unit_block.size[1]*j
                    )
                )

    output_bytes=io.BytesIO()
    output.save(output_bytes, format="PNG")
    output_bytes.seek(0)
    return send_file(output_bytes, mimetype="image/png")

@app.get("/logo/main/<color>/<letter>")
@cache.memoize()
def get_logo_color(color, letter=None):

    primary_r=int(app.config["COLOR_PRIMARY"][0:2], 16)
    primary_g=int(app.config["COLOR_PRIMARY"][2:4], 16)
    primary_b=int(app.config["COLOR_PRIMARY"][4:6], 16)

    primary = (primary_r, primary_g, primary_b, 255)

    base_layer = PIL.Image.open(f"{app.config['RUQQUSPATH']}/assets/images/logo/logo_base.png")
    text_layer = PIL.Image.new("RGBA", base_layer.size, color=(255,255,255,0))

    #flood fill main logo shape
    ImageDraw.floodfill(
        base_layer,
        (base_layer.size[0]//2, base_layer.size[1]//2),
        value=primary
        )


    #tilted letter layer
    font = ImageFont.truetype(
        f"{app.config['RUQQUSPATH']}/assets/fonts/Arial-bold.ttf", 
        size=base_layer.size[1]//2
    )

    letter = app.config["SITE_NAME"][0:1].lower()
    box = font.getbbox(letter)

    d = ImageDraw.Draw(text_layer)
    d.text(
        (
            base_layer.size[0] // 2 - box[2] // 2, 
            base_layer.size[0] // 2 - (box[3]+box[1]) // 2
            ),
        letter, 
        font=font,
        fill=(255,255,255,255)
        )

    text_layer = text_layer.rotate(
        angle=20, 
        expand=False, 
        fillcolor=(255,255,255,0),
        center=(
            text_layer.size[0]//2,
            text_layer.size[0]//2
            ),
        resample=PIL.Image.BILINEAR)

    output=PIL.Image.alpha_composite(base_layer, text_layer)
    output_bytes=io.BytesIO()
    output.save(output_bytes, format="PNG")
    output_bytes.seek(0)
    return send_file(output_bytes, mimetype="image/png")


@app.get("/logo/white/<color>/<letter>")
@cache.memoize()
def get_logo_color(color, letter=None):

    primary_r=int(app.config["COLOR_PRIMARY"][0:2], 16)
    primary_g=int(app.config["COLOR_PRIMARY"][2:4], 16)
    primary_b=int(app.config["COLOR_PRIMARY"][4:6], 16)

    primary = (primary_r, primary_g, primary_b, 255)

    base_layer = PIL.Image.open(f"{app.config['RUQQUSPATH']}/assets/images/logo/logo_base.png")
    text_layer = PIL.Image.new("RGBA", base_layer.size, color=(255,255,255,0))

    #tilted letter layer
    font = ImageFont.truetype(
        f"{app.config['RUQQUSPATH']}/assets/fonts/Arial-bold.ttf", 
        size=base_layer.size[1]//2
    )

    letter = app.config["SITE_NAME"][0:1].lower()
    box = font.getbbox(letter)

    d = ImageDraw.Draw(text_layer)
    d.text(
        (
            base_layer.size[0] // 2 - box[2] // 2, 
            base_layer.size[0] // 2 - (box[3]+box[1]) // 2
            ),
        letter, 
        font=font,
        fill=primary
        )

    text_layer = text_layer.rotate(
        angle=20, 
        expand=False, 
        fillcolor=(255,255,255,0),
        center=(
            text_layer.size[0]//2,
            text_layer.size[0]//2
            ),
        resample=PIL.Image.BILINEAR)

    output=PIL.Image.alpha_composite(base_layer, text_layer)
    output_bytes=io.BytesIO()
    output.save(output_bytes, format="PNG")
    output_bytes.seek(0)
    return send_file(output_bytes, mimetype="image/png")

@app.get('/logo/<kind>/<color>/<letter>/<width>/<height>')
@cache.memoize()
def get_assets_images_splash(kind, width, height, color=None, letter=None):

    try:
        width=int(width)
        height=int(height)
    except:
        abort(404)

    if max(width, height)>4500:
        abort(404)

    if kind not in ["splash", "thumb"]:
        abort(404)

    color = color or app.config["COLOR_PRIMARY"]

    primary_r=int(color[0:2], 16)
    primary_g=int(color[2:4], 16)
    primary_b=int(color[4:6], 16)

    primary = (primary_r, primary_g, primary_b, 255)

    base_layer = PIL.Image.new("RGBA", (width, height), color=primary)

    text_layer = PIL.Image.new("RGBA", (width, height), color=(255,255,255,0))

    size=min(height//2, width//2)

    font = ImageFont.truetype(
        f"{app.config['RUQQUSPATH']}/assets/fonts/Arial-bold.ttf", 
        size=size
        )

    letter = app.config["SITE_NAME"][0:1].lower()
    box = font.getbbox(letter)

    d = ImageDraw.Draw(text_layer)
    d.text(
        (
            width // 2 - box[2] // 2, 
            height // 2 - (box[3]+box[1]) // 2
            ),
        letter, 
        font=font,
        fill=(255,255,255,255)
        )

    text_layer = text_layer.rotate(
        angle=20, 
        expand=False, 
        fillcolor=primary,
        resample=PIL.Image.BILINEAR)

    if kind=="thumb":
        font = ImageFont.truetype(
            f"{app.config['RUQQUSPATH']}/assets/fonts/Arial-bold.ttf", 
            size=int(size*0.6)
            )
        fullbox=font.getbbox(app.config["SITE_NAME"].lower())

        if fullbox[2]>width:
            abort(400)

        d = ImageDraw.Draw(text_layer)
        d.text(
            (
                width//2 - fullbox[2]//2,
                height//2 + (box[3]-box[1]) // 2 + int(size*0.2)
                ),
            app.config["SITE_NAME"].lower(),
            font=font,
            fill=(255,255,255,255)
            )

    output=PIL.Image.alpha_composite(base_layer, text_layer)

    output_bytes=io.BytesIO()
    output.save(output_bytes, format="PNG")
    output_bytes.seek(0)
    return send_file(output_bytes, mimetype="image/png")