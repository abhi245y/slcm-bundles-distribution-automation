import os
import pathlib
import time
from typing import List
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
import yaml
import json
import nopecha
import requests
import base64
import urllib3
from labs import scripts
import logging

urllib3.disable_warnings(urllib3.exceptions.HTTPWarning)

driver = webdriver.Chrome()

driver.get("https://examerp.keralauniversity.ac.in/")

with open("./configs/configurations.yaml", "r") as file:
    configurations = yaml.safe_load(file)

mergedOutputFolderPath: str = configurations["mergedOutputFolderPath"]
undallocatedBundlesFolder: str = configurations["undallocatedBundlesFolder"]
cookies_path = "./configs/cookies.json"

# Configure logging to print to the console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def fetch_csrftoken():
    if driver.get_cookies()[0]["name"] == "csrftoken":
        return driver.get_cookies()[0]["value"]
    else:
        return driver.get_cookies()[1]["value"]


def log_message(message, level=logging.INFO):
    if level == logging.INFO:
        logging.info(message)
    elif level == logging.WARNING:
        logging.warning(message)
    elif level == logging.ERROR:
        logging.error(message)


def apply_styles(worksheet, df, workbook):
    align_format = workbook.add_format(
        {"font_size": 11, "align": "center", "valign": "vcenter", "text_wrap": True}
    )

    worksheet.set_column("A:A", 42 / 7, align_format)  # Sl.No.
    worksheet.set_column("B:B", 105 / 7, align_format)  # Bundle Code
    worksheet.set_column("C:C", 62 / 7, align_format)  # AS Count
    worksheet.set_column("D:D", 171 / 7, align_format)  # Course Name
    worksheet.set_column("E:E", 140 / 7, align_format)  # District
    worksheet.set_column("F:F", 67 / 7, align_format)  # Camp
    worksheet.set_column("G:G", 73 / 7, align_format)  # Status

    worksheet.set_default_row(39)

    worksheet.set_margins(left=0.25, right=0.25, top=0.6, bottom=0.3)

    header_format = workbook.add_format(
        {
            "font_size": 15,
            "bold": True,
            "underline": True,
            "align": "center",
            "valign": "vcenter",
        }
    )
    worksheet.set_header(
        '&C&"Arial"&B{}&"'.format(configurations["examName"]),
        {"header_header_spacing": 0.3, "font": header_format},
    )

    # Apply alignment and wrap text to data cells
    for row_num, row_data in enumerate(df.values):
        for col_num, cell_value in enumerate(row_data):
            worksheet.write(row_num + 1, col_num, str(cell_value), align_format)

    worksheet.repeat_rows(0)

    (max_row, max_col) = df.shape
    column_settings = [{"header": column} for column in df.columns]
    worksheet.add_table(0, 0, max_row, max_col - 1, {"columns": column_settings})


def auto_login(capcha_link: str):
    """
    Auto login to the website when the cookies are expired
    Args:
        capcha_link (str): URL of the capcha image
    """
    log_message("Fetching captcha solution...", logging.INFO)
    nopecha.api_key = configurations["nopecha"]

    response = requests.get(capcha_link, verify=False)
    image_data = response.content
    base64_image = base64.b64encode(image_data).decode("utf-8")

    cpacha_text = nopecha.Recognition.solve(
        type="textcaptcha",
        image_data=[base64_image],
    )

    driver.find_element(By.ID, "username").send_keys(configurations["username"])
    driver.find_element(By.ID, "password").send_keys(configurations["password"])

    capcha_filed = driver.find_element(By.ID, "id_captcha_1")
    capcha_filed.clear()
    capcha_filed.send_keys(cpacha_text[0])
    driver.find_element(By.CLASS_NAME, "btn-primary").click()


def add_cookies(cookies: List[dict]) -> None:
    """
    Adds cookies to the driver for session management.

    Args:
        cookies (List[dict]): List of cookie dictionaries.
    """
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("https://examerp.keralauniversity.ac.in/cd-unit/qpcode-wise-bundle-list")


