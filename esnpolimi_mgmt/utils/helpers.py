from django.utils.html import format_html


def create_link(link, text):
    return format_html("<a href={link}>{text}</a>", link=link, text=text)
