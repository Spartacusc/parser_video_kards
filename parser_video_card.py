from config import DRIVER_PATH, URL
from selenium import webdriver
from db import find_all_search, add_video_card


class ParseVideoCard:

    def __init__(self, url, bot=None):
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        self.driver.minimize_window()
        self.url = url
        self.bot = bot

    def __del__(self):
        self.driver.close()

    async def parse(self):
        search_models = find_all_search()

        for page in range(1, 10):
            print(self.url.format(page))
            self.driver.get(self.url.format(page))
            items = len(self.driver.find_elements_by_class_name("catalog-products view-simple"))
            for item in range(items):
                cards = self.driver.find_elements_by_class_name("catalog-product ui-button-widget")
                for card in cards:
                    product_item = card.find_element_by_class_name("catalog-product__name ui-link ui-link_black")
                    card_title = product_item.text
                    card_href = product_item.get_attribute("href")
                    for search_model in search_models:
                        if card_title.find(search_model.title) >= 0:
                            await add_video_card(card_title, card_href, search_model.chat_id, self.bot)
