from pillow_heif import register_heif_opener
from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile

# Register HEIF/HEIC support with Pillow
register_heif_opener()

def convert_heif_to_jpeg(uploaded_file):
    # Open the uploaded HEIC image
    image = Image.open(uploaded_file)

    # Create an in-memory buffer to save the JPEG
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG', quality=85)
    buffer.seek(0)

    if not getattr(uploaded_file, 'field_name', None):
        uploaded_file.field_name = 'home'
    
    # Create a Django-compatible InMemoryUploadedFile
    converted_file = InMemoryUploadedFile(
        buffer,
        field_name=uploaded_file.field_name,
        name=uploaded_file.name.rsplit('.', 1)[0] + '.jpeg',
        content_type='image/jpeg',
        size=buffer.getbuffer().nbytes,
        charset=None
    )
    return converted_file

