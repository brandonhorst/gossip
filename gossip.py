#!/usr/bin/env python3
import json
import heapq


class School:
    """class School - represents some students with some listeners,
    each with a conversation length. This forms a directed, weighted graph,
    where the nodes are students, the edges point from student->listener,
    and the weights for each edge is the time of the conversation.

    Data is stored in a self.students, a dict with one key for each student.
    The value of this dict is another dict, with one key for each listener, and
    the value is the time of this conversation.

    {
        talker1: {
            listener1: time1,
            listener2: time2
            ...
        }
        ...
    }
    """

    def __init__(self, chain):
        """accepts a chain in the form:
        [
            {talker: "name", listener: "name", time: "time"},
            ...
        ]

        Populates self.students. self.students should not be modified after
        initialization.
        """
        self.students = {}
        for entry in chain:
            talker = entry["talker"]
            listener = entry["listener"]
            time = entry["time"]

            if talker not in self.students.keys():
                self.students[talker] = {}
            self.students[talker][listener] = time

    def search(self, gossiper, victim):
        """Find the shortest time between gossiper and victim.

        Keyword arguments:
        gossiper -- the name of the student the gossip starts with
        victim -- the name of the student the gossip ends with

        Returns: minimum time for the gossip to get to the victim, in seconds

        Uses Dijkstra's algorithm for finding the minimum time.
        Does not modify self in any way, so this call is thread-safe.
        """
        #unvisited: set of all students that have not yet been visited.
        # initialized to all students.
        unvisited = set(self.students.keys())

        #if gossiper or victim are not in our set, raise an Exception
        if not gossiper in unvisited:
            raise ValueError("gossiper ({0}) not in gossip chain".format(gossiper))

        if not victim in unvisited:
            raise ValueError("victim ({0}) not in gossip chain".format(victim))

        #times: dict of {student: time} for each student, where time
        # represents the minimum time it would take for the gossip to
        # get to that student
        # initialized to infinity for all students, but 0 for the gossiper
        times = {name: float("inf") for name in self.students.keys()}
        times[gossiper] = 0

        while unvisited:
            #Of all the unvisited students,
            # get the student with the minimum distance
            this_student = min(unvisited, key = times.get)

            #If the minimum unvisited time is infinity, the input must not
            # have been a proper graph, because all remaining students
            # are not listeners for anyone who has already been visited
            if times[this_student] == float("inf"):
                raise RuntimeError("provided gossip chain is not a true graph")

            #if we are visiting the victim, then we have done it
            # return the time that it took to get here
            if this_student == victim:
                return times[this_student]

            #visit this student, so remove from unvisited set
            unvisited.remove(this_student)

            #for all of this_student's listeners...
            for listener, time in self.students[this_student].items():
                
                #check to see if the time through this path is
                # less than their previous time. If it is, update it
                time_to_listener = times[this_student] + time
                if time_to_listener < times[listener]:
                    times[listener] = time_to_listener

#Simple CLI implementation
if __name__ == '__main__':
    import sys

    if not len(sys.argv) == 3:
        print("Accepts 2 arguments: gossiper and victim. Case sensitive")
        quit(0)

    gossiper, victim = sys.argv[1:]

    #Load up the gossip-chain from a json file, and create a School
    with open('gossip-chain.json', 'r') as file:
        gossip_chain = json.load(file)
    school = School(gossip_chain)

    #take the gossiper and victim from system arguments, and search
    time = school.search(gossiper, victim)

    print("Time from {0} to {1}: {2}".format(gossiper, victim, time))
    quit(1)