def style_merged_table(merged_data, output_file):
    df = merged_data
    writer = pd.ExcelWriter(output_file, engine="xlsxwriter")
    workbook = writer.book
    df.drop(df.columns[[0]], axis=1, inplace=True)

    for camp in df["Camp"].unique():
        try:
            new_df = df[df["Camp"] == camp]
            new_df = new_df.reset_index()
            new_df = new_df.rename(columns={"index": "Sl.No"})
            new_df["Sl.No"] = new_df.index + 1
            new_df.to_excel(
                writer, sheet_name=camp, index=False, startrow=1, header=False
            )

            worksheet = writer.sheets[camp]
            apply_styles(worksheet, new_df, workbook)
        except Exception:
            new_df = df[df["Camp"].isnull()]
            new_df = new_df.reset_index()
            new_df = new_df.rename(columns={"index": "Sl.No"})
            new_df["Sl.No"] = new_df.index + 1
            new_df.to_excel(
                writer, sheet_name="Generated", index=False, startrow=1, header=False
            )

            worksheet = writer.sheets["Generated"]
            apply_styles(worksheet, new_df, workbook)
    writer.close()


def merge_excel_files(folder_path: str, output_file: str, exam_name: str) -> None:
    """
    Merges multiple Excel files in a given folder into one output file.

    Args:
        folder_path (str): Path to the folder containing Excel files.
        output_file (str): Path to the output Excel file.
        exam_name (str): Name of the exam, used to filter the files.
    """
    merged_data = pd.DataFrame()
    for file in os.listdir(folder_path):
        if file.startswith(exam_name) and file.endswith(".xlsx"):
            file_path = os.path.join(folder_path, file)
            data = pd.read_excel(file_path)
            merged_data = pd.concat([merged_data, data], ignore_index=True)
    # merged_data.to_excel(output_file, index=False)
    merged_data.sort_values(by="Bundle Code", ascending=True, inplace=True)

    style_merged_table(merged_data, output_file)
    log_message(f"Merged data saved to {output_file}", logging.INFO)


def check_qp(table: BeautifulSoup, target_qp: str) -> str:
    """
    Checks if the scraped QP code matches the target QP code.

    Args:
        table (BeautifulSoup): The parsed HTML table.
        target_qp (str): Target QP code to match.

    Returns:
        str: Result of the check ('success', 'try again', or 'empty').
    """
    data_tables_empty_td = (
        table.find("tr", class_="odd").find("td", class_="dataTables_empty")
        if table.find("tr", class_="odd")
        else None
    )
    if data_tables_empty_td is None:
        qp_in_table = table.find("tr", class_="odd").find_all("td")[2].text.strip()[:6]
        return "success" if qp_in_table == target_qp else "try again"
    else:
        return "empty"


def grab_bundle_details_using_script(
    qp_codes: List[str],
    path: str,
    exam_name: str,
) -> None:
    headers = [
        "Sl.No.",
        "Bundle Code",
        "AS Count",
        "Course Name",
        "District",
        "Camp",
        "Status",
    ]

    for qp_code in qp_codes:
        data = []
        log_message(f"Fetching deatils of: {qp_code}", logging.INFO)

        res = driver.execute_script(
            scripts.get_bundles_list(
                csrftoken=fetch_csrftoken(),
                qp_code=qp_code,
            )
        )
        try:
            if res["message"] == "success":
                log_message(f"Saving Details of: {qp_code}", logging.INFO)
                for bundle_details in res["data"]["bundleList"][0]:
                    status = bundle_details["status"]
                    if bundle_details["status"] == "DELIVERED UNIVERSITY":
                        status = "Allocated To Camp"
                    data.append(
                        [
                            "",
                            bundle_details["bundleCode"],
                            bundle_details["totalCount"],
                            bundle_details["courseName"],
                            bundle_details["district"],
                            bundle_details["camp"],
                            status,
                        ]
                    )
                # print(data)
                df = pd.DataFrame(data, columns=headers)
                file_name = exam_name + " " + qp_code
                final_file_name = str(path) + str(file_name)
                df.to_excel(final_file_name + ".xlsx", index=False)
            else:
                log_message(res["message"], logging.WARNING)
        except Exception as e:
            log_message(f"Error fetched result {res}| Error: {e}", logging.ERROR)

    output_file = mergedOutputFolderPath + exam_name + "_combined.xlsx"
    merge_excel_files(path, output_file, exam_name)


