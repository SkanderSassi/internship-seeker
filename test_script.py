from config import browser


TEST_URL = "https://recruter.tn/offres-de-stages-pfe-2021-a-hikma-pharmaceuticals/"
BASE_XPATH = "//*/section[@class='post-content']"
browser.get(TEST_URL)
div_elements = browser.find_elements_by_xpath(f"{BASE_XPATH}/div")
p_elements = browser.find_elements_by_xpath(f"{BASE_XPATH}/p")
print(len(div_elements) + len(p_elements))
final_text = []
for element in div_elements + p_elements:
    if element.get_attribute("class") == "su-button-center":
        break
    print(element.text)
    final_text.append(element.text)
print(' '.join(final_text))