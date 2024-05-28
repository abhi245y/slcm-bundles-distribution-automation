from typing import List
import json


def get_bundles_list(qp_code: str, csrftoken: str):
    bundle_list_script = f"""
return (async () => {{
  const response = await fetch("https://examerp.keralauniversity.ac.in/cd-unit/qpcode-wise-bundle-list", {{
    "headers": {{
      "accept": "application/json",
      "content-type": "application/json",
      "x-csrftoken": "{csrftoken}"
    }},
    "body": '{{"qp_code":"{qp_code}"}}',
    "method": "POST",
    "mode": "cors",
    "credentials": "include"
  }});
  const data = await response.json();
  return data;
}})();
"""
    return bundle_list_script


def get_campwise_bundle_list(qp_code: str):
    campwise_bundle_list_script = """
return (async () => {
  const response = await fetch("https://examerp.keralauniversity.ac.in/cd-unit/campwise-bundle-list?format=json", {
    "headers": {
       "accept": "application/json, text/javascript, */*; q=0.01",
      "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
      "x-csrftoken": ""
    },
    "body": "qp_code=%s",
    "method": "POST",
    "mode": "cors",
    "credentials": "include"
  });
  const data = await response.json();
  return data;
})();
"""
    return campwise_bundle_list_script % qp_code.replace(" ", "+")


def allocate_bundle(
    csrftoken: str, bundle_id_list: List[str], camp_id: int, subcamp_id: int
):
    bundle_allocation_script = f"""
return (async () => {{
    const response = await fetch("https://examerp.keralauniversity.ac.in/cd-unit/bundle-alocate-to-camp", {{
    "headers": {{
        "accept": "application/json",
       "content-type": "application/json",
      "x-csrftoken": "{csrftoken}"
    }},
   "body": '{{"bundle_id_list": {json.dumps(bundle_id_list)}, "camp_id": {camp_id}, "subcamp_id": {subcamp_id}}}',
    "method": "POST",
    "mode": "cors",
    "credentials": "include"
    }});
    const data = await response.json();
    return data;
  }})();
    """
    return bundle_allocation_script


def get_sub_camp_list(csrftoken: str, camp_id: int):
    sub_camp_list_script = f"""
return (async () => {{
    const response = await fetch("https://examerp.keralauniversity.ac.in/cd-unit/sub-camp-list-allocation?format=json", {{
    "headers": {{
        "accept": "*/*",
       "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
      "x-csrftoken": "{csrftoken}"
    }},
   "body": "campid={camp_id}",
    "method": "POST",
    "mode": "cors",
    "credentials": "include"
    }});
    const data = await response.json();
    return data;
  }})();
    """
    return sub_camp_list_script


def get_exam_code_id(csrftoken: str, exam_date: str):
    date_wise_exam_code_list = f"""
  return (async () => {{
    const response = await fetch("https://examerp.keralauniversity.ac.in/cd-unit/datewise-exam-view", {{
    "headers": {{
        "accept": "application/json",
       "Content-Type": "application/json",
      "x-csrftoken": "{csrftoken}"
    }},
    "referrer": "https://examerp.keralauniversity.ac.in/cd-unit/all-bundle-list",
   "body": '{{"exam_date":"{exam_date}"}}',
    "method": "POST",
    "mode": "cors",
    "credentials": "include"
    }});
    const data = await response.json();
    return data;
  }})();
    """
    return date_wise_exam_code_list


def get_bundle_list(csrftoken: str, exam_date: str, exam_id: str) -> str:
    date_wise_exam_code_list = f"""
return (async () => {{
    const response = await fetch("https://examerp.keralauniversity.ac.in/cd-unit/examwise-bundle-list", {{
        "headers": {{
            "accept": "application/json",
            "Content-Type": "application/json",
            "x-csrftoken": "{csrftoken}"
        }},
        "referrer": "https://examerp.keralauniversity.ac.in/cd-unit/all-bundle-list",
        "body": '{{"exam_id":"{exam_id}", "date": "{exam_date}"}}',
        "method": "POST",
        "mode": "cors",
        "credentials": "include"
    }});
    const data = await response.json();
    return data;
}})();  
    """
    return date_wise_exam_code_list


def bundle_recive(csrftoken: str, bundleid: int):
    bundle_recive = f"""
return (async () => {{
    const response = await fetch("https://examerp.keralauniversity.ac.in/cd-unit/decrypt-bundle-recive?format=json", {{
    "headers": {{
        "accept": "*/*",
       "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
      "x-csrftoken": "{csrftoken}"
    }},
    "referrer": "https://examerp.keralauniversity.ac.in/cd-unit/bundle-recive",
   "body": "bundleid={bundleid.replace(" ", "+")}&bcode=CA",
    "method": "POST",
    "mode": "cors",
    "credentials": "include"
    }});
    const data = await response.json();
    return data;
  }})();
    """
    return bundle_recive
