import json
import os


script_folder = os.path.dirname(os.path.abspath(__file__))
input_file_two_products = os.path.join(script_folder, '2025.10.06_00.04.json')
print('input_file_two_products:', input_file_two_products)

# Load all test results
with open(input_file_two_products) as f:
    data = json.load(f)

products = []
threads = []
block_sizes = []
for d in data:
    product_vendor = d["product_vendor"]
    product_name = d["product_name"]
    product_version = d["product_version"]
    product_protocol = d["product_test_protocol"]
    product_label = f'{product_vendor} {product_name} {product_version}'
    if product_label not in products:
        products.append(product_label)

    block_size = d["block_size"]
    if block_size not in block_sizes:
        block_sizes.append(block_size)

    thread = d["threads"]
    if thread not in threads:
        threads.append(thread)

four_corners = [
    "Sequential Write",
    "Sequential Read",
    "Random Write",
    "Random Read"
]

metrics = {
    "iops": "IOPS",
    "mibs": "Throughput (MiB/s)",
    "lat": "Latency (µs)"
}

compare_product_data = []

for product_key in products:
    for test_name in four_corners:
        for block in block_sizes:
            iops_list = []
            mibs_list = []
            lats_list = []
            for d in data:
                test_name_value = f'{d["test_mode"]} {d["operation"]}'
                product_vendor = d["product_vendor"]
                product_name = d["product_name"]
                product_version = d["product_version"]
                product_protocol = d["product_test_protocol"]
                product_label = f'{product_vendor} {product_name} {product_version}'
                if test_name == test_name_value and block == d["block_size"] and product_key == product_label:

                    iops = round(d["iops"])
                    mibs = round(d["mibs"])
                    lats = round(d["lat"])
                    iops_list.append(iops)
                    mibs_list.append(mibs)
                    lats_list.append(lats)

            if block == 4096:
                block_size = "4K"
            elif block == 32768:
                block_size = "32K"
            elif block == 65536:
                block_size = "64K"
            else:
                block_size = f"{block}B"

            test_at_block_size = {
                "product_key": product_key,
                "test_name": f'{test_name} {block_size}',
                "block_size": block_size,
                "threads": threads,
                "iops": iops_list,
                "mibs": mibs_list,
                "lats": lats_list
            }
            compare_product_data.append(test_at_block_size)

for info in compare_product_data:
    if info["block_size"] == "4K":
        print(info)

ppd = json.dumps(compare_product_data)
print(ppd)