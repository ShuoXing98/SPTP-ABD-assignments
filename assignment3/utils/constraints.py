import numpy as np

class Constriant:
    def __init__(self):
        super(Constriant, self).__init__()
        pass

    def feasibility(self, id, slon):
        pass

class Cardinality_Constriant(Constriant):
    def __init__(self, k):
        super(Cardinality_Constriant, self).__init__()
        self.k = k

    def feasibility(self, sequence):
        current_cardinality = len(sequence)
        if current_cardinality < self.k:
            return True
        else:
            return False

class Matroid_Constriant(Constriant):
    def __init__(self):
        super(Matroid_Constriant, self).__init__()
        pass
    def get_rank(self):
        pass

    def feasibility(self, id, slon):
        pass

class Partation_Matroid(Matroid_Constriant):
    def __init__(self, groups_elements, groups_caridinality):
        super(Partation_Matroid, self).__init__()
        self.groups_elements = groups_elements
        self.k = groups_caridinality

    def get_rank(self):
        return np.sum(self.k)

    def feasibility(self, group_of_id, current_set):
        current_groups_of_elements = [self.groups_elements[id] for id in current_set]
        id_count = current_groups_of_elements.count(group_of_id)
        if id_count < self.k[group_of_id]:
            return True
        else:
            return False