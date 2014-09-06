#!/usr/bin/env python3

import gossip
import json
from threading import Thread
from timeit import timeit
import sys

#run the gossip search, and return the amount of time to complete in ms
def profile(talker, listener, iterations=1):
    """run gossip.School::search multiple times with talker and listener
    , and return average execution time."""

    total_time = timeit(
        stmt="school.search('{0}', '{1}')".format(talker, listener),
        setup="import gossip; school = gossip.School({0})".format(gossip_chain),
        number=iterations)

    #convert s -> ms, account for multiple iterations
    return total_time / iterations * 1000

#run the program for the given input.
#actually runs it twice - once to get the results, and once to time it
def runChain(input_obj):
    rumor_id = input_obj["id"]
    talker = input_obj["talker"]
    listener = input_obj["listener"]
    school = gossip.School(gossip_chain)

    output_obj = {
        "id": rumor_id,
        "travel_time": school.search(talker, listener),
        "calc_time": profile(talker, listener)
    }
    #this is thread safe
    results[rumor_id - 1] = (input_obj, output_obj)

with open('gossip-chain.json', 'r') as gossip_file:
    gossip_chain = json.load(gossip_file)

with open('input.json', 'r') as input_file:
    inputs = json.load(input_file)

#initialize an array to contain the inputs
results = [None] * len(inputs)
threads = []

#run each input in a new thread
for input_obj in inputs:
    thread = Thread(target=runChain, args=[input_obj])
    threads.append(thread)
    thread.start()

#wait for all threads to terminate
for thread in threads:
    thread.join()

#print the results in order for easy copy-paste
for input_obj, output_obj in results:
    print(json.dumps(input_obj), "\t", json.dumps(output_obj))