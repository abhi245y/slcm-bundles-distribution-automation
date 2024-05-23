from selenium import webdriver

# import yaml
import json

# import requests
# import time
# import pprint
from selenium.webdriver.chrome.options import Options

import scripts

options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

driver.get("https://examerp.keralauniversity.ac.in/")

with open("./configs/cookies.json", "r") as f:
    cookies = json.load(f)

for cookie in cookies:
    driver.add_cookie(cookie)


driver.get("https://examerp.keralauniversity.ac.in/user/dashboard")


# bundle_list = []
# for qp in ['S 3134','S 3135','S 3136', 'S 3137', 'S 3138']:
#   try:
#     res = driver.execute_script (scripts.get_bundles_list(qp,cfrtoken))
#     bundle_list.append(res['data']['bundleList'][0])
#   except:
#     print(res)


# save_file = open("savedata_2.json", "w")
# json.dump(bundle_list, save_file, indent = 6)
# save_file.close()

cfrtoken = ""
# print(
#     driver.execute_script(scripts.get_sub_camp_list(cfrtoken, 3))["data"]["subcamplist"]
# )
# print(
#     driver.execute_script(
#         scripts.allocate_bundle(
#             csrftoken="",
#             bundle_id_list=[
#                 "40324",
#                 "40472",
#                 "40684",
#                 "40812",
#             ],
#             camp_id=3,
#             subcamp_id=236,
#         )
#     )
# )

# print(
#     driver.execute_script(
#         scripts.get_bundles_list(
#             csrftoken=driver.get_cookies()[0]["value"],
#             qp_code="S 6924",
#         )
#     )
# )


def auto_qp_series_generator(
    # series: str, range_start: int, range_end: int, exam_name: str
) -> None:
    """
    Generates a series of QP codes based on user input and processes them.

    Args:
        series (str): Series identifier (e.g., 'P', 'Q', 'R').
        range_start (int): Starting range of QP codes.
        range_end (int): Ending range of QP codes.
        exam_name (str): Name of the exam.
    """
    # qp_codes = [series + " " + str(i) for i in range(range_start, range_end + 1)]


auto_qp_series_generator()

# with open('savedata.json' , 'r') as saved:
#     saved_json = json.load(saved)

# def get_selected_keys(data, keys):
#     selected_data = {key: data[key] for key in keys}
#     # output = ", ".join([f"{key}: {value}" for key, value in selected_data.items()])
#     return selected_data

# import pandas as pd

# for data in saved_json['data']['bundleList'][0]:
#     print(data)
#     print(pd.DataFrame([get_selected_keys(data, ['bundleCode', 'camp', 'district', 'status', 'totalCount'])]))
#     break
