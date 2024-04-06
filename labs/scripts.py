from typing import List

def get_bundles_list(qp_code: str, csrftoken: str):
    bundle_list_script = f'''
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
'''
    return bundle_list_script

def get_campwise_bundle_list(qp_code:str):
    campwise_bundle_list_script = '''
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
'''
    return campwise_bundle_list_script % qp_code.replace(" ","+")


def allocate_bundle(csrftoken:str ,bundle_id_list:List[str], camp_id:int, subcamp_id:int):
    bundle_allocation_script=f'''
return (async () => {{
  const response = await fetch("https://examerp.keralauniversity.ac.in/cd-unit/bundle-alocate-to-camp", {{
    "headers": {{
        "accept": "application/json",
       "content-type": "application/json",
      "x-csrftoken": {csrftoken}
    }},
   "body": "{{\"bundle_id_list\":{bundle_id_list},\"camp_id\":3,\"subcamp_id\":215}}",
    "method": "POST",
    "mode": "cors",
    "credentials": "include"
  }});
  const data = await response.json();
  return data;
}})();
    '''
    return bundle_allocation_script