def grab_bundle_codes_from_source(
    turn: int, data: List[List[str]], file_name: str, qp_code: str, folder_path: str
) -> None:
    """
    Scrapes and converts an HTML table with bundle details to an Excel file.
    Each file is saved per QP code and all files are merged into one Excel file.

    Args:
        turn (int): Indicates the iteration number.
        data (List[List[str]]): Data to be written to the file.
        file_name (str): Name of the file to be created.
        qp_code (str): QP code for filtering.
        folder_path (str): Path to the folder where the file will be saved.
    """
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    table = soup.find("table", {"id": "style-2"})
    check_res = check_qp(table, qp_code)
    log_message(f"Checking QP: {check_res}", logging.INFO)
    if check_res == "success":
        if turn == 1:
            data.clear()
            for row in table.find_all("thead"):
                row_data = [
                    cell.get_text(strip=True)
                    for cell in row.find_all("th")
                    if cell.get_text(strip=True) != "c"
                ]
                if row_data:
                    data.append(row_data)
        for row in table.find_all("tr"):
            row_data = [
                cell.get_text(strip=True)
                for cell in row.find_all("td")
                if cell.get_text(strip=True) != "c"
            ]
            if row_data:
                data.append(row_data)
        log_message(f"Grabbed: {data[-1]}", logging.INFO)
        df = pd.DataFrame(data[1:], columns=data[0])
        final_file_name = str(folder_path) + str(file_name)
        df.to_excel(final_file_name + ".xlsx", index=False)
    elif check_res == "empty":
        pass


def qp_code_details_grabber(qp_codes: List[str], path: str, exam_name: str) -> None:
    """
    Submits each QP code to the webpage and grabs the HTML code.

    Args:
        qp_codes (List[str]): List of QP codes.
        path (str): Path to save the output files.
        exam_name (str): Name of the exam.
    """
    for i, qp_code in enumerate(qp_codes, start=1):
        log_message(f"Grabbing: {qp_code}", logging.INFO)
        qpCodeInputTag = driver.find_element(By.ID, "qp_code")
        driver.execute_script('document.getElementById("qp_code").value = ""')
        time.sleep(1)
        qpCodeInputTag.send_keys(qp_code)
        submit_button = driver.find_element(By.ID, "submit_button")
        submit_button.click()
        wait = WebDriverWait(driver, 100)
        try:
            wait.until_not(
                EC.presence_of_element_located((By.CLASS_NAME, "blockOverlay"))
            )
            select_element = Select(driver.find_element(By.NAME, "style-2_length"))
            select_element.select_by_value("1000")
            try:
                grab_bundle_codes_from_source(
                    turn=1,
                    data=[],
                    file_name=exam_name + " " + qp_code,
                    qp_code=qp_code,
                    folder_path=path,
                )
                time.sleep(2)
            except Exception as e:
                log_message(f"Error in {qp_code}. Skipping. Error: {e}", logging.ERROR)
                pass
        except TimeoutException:
            log_message("Error Reloading Page", logging.ERROR)
            driver.refresh()
    output_file = mergedOutputFolderPath + exam_name + "_combined.xlsx"
    merge_excel_files(path, output_file, exam_name)


