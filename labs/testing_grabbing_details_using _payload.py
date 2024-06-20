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

csrftoken = driver.get_cookies()[0]["value"]


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
#             csrftoken=csrftoken,
#             qp_code="S 6830",
#         )
#     )
# )

# bundle_details = driver.execute_script(
#     scripts.bundle_recive(
#         csrftoken=csrftoken,
#         bundleid="S 68300002",
#     )
# )["data"]["bundleLists"][0]

# print(bundle_details["dateofexamination"])
# exam_code_id_list = driver.execute_script(
#     scripts.get_exam_code_id(
#         csrftoken=csrftoken,
#         exam_date=bundle_details["dateofexamination"],
#     )
# )

# print(exam_code_id_list)
# for exam_code_list in exam_code_id_list["data"]["examList"]:
#     if exam_code_list["examCode"] == bundle_details["examinationcode"]:
#         print(
#             driver.get_exam_code_id(
#                 scripts.get_bundle_list(
#                     csrftoken=csrftoken,
#                     exam_date=bundle_details["dateofexamination"],
#                     exam_id=exam_code_list["examId"],
#                 )
#             )
#         )
#         break

series = "T"
range_start = 5069
range_end = 5081
# qp_codes = [series + " " + str(i) for i in range(range_start, range_end + 1)]
qp_codes = [
    "T 5044",
    "T 5045",
    "T 5046",
    "T 5047",
    "T 5059",
    "T 5063",
    "T 5064",
    "T 5065",
    "T 5066",
]
camp_id = 3
sub_camp_name = "S6-New Gen-UG April 2024 (TVPM)"

bundle_ids = []
for qp_code in qp_codes:
    res = driver.execute_script(
        scripts.get_bundles_list(
            csrftoken=csrftoken,
            qp_code=qp_code,
        )
    )
    if res["message"] == "success":
        for bundle_details in res["data"]["bundleList"][0]:
            if bundle_details["status"] == "COLLECTED":
                bundle_ids.append(bundle_details["id"])

        # bundle_ids.append(
        #     bundle_details["id"] for bundle_details in res["data"]["bundleList"][0]
        # )

sub_camp_list = driver.execute_script(
    scripts.get_sub_camp_list(csrftoken=csrftoken, camp_id=camp_id)
)
sub_camp_id = ""

if sub_camp_list["message"] == "Successfully fetched the details":
    for sub_camps in sub_camp_list["data"]["subcamplist"]:
        if sub_camps["name"] == sub_camp_name:
            sub_camp_id = sub_camps["id"]
            break
else:
    print(sub_camp_list)

print(sub_camp_id)
print(
    driver.execute_script(
        scripts.allocate_bundle(
            csrftoken=csrftoken,
            bundle_id_list=bundle_ids,
            camp_id=camp_id,
            subcamp_id=sub_camp_id,
        )
    )
)

driver.quit()

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
