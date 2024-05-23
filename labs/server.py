from flask import Flask, jsonify, request
import os
import pandas as pd
import colorama
import logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)
# log.disabled = True

app = Flask(__name__)
# app.config = {
#      "DEBUG": True,
#      "TEMPLATES_AUTO_RELOAD": True,
#      "CONTENT_SECURITY_POLICY": "default-src 'self' https://0.0.0.0:443"
# }

import json

xlFIleName = 'Second Semester PG November 2023 Camp Distribution QP Code '
folderName = '/Second Semester PG November 2023/'

def getBundleCodes(qpCode, targetCamp):
    folder_path = "./Outputs/Generated_Distributions/"+folderName
    # print(qpCode)

    bundleCodesArray = []
    print(folder_path)
    print(xlFIleName)
    for filename in os.listdir(folder_path):
        if filename.startswith(xlFIleName) and filename.endswith(str(qpCode)+'.xlsx'):
            input_file = os.path.join(folder_path, filename)
            
            # Read the processed Excel file as DataFrame
            df = pd.read_excel(input_file)
            
            # Convert each row to a dictionary and append to the list
            for _, row in df.iterrows():
                # data_dict = {
                #     'Qp Code': row['Bundle Code'][2:6],
                #     'Bundle Code': row['Bundle Code'],
                #     'AS Count': row['AS Count'],
                #     'District': row['District'],
                #     'Status': row['Status']
                # }
                if row['Camp'] == targetCamp:
                    bundleCodesArray.append(row['Bundle Code'])
                
    
    return bundleCodesArray

def save_to_json_file(filename, data, bundle_id):
    if os.path.exists(filename):
        # Read the existing data from the file
        with open(filename, 'r') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []
        print("Current",bundle_id)
    else:
        existing_data = []

    # Append the new data to the existing data
    existing_data.extend(data)

    # Write the updated data back to the file
    with open(filename, 'w') as file:
        json.dump(existing_data, file)

def getDataFronExcelAsJson(qpCode, requestedBundleCode):
    folder_path = "./Generated_Distributions/"+folderName
    # print(qpCode)
    
    for filename in os.listdir(folder_path):
        if filename.startswith(xlFIleName) and filename.endswith(str(qpCode)+'.xlsx'):
            input_file = os.path.join(folder_path, filename)
            
            # Read the processed Excel file as DataFrame
            df = pd.read_excel(input_file)
            
            # Convert each row to a dictionary and append to the list
            for _, row in df.iterrows():
                # data_dict = {
                #     'Qp Code': row['Bundle Code'][2:6],
                #     'Bundle Code': row['Bundle Code'],
                #     'AS Count': row['AS Count'],
                #     'District': row['District'],
                #     'Status': row['Status']
                # }
                bundleCode = row['Bundle Code']
                campName = row['Camp']

                if bundleCode == requestedBundleCode:
                    if campName == "Pathanamthitta":
                        # print(colorama.Fore.YELLOW+campName+ colorama.Fore.RESET)
                        return "Pandalam"
                    else:
                        # print(colorama.Fore.YELLOW+campName+ colorama.Fore.RESET)\
                        return campName

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/api/save_data", methods=["POST"])
def saveDetails():
    bundle_id = request.json.get("bundleID")
    try:
        tvmCampBundles = []
        tvmCampBundles.append(str(bundle_id))
        save_to_json_file('tvmCampBundles_list.json',tvmCampBundles, bundle_id)
        return jsonify({'status':'Success'})
    except:
        return jsonify({'status':'Error'})


@app.route("/api/get_data", methods=["POST"])
def get_data():
    bundle_id = request.json.get("bundleID")
    print(colorama.Fore.RED+bundle_id+ colorama.Fore.RESET)
    campName = getDataFronExcelAsJson(bundle_id[:6],bundle_id)
    if bundle_id[:6] != 'R 7560':
         print(colorama.Fore.GREEN+'WARNING CHANGE IN QP CODE DETECTED'+ colorama.Fore.RESET)
    if campName is not None:
        print(colorama.Fore.YELLOW+campName+ colorama.Fore.RESET)
        result = {"bundleID":bundle_id,"district": campName,"status": "success"}
        return jsonify(result)
    else:
        print(colorama.Fore.RED+"Bundle Not Distributed"+ colorama.Fore.RESET)
        return jsonify({"bundleID":bundle_id,"status": "failed"})
    
@app.route("/api/get_bundles", methods=["POST"])
def get_bundles():
    qpCode = request.json.get("qpCode")
    campName = request.json.get("campName")
    print("Fetching Bundles For", qpCode,campName)
    bundleCodes = getBundleCodes(qpCode, campName)
    if bundleCodes is not None:
        result = {"bundleCodes":bundleCodes,"status": "success"}
        print(len(bundleCodes))
        return jsonify(result)




if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',ssl_context='adhoc')