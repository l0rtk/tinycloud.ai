from tfox.buyer_seller import process_classified_ad
from services.mongodb import MongoDBService
from dotenv import load_dotenv
from pprint import pprint
import os

load_dotenv()

mongodb = MongoDBService(
    connection_uri=os.getenv("MONGODB_CONNECTION_URI"),
    database_name=os.getenv("MONGODB_DATABASE_NAME")
)   


docs = mongodb.find_many("facebook_posts", { "analyzed": False })
total_docs = len(list(docs))  # Get total count
print(f"Found {total_docs} documents to analyze")

for i, doc in enumerate(docs, 1):
    print(f"Processing document {i}/{total_docs}...")
    analysis = process_classified_ad(doc["text"])
    
    # Validate analysis structure
    if not isinstance(analysis, dict) or not all(key in analysis for key in ["translated_text", "status"]):
        print(f"Warning: Invalid analysis structure for document {i}. Skipping update.")
        continue
        
    doc["analysis"] = analysis
    doc["analyzed"] = True
    mongodb.update_one("facebook_posts", { "_id": doc["_id"] }, doc)
    print(f"Completed {i}/{total_docs} ({(i/total_docs)*100:.1f}%)")

print("Analysis complete!")



# if __name__ == "__main__":
#     sample_text = """
#         ქუთაისში იყიდება კორეული სახურავი 0.5მმ ახალი 3 ცალი 7.30 სმ იანები 22 კვ. მეტრი ასევე წყლის 4 ცალი ტრუბა, ერთ ნახევარი 4 მეტრიანი ღარი და 180 ცალი შურუფი! ფასი: კორეული ჟეშტი - 20 ლარი კვადრატი წყლის ტრუბები-80 ლარი ღარი-40 ლარი ტელ: 592016858 ან 598352864
#     """
#     result = process_classified_ad(sample_text)
#     pprint(result)
