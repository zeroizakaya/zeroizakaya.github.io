from pdf2image import convert_from_path
from pathlib import Path
from typing import List, Optional, Union


def pdf_to_images(
    pdf_path: Union[str, Path],
    output_dir: Optional[Union[str, Path]] = None,
    output_format: str = "PNG",
    dpi: int = 200,
    first_page: Optional[int] = None,
    last_page: Optional[int] = None,
    poppler_path: Optional[str] = None,
    prefix: str = "page",
    quality: int = 95
) -> List[str]:
    """
    Convert a multi-page PDF to a set of images.

    Args:
        pdf_path: Path to the input PDF file
        output_dir: Directory to save images (default: same as PDF directory)
        output_format: Image format (PNG, JPEG, etc.)
        dpi: Resolution for conversion (higher = better quality, larger file)
        first_page: First page to convert (1-indexed, None = start from beginning)
        last_page: Last page to convert (1-indexed, None = convert to end)
        poppler_path: Path to poppler binaries (Windows only, usually)
        prefix: Prefix for output filenames
        quality: JPEG quality (1-100, only applies to JPEG format)

    Returns:
        List of paths to generated image files

    Raises:
        FileNotFoundError: If PDF file doesn't exist
        ValueError: If invalid page range specified
    """
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if output_dir is None:
        output_dir = pdf_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    try:
        images = convert_from_path(
            pdf_path,
            dpi=dpi,
            first_page=first_page,
            last_page=last_page,
            poppler_path=poppler_path,
            fmt=output_format.lower()
        )
    except Exception as e:
        raise RuntimeError(f"Failed to convert PDF: {e}")

    if not images:
        raise ValueError("No pages found in the specified range")

    saved_files = []
    base_name = pdf_path.stem

    for i, image in enumerate(images, start=1):
        page_num = (first_page or 1) + i - 1

        filename = f"{prefix}_{base_name}_{page_num:03d}.{output_format.lower()}"
        file_path = output_dir / filename

        save_kwargs = {}
        if output_format.upper() == "JPEG":
            save_kwargs["quality"] = quality
            save_kwargs["optimize"] = True
        elif output_format.upper() == "PNG":
            save_kwargs["optimize"] = True

        image.save(file_path, output_format.upper(), **save_kwargs)
        saved_files.append(str(file_path))
        print(f"Saved {str(file_path)}")

    return saved_files


if __name__ == "__main__":
    try:
        result = pdf_to_images(
            "../menu.pdf",
            output_dir="output",
            output_format="PNG",
            dpi=200,
            quality=95
        )
        print(f"Conversion complete: {result}")
    except Exception as e:
        print(f"Error: {e}")
