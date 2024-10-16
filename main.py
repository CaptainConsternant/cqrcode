import os

import click
import qrcode
from PIL import Image
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer


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
@click.argument("url")
def create(output_file,logo_path, url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    logo=logo_path if logo_path else f"{os.environ.get("SNAP")}/assets/canonical.png"    
    qri = qr.make_image(
        image_factory=StyledPilImage,
        color_mask=SolidFillColorMask(
            back_color=(255, 255, 255), front_color=(233, 84, 32)
        ),
        module_drawer=RoundedModuleDrawer(),
        embeded_image_path=logo,
    )

    qri.save(output_file)


if __name__ == "__main__":
    create()
