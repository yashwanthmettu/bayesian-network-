import sys

class B_E_A_J_M(object):
    def events_probability(self, values):
        burglary=self.relations("B", values[0], None, None)
        earthquake=self.relations("E", values[1], None, None)
        alarm=self.relations("A|B,E", values[2], values[0], values[1])
        Johncalls=self.relations("J|A", values[3], values[2], None)
        Marycalls=self.relations("M|A", values[4], values[2], None)
        return burglary * earthquake * alarm * Johncalls * Marycalls

    def relations(self, event, prob_a, prob_b, prob_c):
        if event == "B":
            return 0.001 if prob_a else 0.999
        elif event == "E":
            return 0.002 if prob_a else 0.998
        elif event == "A|B,E":
            p_2 = {
                (True, True): 0.95,
                (True, False): 0.94,
                (False, True): 0.29,
                (False, False): 0.001}.get((prob_b, prob_c), None)
            return p_2 if prob_a else (1 - p_2)
        elif event == "J|A":
            p_2 = 0.9 if prob_b else 0.05
            return p_2 if prob_a else (1 - p_2)
        elif event == "M|A":
            p_2 = 0.7 if prob_b else 0.01
            return p_2 if prob_a else (1 - p_2)
        else:
            raise ValueError("Invalid event")

    def event(self, values):
        if not None in values:
            return self.events_probability(values)
        else:
            index = values.index(None)
            next_values_true = list(values)
            next_values_true[index] = True
            prob_t = self.event(next_values_true)
            next_values_false=list(values)
            next_values_false[index] = False
            prob_f = self.event(next_values_false)
            return prob_t + prob_f

    def get_result(self, values):
        result = []
        prefixes = ["B", "E", "A", "J", "M"]

        for prefix in prefixes:
            true_key = prefix + "t"
            false_key = prefix + "f"

            if true_key in values:
                result.append(True)
            elif false_key in values:
                result.append(False)
            else:
                result.append(None)
        return result

def bnet():
    given = False
    observations = []
    query = []

    for argument in sys.argv:
        if argument == "given":
                given = True
        query.append(argument)
        if given:
            observations.append(argument)

    if not query:
        print("Invalid query")
        return

    network = B_E_A_J_M()
    x = network.event(network.get_result(query))
    if observations:
        y = network.event(network.get_result(observations))
    else:
        y = 1
    print("The probability =",  (x/y))

bnet()