import networkx as nx
import numpy as np
import scipy 

class Sim(object):
    def __init__(self, rate, size, res_factor,
                 graph=False, Nmonte_points=10000):
        self.rate = rate 
        self.size = size
        self.area = size * size 
        self.res_factor = res_factor # for final coverage estimation
        self.graph = graph
        self.Nmonte_points=Nmonte_points
        self.dr = 1 

        self.coverage = 0

        self.G = nx.Graph()
        self.G.add_nodes_from(['top','bottom','left','right'])

        self.Nnodes = 0
        self.radii = np.zeros(1,int)
        self.radii2 = np.zeros(1,int)
        
        self.all_connected_top = set() # all nodes connected to top
        self.all_connected_left = set() # all nodes connected to left
        
        self.monte_points = self.create_monte_points()       
        
        self.nodes = np.random.random(2).reshape(1,2) * self.size
        self.Nnodes = 1
        
        self.distance_matrix = self.find_distances()
        self.radii = np.zeros(1,int)
        self.radii2 = np.zeros(1,int)
        
        self.monte_distances2 = np.empty((0,self.Nmonte_points))
        self.monte_distances2 = self.add_monte_distance2(self.nodes[0],self.monte_points)

    def simulate(self):
        path = False #either a path from top to bottom, or left to right
        nodes_to_add = 0
        while not path:
            if nodes_to_add:
                self.nodes, added = self.add_nodes(self.nodes,nodes_to_add)
                if added: 
                    self.distance_matrix = self.find_distances()
                    self.radii = np.append(self.radii,[0]*added)
                    self.radii2 = np.append(self.radii2,[0]*added)

            nodes_to_add = self.increment()
            
            if self.check_path(self.G,'top','bottom',{'left','right'}): break
            if self.check_path(self.G,'left','right',{'top','bottom'}): break
        self.monte_distances2 = self.calc_monte_distances2(self.nodes,
                                                           self.monte_points)
        self.coverage = self.calc_monte_coverage()
        
        if self.graph:
            with open('nodes.dat','w') as f:
                for i in range(self.Nnodes):
                    r = self.radii[i]
                    if r != 0:
                      f.write(str(self.nodes[i][0]/self.size)+'\t'+
                            str(self.nodes[i][1]/self.size)+'\t'+
                            str(float(r)/self.size)+'\n')
            with open('nodes1.dat','w') as f:
                for i in range(self.Nnodes):
                    r = self.radii[i]-1
                    if r != 0:
                      f.write(str(self.nodes[i][0]/self.size)+'\t'+
                            str(self.nodes[i][1]/self.size)+'\t'+
                            str(float(r)/self.size)+'\n')
    
    def check_path(self,graph,source,target,ignore):
        sub_graph = graph.subgraph( set(graph.nodes) - ignore)
        if nx.has_path(sub_graph,source,target):
            path = True
        else:
            path = False
        return path
            

    def create_monte_points(self):
        N = self.Nmonte_points 
        points = np.random.rand(N,2)
        #with open('monte','w') as f:
        #    for point in points:
        #        f.write(str(point[0])+'\t'+str(point[1])+'\n')
        return points * self.size
    
    def add_monte_distance2_2(self,nodes,points):
        #x = points[:,0] - node[0]
        #y = points[:,1] - node[1]
        #dist2 = x*x + y*y

        # square distance between all pairs of coords in lists nodes and points
        print 'nodes',nodes
        print 'points',points
        dist2_i = np.sum((nodes[:, None,:] - points[None, :, :])**2,2)
        return np.vstack((self.monte_distances2,dist2))

    def calc_monte_distances2(self, nodes, points):
        return np.sum((nodes[:, None,:] - points[None, :, :])**2,2)

    def add_monte_distance2(self,node,points):
        x = points[:,0] - node[0]
        y = points[:,1] - node[1]
        dist2 = x*x + y*y

        #dist = points - node
        #dist2 = np.sum(dist*dist,1)
        return np.vstack((self.monte_distances2,dist2))

    def calc_monte_coverage(self):
        coverage_matrix = self.monte_distances2 < self.radii2[:,np.newaxis]
        coverage = np.sum(coverage_matrix,0) > 0
        return float(np.sum(coverage)) / self.Nmonte_points

    def find_path(self, all_connected, touching_opposite_boundary):
        ispath = False
        #     print i, self.touching_top
        #     print self.radius, already_checked
        searching = True 
        to_search = all_connected
        last_connected = set()
        while searching:
            to_search = all_connected - last_connected
            last_connected = set(all_connected)
            for j in to_search: 
                for k in range(self.Nnodes):
                    if self.touch_matrix[j,k]:
                        all_connected |= { k }

            if all_connected & touching_opposite_boundary:
                ispath = True
                searching = False
            if len(last_connected) == len(all_connected):
                break
        #print self.radius,path
        #print 'bot',self.touching_bottom
        #print '!  ',bool(connected &self.touching_bottom )
        #print ispath
        if ispath  and self.graph:
            with open('monte.dat','w') as f:
                for i in all_connected:
                    if self.radii[i] != 0:
                        f.write(str(self.nodes[i][0]/(self.size))+'\t'+
                                str(self.nodes[i][1]/(self.size))+'\n')
        return ispath, all_connected
 

    def increment(self):
        self.radii += self.dr
        self.radii2 = self.radii * self.radii
        if len(self.radii) != self.Nnodes: raise Exception(self.Nnodes,self.radii)
        
        self.touch_matrix = self.circles_touching()
        self.G.add_edges_from( np.transpose(np.where(self.touch_matrix==1)) )
        self.update_touching_boundary()

        add = np.random.poisson( float(self.rate) / self.size) 

        return add
        
    def update_touching_boundary(self):
        for i in range(self.Nnodes):
            x = self.nodes[i][0]
            y = self.nodes[i][1]
            r = self.radii[i]
            if y - r < 0:
                self.G.add_edge('bottom',i)
            if y + r > self.size:
                self.G.add_edge('top',i)
            if x - r < 0:
                self.G.add_edge('left',i)
            if x + r > self.size:
                self.G.add_edge('right',i)

    def find_distances(self):
        matrix = np.zeros((self.Nnodes,self.Nnodes))
        for i in range(self.Nnodes):
            n1 = self.nodes[i]
            for j in range(i+1,self.Nnodes):
                n2 = self.nodes[j]
                r2 = self.distance2(n1, n2)
                matrix[i,j] = r2
                matrix[j,i] = r2
        return matrix

    def circles_touching(self):
        radius_matrix = self.radii + self.radii[:,np.newaxis] 
        radius_matrix = radius_matrix**2
        np.fill_diagonal(radius_matrix,0)
        touch_matrix = radius_matrix > self.distance_matrix
        return touch_matrix

    def add_nodes(self, nodes, N):
        added = 0
        for i in range(N):
            x = np.random.random() * self.size
            y = np.random.random() * self.size
            add = True
            for j in range(self.Nnodes):
                if self.distance([x,y],nodes[j]) < self.radii[j]:
                    add = False
            if add: 
                nodes = np.vstack((nodes, [x,y] ))
                added += 1
        self.Nnodes += added

        #if added:
        #    print self.radii[0],added
        return nodes, added

    def distance2(self, r1, r2):
        a = r1[0] - r2[0]
        b = r1[1] - r2[1]
        return a * a + b * b

    def distance(self, r1, r2):
        a = r1[0] - r2[0]
        b = r1[1] - r2[1]
        mag = a * a + b * b
        return np.sqrt(mag)
    
    def print_output(self):
        print 'Coverage   =',self.coverage
        print 'Nsites     =',self.Nnodes
        print 'Max radius =',self.radii[0]
        #print 'Niter      =',self.radii[0]

