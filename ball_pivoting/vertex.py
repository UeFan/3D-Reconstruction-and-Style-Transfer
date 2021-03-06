import numpy as np
import pcl


class Vertex(object):

    def __init__(self, xyz, n_xyz, idx=-1):
        self.xyz = xyz
        self.n_xyz = n_xyz
        self.adj_edges = []
        self.adj_facets = []
        self.type = 0 # 0: orphan; 1: front; 2: inner
        self.idx = idx
        self.seed_candidate = True
        

    def add_adjacent_edge(self, e):
        self.adj_edges.append(e)
        

    def remove_adjacent_edge(self, e):
        self.adj_edges.remove(e)
        

    def add_adjacent_facet(self, f):
        self.adj_facets.append(f)
        

    def remove_adjacent_facet(self, f):
        self.adj_facets.remove(f)
        

    def set_type(self, ty):
        self.type = ty
        

    def get_type(self):
        return self.type
    

    def update_type(self):
        if len(self.adj_edges) == 0:
            self.type = 0
            return
        self.seed_candidate = False
        for e in self.adj_edges:
            if e.get_type != 2:
                self.type = 1
                return
        self.type = 2
        

    def adjacent_edges(self):
        return self.adj_edges
    

    def get_links(self, v):
        inters = set(self.adj_edges) & set(v.adj_edges)
        if inters == set():
            return None
        return next(iter(inters))
    

    def compatible_with(self, v1, v2):
        nt = np.cross(self.xyz-v1.xyz, v2.xyz-v1.xyz)
        if np.linalg.norm(nt) == 0:
            return False
        nt = nt / np.linalg.norm(nt)
        if np.dot(nt, self.n_xyz) < 0:
            nt = -nt
        if np.dot(nt, v1.n_xyz) > 0 and np.dot(nt, v2.n_xyz) > 0:
            return True
        return False
    

    def distance_to(self, v):
        if isinstance(v, np.ndarray):
            return np.linalg.norm(self.xyz - v)
        else:
            return np.linalg.norm(self.xyz - v.xyz)
        

    def find_border(self, t):
        e0 = self.get_links(t)
        facet = e0.adj_facet1
        candidate = None
        for ei in self.adj_edges:
            if ei.type != 0:
                continue
            v = ei.source
            if v == self:
                continue
            if facet.has_vertex(v):
                continue
            e = v.get_links(t)
            if e is None:
                continue
            if e.type != 0 or e.source != t:
                continue
            return v
        return candidate

    
