from tfox.buyer_seller import process_classified_ad
from pprint import pprint



if __name__ == "__main__":
    sample_text = """
        ქუთაისში იყიდება კორეული სახურავი 0.5მმ ახალი 3 ცალი 7.30 სმ იანები 22 კვ. მეტრი ასევე წყლის 4 ცალი ტრუბა, ერთ ნახევარი 4 მეტრიანი ღარი და 180 ცალი შურუფი! ფასი: კორეული ჟეშტი - 20 ლარი კვადრატი წყლის ტრუბები-80 ლარი ღარი-40 ლარი ტელ: 592016858 ან 598352864
    """
    result = process_classified_ad(sample_text)
    pprint(result)
