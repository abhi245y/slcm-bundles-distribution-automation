import json
import os
import pandas as pd
from pprint import pprint
from typing import Dict, List, Tuple

def check_remaining_packets(destination_values: Dict[str, int], sorted_packets: List[Tuple[int, str, str]], not_sent_packet_ids: List[str]) -> bool:
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

def distribute_packets(num_packets: int, packet_values: List[int], packet_ids: List[str], origin_places: List[str], distribution_places: List[str], target_values: List[int]) -> Dict[str, List[Tuple[str, int, str]]]:
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
    
    # Allocation logic
    # [..code unchanged..]

    # Final check and packet allocation
    if check_remaining_packets(destination_values, sorted_packets, not_sent_packet_ids=[packet_id for packet_id in packet_ids if packet_id not in sent_packet_ids]):
        print("All Packets Allocated")
        print('###################################################################################################################################################\n\n')
    return destination_packets

def main(distribution_data: Dict[str, int], distribution_places: List[str], course_and_sem_name: str, bundle_details_excel_files_folderpath: str) -> Dict[str, List[Tuple[str, int, str]]]:
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

    num_packets = len(packet_ids)

    target_values = []
    for place in distribution_places:
        print("Total value for {}:".format(place), distributionData[place])
        target_values.append(distributionData[place])

    destination_packets = distribute_packets(num_packets, packet_values, packet_ids, origin_places, distribution_places, target_values)
    return destination_packets