class MegaMarkerParser:
    @classmethod
    def start_parse(cls, url, last_price, driver):
        driver.get(url=url)
        price, bonuses = cls.get_price_and_bonuses(driver)

    @classmethod
    def get_price_and_bonuses(cls):
        pass

    @classmethod
    def check_prices(cls):
        pass
    # driver = webdriver.Chrome()
    #
    # try:
    #     prices_and_urls = []
    #     for page_number in range(1, 50):
    #         url = f'https://megamarket.ru/catalog/page-{page_number}/?q=iphone%2015%20128'
    #         driver.get(url=url)
    #
    #         all_items = driver.find_elements(By.CLASS_NAME, 'item-info')
    #         items = [item for item in all_items if 'item-info__bottom' not in item.get_attribute("class")]
    #
    #         for item in items:
    #             price = get_item_price(item)
    #             bonus = get_item_bonus(item)
    #             item_url = get_item_url(item)
    #             finally_price = Calculator.count_finally_price(price, bonus, True)
    #             prices_and_urls.append((finally_price, item_url))
    #
    # except Exception as ex:
    #     logger.warning(ex)
    #
    # finally:
    #     prices_and_urls.sort(key=lambda x: x[0])
    #     logger.debug(prices_and_urls)
    #     driver.close()
    #     driver.quit()
    #

    def for_personal():
        driver = webdriver.Chrome()

        try:
            prices_and_urls = []
            for page_number in range(1, 50):
                url = f'https://megamarket.ru/catalog/page-{page_number}/?q=iphone%2015%20128'
                driver.get(url=url)

                all_items = driver.find_elements(By.CLASS_NAME, 'item-info')
                items = [item for item in all_items if 'item-info__bottom' not in item.get_attribute("class")]

                for item in items:
                    price = get_item_price(item)
                    bonus = get_item_bonus(item)
                    item_url = get_item_url(item)
                    finally_price = Calculator.count_finally_price(price, bonus, True)
                    prices_and_urls.append((finally_price, item_url))

        except Exception as ex:
            logger.warning(ex)

        finally:
            prices_and_urls.sort(key=lambda x: x[0])
            logger.debug(prices_and_urls)
            driver.close()
            driver.quit()

    def get_item_price(item):
        price_element = item.find_element(By.CLASS_NAME, 'item-price').find_element(By.TAG_NAME, 'span')
        element_string_price = price_element.get_attribute("innerText")
        return parse_price_string(element_string_price)

    def get_item_bonus(item):
        bonus_element = item.find_elements(By.CLASS_NAME, 'money-bonus_loyalty')
        if bonus_element:
            bonus_amount = bonus_element[0].find_element(By.CLASS_NAME, 'bonus-amount')
            element_string_bonus = bonus_amount.get_attribute("innerText")
            elements_int_bonuses = parse_price_string(element_string_bonus)
        else:
            elements_int_bonuses = 0
        return elements_int_bonuses

    def get_item_url(item):
        element_url = item.find_element(By.CLASS_NAME, 'ddl_product_link')
        element_string_url = element_url.get_attribute("href")
        return element_string_url

    def parse_price_string(price_string):
        price_string = price_string.replace('\xa0', ' ')
        price_string = ''.join(c for c in price_string if c.isdigit() or c.isspace())
        price = int(price_string.replace(' ', ''))
        return price

    class Calculator:
        @classmethod
        def count_finally_price(cls, price, bonuses, coupon=None):
            if coupon:
                bonuses_percent = cls._count_percent_of_prices_bonuses(price, bonuses)
                price = Coupon.get_price_with_coupon_ikra(price)
                bonuses = bonuses_percent * price

            return round(price - bonuses, 0)

        @classmethod
        def _count_percent_of_prices_bonuses(cls, price, bonuses):
            return bonuses / price

    class Coupon:
        @staticmethod
        def get_price_with_coupon_ikra(price):
            if price < 11000:
                return price
            elif price < 30000:
                return price - 2000
            elif price < 50000:
                return price - 5000
            elif price < 7000:
                return price - 9000
            return price - 12000




