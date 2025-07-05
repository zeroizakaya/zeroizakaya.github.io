import os


def generate_image_gallery_body(folder_path, prefix='menu', file_extension='png', eager_count=5):
    """
    Generate HTML body content for image gallery from folder files.

    Args:
        folder_path (str): Path to folder containing images
        file_extension (str): Image file extension (default: 'png')
        eager_count (int): Number of images to eager load (default: 5)

    Returns:
        str: HTML body content with img tags
    """
    files = sorted([f for f in os.listdir(folder_path) if f.endswith(f'.{file_extension}')])

    body_content = []

    for i, filename in enumerate(files):
        loading = "eager" if i < eager_count else "lazy"
        img_tag = f'    <img src="{prefix}/{filename}" alt="{filename}" loading="{loading}">'
        body_content.append(img_tag)

    return '\n'.join(body_content)


body = generate_image_gallery_body('output', 'menu', 'png', 5)
print(body)
