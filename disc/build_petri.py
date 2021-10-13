from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.petri_net.utils import petri_utils
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter

# Receives as input: SequenceDatabase, X,Y sets of regions
def build_petrinet(sdb,X,Y):
    net = PetriNet("new_petri_net")
    source = PetriNet.Place("source")
    sink = PetriNet.Place("sink")
    net.places.add(source)
    net.places.add(sink)
    num_act = sdb.num_activities

    trans = []

    for i in range(num_act-2):
        act = sdb.idx_to_activity[i]
        t = PetriNet.Transition(act, act)
        trans.append(t)
        net.transitions.add(t)

    #Model artificial start and end activities as silent transitions for conformance
    t_start = PetriNet.Transition("art_start", None)
    trans.append(t_start)
    net.transitions.add(t_start)
    t_end = PetriNet.Transition("art_end", None)
    trans.append(t_end)
    net.transitions.add(t_end)

    #add arcs to/from artificial start/end
    petri_utils.add_arc_from_to(source, trans[num_act-2], net)
    petri_utils.add_arc_from_to(trans[num_act-1], sink, net)

    for i in range(len(X)):
        x=X[i]
        y=Y[i]
        place = PetriNet.Place("p"+ str(i))
        for j in range(num_act):
            if x[j] == 1:
                petri_utils.add_arc_from_to(trans[j], place, net)
            if y[j] == 1:
                petri_utils.add_arc_from_to(place, trans[j], net)

    initial_marking = Marking()
    initial_marking[source] = 1
    final_marking = Marking()
    final_marking[sink] = 1

    return net, initial_marking, final_marking

