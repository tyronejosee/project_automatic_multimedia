import os
import json
import logging

import requests
from bs4 import BeautifulSoup

from core.interfaces.command_interface import ICommand
from core.utils.functions import extract_year, sanitize_filename
from core.utils.logging import setup_logging

setup_logging()


class GenerateAnimeFoldersCommand(ICommand):
    def __init__(
        self,
        directory: str,
        headers: dict[str, str],
        elements: dict[str, str],
        url: str,
    ) -> None:
        self.directory: str = directory
        self.url: str = url
        self.headers: dict[str, str] = headers
        self.elements: dict[str, str] = elements or {}

    def execute(self) -> None:
        """
        Main method that executes the command.
        """
        links: list[str] = self._get_links()
        anime_dict = []
        for link in links:
            anime = self._scrape_link(link)
            anime_dict.append(anime)

        for data in anime_dict:
            folder_name: str = f"{data['title']} ({data['year']})"
            clean_name: str = sanitize_filename(folder_name)
            self._generate_folder(clean_name, data)

    def _get_links(self) -> list[str]:
        """
        pending.
        """
        animes: list[str] = []
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception(f"{response.status_code}")
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", class_="link-title")
        for link in links[:5]:
            href = link.get("href")
            animes.append(href)
        return animes

    def _scrape_link(self, link: str) -> dict[str, str] | None:
        try:
            response = requests.get(link, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            data: dict[str, str] = {"url": link}

            for name, selector in self.elements.items():
                element = soup.select_one(selector)
                if name == "website" and element:
                    data[name] = (
                        str(element.get("href"))
                        if element and element.get("href")
                        else ""
                    )
                elif element:
                    data[name] = element.text.strip()

            # Extract the image
            image_tag = soup.find("meta", property="og:image")
            if image_tag and image_tag.get("content"):
                data["image"] = image_tag["content"]

            # Get each element from the dictionary
            title_eng: str = data.get("title_eng", "")
            title_jpn: str = data.get("title_jpn", "")
            title_kanji: str = (
                data.get("title_kanji", "").replace("Japanese: ", "").strip()
            )
            year: str = extract_year(data.get("year", ""))
            image: str = data.get("image", "")
            website: str = data.get("website", "")

            title: str = title_eng if title_eng else title_jpn
            title_jpn: str = title_jpn if title_jpn else title_eng

            logging.info(f"Processing: {title} ({year})")
            anime: dict[str, str] = {
                "title": title,
                "title_jpn": title_jpn,
                "title_kanji": title_kanji,
                "year": year,
                "image": image,
                "website": website,
            }
            return anime
        except Exception as e:
            logging.error(f"{link}: {e}")

    def _generate_folder(
        self,
        folder_name: str,
        anime_data: dict[str, str],
    ) -> None:
        """
        Generates a folder with given name inside directory.
        """
        folder_path: str = os.path.join(self.directory, folder_name)

        try:
            # Create the folder
            os.makedirs(folder_path, exist_ok=True)
            logging.info(f"Procesing {folder_path}...")

            # Save anime data as JSON
            json_path: str = os.path.join(folder_path, "info.json")
            with open(json_path, "w", encoding="utf-8") as json_file:
                json.dump(anime_data, json_file, ensure_ascii=False, indent=4)

            # Download the image
            if anime_data["image"]:
                image_data: bytes = requests.get(anime_data["image"]).content
                image_filename = "ref.jpg"
                image_path: str = os.path.join(folder_path, image_filename)
                with open(image_path, "wb") as image_file:
                    image_file.write(image_data)
            else:
                logging.error("No image found")

        except OSError as e:
            logging.error(f"{folder_path}: {e}")
        except Exception as e:
            logging.error(f"Error downloading image ({e})")
