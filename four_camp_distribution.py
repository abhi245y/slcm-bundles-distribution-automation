import json
import os
import pandas as pd
from pprint import pprint
from typing import Dict, List, Tuple

def check_remaining_packets(destination_values: Dict[str, int], 
                            sorted_packets: List[Tuple[int, str, str]], 
                            not_sent_packet_ids: List[str]) -> bool:
    """
    Checks if there are any remaining bundles to be allocated.

    Args:
    destination_values (Dict[str, int]): The values for each destination.
    sorted_packets (List[Tuple[int, str, str]]): The sorted list of packets.
    not_sent_packet_ids (List[str]): List of packet IDs that are not yet sent.

    Returns:
    bool: True if no remaining packets, False otherwise.
    """
    messages = []
    packet_values = []           
    for packet_value, packet_id, origin_place in sorted_packets:
        if packet_id in not_sent_packet_ids:
            messages.append(f"Packet ID: {packet_id}, Origin Place: {origin_place}, Value: {packet_value}")
            packet_values.append(packet_value)
    if len(not_sent_packet_ids) != 0:
        pprint(messages)
        print(f"Remaining Slots: {destination_values} || Remaining packets to be allocated: {len(not_sent_packet_ids)} || Remaining packets total weight: {sum(packet_values)}")
        print("Reallocating...")
        return False
    return True

def distribute_packets(packet_values: List[int], 
                        packet_ids: List[str], 
                        origin_places: List[str], 
                        distribution_places: List[str], 
                        target_values: List[int]) -> Dict[str, List[Tuple[str, int, str]]]:
    """
    Core function which distributes packets to different camps.

    Args:
    num_packets (int): Number of packets.
    packet_values (List[int]): List of packet values.
    packet_ids (List[str]): List of packet IDs.
    origin_places (List[str]): List of origin places.
    distribution_places (List[str]): List of distribution places.
    target_values (List[int]): List of target values for each place.

    Returns:
    Dict[str, List[Tuple[str, int, str]]]: Distribution of packets to destinations.
    """
    total_value = sum(packet_values)
    sent_packet_ids = []

    destination_values = {place: value for place, value in zip(distribution_places, target_values)}
    destination_packets = {place: [] for place in distribution_places}

    sorted_packets = sorted(zip(packet_values, packet_ids, origin_places), reverse=True)

    
    for value, packet_id, origin_place in sorted_packets:
        for destination_place in distribution_places:
            if origin_place != destination_place and destination_values[destination_place] >= value:
                destination_values[destination_place] -= value
                destination_packets[destination_place].append((packet_id, value, origin_place))
                sent_packet_ids.append(packet_id)
                break 
    
    for value, packet_id, origin_place in sorted_packets:
        if packet_id in [packet_id for packet_id in packet_ids if packet_id not in sent_packet_ids]:
            for destination_place in distribution_places:
                if  destination_values[destination_place] >= value:
                    destination_values[destination_place] -= value
                    destination_packets[destination_place].append((packet_id, value, origin_place))
                    sent_packet_ids.append(packet_id)
                    break
                
    for value, packet_id, origin_place in sorted_packets:
        if packet_id in [packet_id for packet_id in packet_ids if packet_id not in sent_packet_ids]:
            if origin_place == "Thiruvananthapuram":
                destination_values["Kollam"] -= value
                destination_packets["Kollam"].append((packet_id, value, origin_place))
                sent_packet_ids.append(packet_id)
            elif origin_place == "Kollam":
                destination_values["Thiruvananthapuram"] -= value
                destination_packets["Thiruvananthapuram"].append((packet_id, value, origin_place))
                sent_packet_ids.append(packet_id)
        
    if check_remaining_packets(destination_values, sorted_packets, not_sent_packet_ids=[packet_id for packet_id in packet_ids if packet_id not in sent_packet_ids]) == False:
        remaining = [packet_id for packet_id in packet_ids if packet_id not in sent_packet_ids]
        if len(remaining) > 1:
            split_point = len(remaining) // 2
            for value, packet_id, origin_place in sorted_packets:
                if packet_id in remaining[:split_point]:
                    destination_values["Thiruvananthapuram"] -= value
                    destination_packets["Thiruvananthapuram"].append((packet_id, value, origin_place))
                    sent_packet_ids.append(packet_id)
                elif packet_id in  remaining[split_point:]:
                    destination_values["Kollam"] -= value
                    destination_packets["Kollam"].append((packet_id, value, origin_place))
                    sent_packet_ids.append(packet_id)
        elif len(remaining) == 1:
            for value, packet_id, origin_place in sorted_packets:
                if packet_id in remaining:
                    destination_values["Thiruvananthapuram"] -= value
                    destination_packets["Thiruvananthapuram"].append((packet_id, value, origin_place))
                    sent_packet_ids.append(packet_id)
        
    # Final check and packet allocation
    if check_remaining_packets(destination_values, sorted_packets, not_sent_packet_ids=[packet_id for packet_id in packet_ids if packet_id not in sent_packet_ids]):
        print("All Packets Allocated")
        print('###################################################################################################################################################\n\n')
    return destination_packets

def convert_grabbed_excel_files_to_json(
    qpCode: str,
    packet_values: List[int],
    packet_ids: List[str],
    origin_places: List[str],
    courseAndSemName: str,
    bundle_details_excel_files_folderpath: str
) -> None:
    """
    Converts the tables scraped using bundle_details_collector.py to json.

    Args:
        qpCode (str): Code for the question paper.
        packet_values (List[int]): List to store packet values.
        packet_ids (List[str]): List to store packet IDs.
        origin_places (List[str]): List to store origin places.
        courseAndSemName (str): Name of the course and semester.
        bundle_details_excel_files_folderpath (str): Path to the folder containing bundle details.
    """
    for filename in os.listdir(bundle_details_excel_files_folderpath):
        if filename.startswith(courseAndSemName) and filename.endswith(str(qpCode) + '.xlsx'):
            input_file = os.path.join(bundle_details_excel_files_folderpath, filename)
            df = pd.read_excel(input_file)

            for _, row in df.iterrows():
                packet_ids.append(row["Bundle\xa0Code"])     
                packet_values.append(int(row["AS Count"]))
                origin_places.append(row["District"])


def main(distribution_data: Dict[str, int], 
        distribution_places: List[str], 
        course_and_sem_name: str, 
        bundle_details_excel_files_folderpath: str) -> Dict[str, List[Tuple[str, int, str]]]:
    """
    Gathers necessary data and passes them to different functions for execution.

    Args:
    distribution_data (Dict[str, int]): Distribution data.
    distribution_places (List[str]): List of distribution places.
    course_and_sem_name (str): Name of the course and semester.
    bundle_details_excel_files_folderpath (str): Path to the folder containing bundle details.

    Returns:
    Dict[str, List[Tuple[str, int, str]]]: Final distribution of packets.
    """

    packet_values = []
    packet_ids = []
    origin_places = []

    convert_grabbed_excel_files_to_json(distribution_data['Qp_Code'],packet_values,packet_ids,origin_places,course_and_sem_name,bundle_details_excel_files_folderpath)


    num_packets = len(packet_ids)

    target_values = []
    for place in distribution_places:
        print("Total value for {}:".format(place), distribution_data[place])
        target_values.append(distribution_data[place])

    destination_packets = distribute_packets(packet_values, packet_ids, origin_places, distribution_places, target_values)
    return destination_packets