def auto_qp_series_generator(
    series: str, range_start: int, range_end: int, exam_name: str
) -> None:
    """
    Generates a series of QP codes based on user input and processes them.

    Args:
        series (str): Series identifier (e.g., 'P', 'Q', 'R').
        range_start (int): Starting range of QP codes.
        range_end (int): Ending range of QP codes.
        exam_name (str): Name of the exam.
    """
    qp_codes = [series + " " + str(i) for i in range(range_start, range_end + 1)]
    pathlib.Path(mergedOutputFolderPath).mkdir(parents=True, exist_ok=True)
    path = pathlib.Path(undallocatedBundlesFolder + exam_name)
    path.mkdir(parents=True, exist_ok=True)
    # qp_code_details_grabber(qp_codes, str(path) + "/", exam_name)
    try:
        grab_bundle_details_using_script(
            qp_codes=qp_codes,
            path=str(path) + "/",
            exam_name=exam_name,
        )
    except Exception as e:
        log_message(f"Error execeuting Script: {e}", logging.ERROR)


def create_cookies() -> None:
    with open(cookies_path, "w") as f:
        f.write(json.dumps(driver.get_cookies(), indent=4))
    log_message("Cookies captured. Redirecting...", logging.INFO)
    driver.get("https://examerp.keralauniversity.ac.in/cd-unit/qpcode-wise-bundle-list")


def check_cookies() -> bool:
    """
    Checks if the existing cookies are valid, and if not, attempts auto-login.
    Returns True if cookies are valid or auto-login succeeds, False otherwise.
    """
    log_message("Checking Cookies", logging.INFO)

    if not os.path.exists(cookies_path):
        log_message("No cookies file found", logging.WARNING)
        return attempt_auto_login()

    try:
        with open(cookies_path, "r") as f:
            cookies = json.load(f)

        if cookies[0]["expiry"] <= int(time.time()):
            log_message("Cookies have expired", logging.WARNING)
            return attempt_auto_login()

        log_message("Cookies are valid. Redirecting...", logging.INFO)
        add_cookies(cookies)
        return True, ""

    except Exception as e:
        log_message(f"Error reading cookies: {e}", logging.ERROR)
        return attempt_auto_login()


def attempt_auto_login() -> bool:
    """
    Attempts to perform auto-login.
    Returns True if successful, False otherwise.
    """
    try:
        log_message("Attempting auto-login", logging.INFO)
        captcha_link = driver.find_element(By.CLASS_NAME, "captcha").get_attribute(
            "src"
        )
        auto_login(captcha_link)
        return True, ""
    except Exception as e:
        log_message(f"Auto-login failed: {e}", logging.ERROR)
        log_message("Please log in manually", logging.WARNING)
        return False, captcha_link


def manual_login(username, password, capcha_text):
    driver.get("https://examerp.keralauniversity.ac.in/")
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)

    capcha_filed = driver.find_element(By.ID, "id_captcha_1")
    capcha_filed.clear()
    capcha_filed.send_keys(capcha_text)
    driver.find_element(By.CLASS_NAME, "btn-primary").click()


def custom_qp_range(qp_codes: List[str], exam_name: str) -> None:
    """
    Uses the custom series of QP codes given by the user.

    Args:
        qp_codes (List): Custom List of QP Codes
        exam_name (str): Name of the exam.
    """

    pathlib.Path(mergedOutputFolderPath).mkdir(parents=True, exist_ok=True)
    path = pathlib.Path(undallocatedBundlesFolder + exam_name)
    path.mkdir(parents=True, exist_ok=True)
    # qp_code_details_grabber(qp_codes, str(path) + "/", exam_name)

    try:
        grab_bundle_details_using_script(
            qp_codes=qp_codes,
            path=str(path) + "/",
            exam_name=exam_name,
        )
    except Exception as e:
        log_message(
            f"Error execeuting Script in fun custom_qp_range: {e}", logging.ERROR
        )


# if __name__ == "__main__":
#     # check_cookies()
#     # if configurations["customQPRangeMode"]:
#     #     log_message("Running Mode: Custom QP Range", logging.INFO)
#     #     custom_qp_range(configurations["customQPRange"], configurations["examName"])
#     #     pass
#     # else:
#     #     log_message("Running Mode: Auto Gen QP Range", logging.INFO)
#     #     auto_qp_series_generator(
#     #         configurations["qpSeries"],
#     #         int(configurations["qpStartRange"]),
#     #         int(configurations["qpEndRange"]),
#     #         configurations["examName"],
#     #     )
#     driver.quit()
