# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MyfirstprojectPipeline:
    def process_item(self, item, spider):
        adapter_obj = ItemAdapter(item)

        # removing white spaces from all the fields except the description
        field_names = adapter_obj.field_names()
        for field_name in field_names:
            if field_name != "description":
                print(field_name)
                field_value = adapter_obj.get(field_name)
                adapter_obj[field_name] = field_value.strip()

        
        # turning category and product type to lower case
        required_fields = ["category","product_type"]
        for field_name in required_fields:
            field_value = adapter_obj.get(field_name)
            adapter_obj[field_name] = field_value.lower()

        # removing £ sign from price and converting to float
        required_fields = ["price","tax","price_excl_tax","price_incl_tax"]
        for field_name in required_fields:
            field_value = adapter_obj.get(field_name)
            field_value = field_value.replace("£","")
            field_value = float(field_value)

            adapter_obj[field_name] = field_value

        # converting no of available books from "In stock (19 available)" into integer
        field_value = adapter_obj.get("availability")
        splitted_list = field_value.split("(")
        if len(splitted_list)<2:
            adapter_obj["availability"] = 0
        else:
            field_value = splitted_list[1].split(" ")
            adapter_obj["availability"] = int(field_value[0])
        

        # converting no of reviews to int
        field_value = adapter_obj.get("num_reviews")
        adapter_obj["num_reviews"] = int(field_value)

        # converting stars to integer
        field_value = adapter_obj.get("stars")
        field_value = field_value.split(" ")[0].lower()
        
        if field_value == "zero":
            adapter_obj["stars"] = 0
        elif field_value == "one":
            adapter_obj["stars"] = 1
        elif field_value == "two":
            adapter_obj["stars"] = 2
        elif field_value == "three":
            adapter_obj["stars"] = 3
        elif field_value == "four":
            adapter_obj["stars"] = 4
        elif field_value == "five":
            adapter_obj["stars"] = 5



        return item
