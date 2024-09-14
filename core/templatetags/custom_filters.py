from django import template
from bs4 import BeautifulSoup

register = template.Library()

@register.filter(name='truncate_html')
def truncate_html(value, limit=250):
    """
    Truncate HTML content to a specified number of characters, excluding images.
    """
    if not value:
        return ""
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(value, 'html.parser')
    
    # Find all images and temporarily remove them
    for img in soup.find_all('img'):
        img.decompose()
    
    # Get the text content, truncated
    text = soup.get_text()
    truncated_text = text[:limit] + ('...' if len(text) > limit else '')
    
    # Create a new BeautifulSoup object with the truncated text
    truncated_soup = BeautifulSoup(f'<div class="break-words">{truncated_text}</div>', 'html.parser')
    
    # Restore the images to their original positions
    for img in soup.find_all('img'):
        truncated_soup.div.insert_after(img)
    
    return str(truncated_soup)
