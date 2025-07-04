from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject


def trim_pdf(input_path, output_path, trim_pixels=10, alternate_trim=None):
    """
    Trim PDF pages with optional alternating left/right trimming for better alignment.

    Args:
        input_path: Path to input PDF
        output_path: Path to output PDF
        trim_pixels: Base trim amount for all sides
        alternate_trim: Dict with 'left_pages' and 'right_pages' keys for additional trimming
                      e.g., {'left_pages': 20, 'right_pages': 15} adds extra trim to left/right
    """
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page_num, page in enumerate(reader.pages):
        media_box = page.mediabox

        # Base trim amounts
        left_trim = trim_pixels
        right_trim = trim_pixels

        # Add alternating trim if specified
        if alternate_trim:
            if page_num % 2 == 0:  # Even pages (0, 2, 4...) - typically left pages
                left_trim += alternate_trim.get('left_pages', 0)
            else:  # Odd pages (1, 3, 5...) - typically right pages
                right_trim += alternate_trim.get('right_pages', 0)

        new_media_box = RectangleObject((
            media_box.lower_left[0] + left_trim,  # left
            media_box.lower_left[1] + trim_pixels,  # bottom
            media_box.upper_right[0] - right_trim,  # right
            media_box.upper_right[1] - trim_pixels  # top
        ))

        page.mediabox = new_media_box
        page.cropbox = new_media_box
        writer.add_page(page)

    with open(output_path, 'wb') as output_file:
        writer.write(output_file)


trim_pdf('../menu.pdf', '../menu.pdf',
         trim_pixels=17,
         alternate_trim={'left_pages': 6, 'right_pages': 6})
