import os

import click
import qrcode
from PIL import Image
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

@click.command()
@click.option(
    "--output_file",
    default="./qrcode.png",
    help='Output file path (defaults to "./qrcode.png")',
)
@click.option(
    "--logo_path",
    default=None,
    help='Path to the logo to to embed (defaults to the Canonical one)',
)
@click.option(
    "--fg_color",
    default=None,
    help='HEX color to use for foreground (defaults to Ubuntu orange)',
)
@click.option(
    "--bg_color",
    default=None,
    help='HEX color to use for background (defaults to white)',
)

@click.argument("url")

def create(output_file, logo_path, fg_color, bg_color, url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    front_color=hex_to_rgb(fg_color) if fg_color else (233, 84, 32)
    back_color=hex_to_rgb(bg_color) if bg_color else (255, 255, 255)
    qr.add_data(url)
    qr.make(fit=True)
    logo=logo_path if logo_path else f"{os.environ.get("SNAP")}/assets/canonical.png"    
    qri = qr.make_image(
        image_factory=StyledPilImage,
        color_mask=SolidFillColorMask(
            back_color=back_color, front_color=front_color
        ),
        module_drawer=RoundedModuleDrawer(),
        embeded_image_path=logo,
    )

    qri.save(output_file)


if __name__ == "__main__":
    create()
