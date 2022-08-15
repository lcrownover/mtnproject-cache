#!/usr/bin/env python3


import requests
from bs4 import BeautifulSoup


# url = "https://www.mountainproject.com/area/105708965/oregon"
# resp = requests.get(url)
# soup = BeautifulSoup(resp.content, 'html.parser')
#
# print(soup)

# url = "https://www.mountainproject.com/photo/106229550/smith-rock"
# resp = requests.get(url)
# soup = BeautifulSoup(resp.content, 'html.parser')


class PhotoLinkHandler:
    def __init__(self, parent_link: str, url: str) -> None:
        self.parent_link = parent_link
        self.url = url
        self.caption = url.split("/")[-1]
        self.id = url.split("/")[-2]

    def _get_image_cdn_link(self) -> str:
        resp = requests.get(self.url)
        soup = BeautifulSoup(resp.content, "html.parser")
        img_a = soup.find("a", id="expand-href")
        return img_a["href"]

    @property
    def cdn_link(self) -> str:
        return self._get_image_cdn_link()


class CDNLinkHandler:
    def __init__(self, image_caption: str, url: str) -> None:
        self.image_caption = image_caption
        self.url = url

    ###
    # Private API
    ###
    def _get_filename_from_url(self) -> str:
        """Returns a valid filename built from the url"""
        resource = self.url.split("/")[-1]
        filename, ext = resource.split(".")
        return f"{filename}_{self.image_caption}.{ext}"

    ###
    # Public API
    ###

    def save_image(self, filename: str = "") -> None:
        if not filename:
            filename = self._get_filename_from_url()
        img_data = requests.get(self.url).content
        with open(f"images/{filename}", "wb") as handler:
            handler.write(img_data)


# Get the CDN link from a given image link
h = PhotoLinkHandler(parent_link="", url="https://www.mountainproject.com/photo/111155582/stephanie-balbin-on-the-bolt-ladder-this-photo-also-shows-why-it-is-important-to")

# Save the image from the CDN link
h = CDNLinkHandler(image_caption=h.caption, url=h.cdn_link)
h.save_image()
