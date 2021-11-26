# import numpy as np
import math

def Distance(p1, p2):
    a = p1['lon'] - p2['lon']
    b = p1['lat'] - p2['lat']
    dis = math.sqrt(a*a + b*b)
    return dis

class WayPoints():
    def __init__(self,radius=20, circ_pts=6, directs=8):
        self.radius = radius * pow(10,-5)        #1 degree: 100km
        self.circ_pts = circ_pts
        self.directs = directs
        self.angle = 2*math.pi / circ_pts

    def _k_means(self,):
        pass

    def _dymatic(self,):
        pass

    def _greedy(self,objs,start):
        waittings = objs.copy()
        results = []
        cur = start
        for i in range(len(waittings)):
            min_dis = float('inf')
            idx = 0
            for j,pt in enumerate(waittings):
                dis = Distance(cur,pt)
                if min_dis > dis:
                    min_dis = dis
                    idx = j
            cur = waittings[idx]
            waittings.remove(cur)
            results.append(cur)

        return results

    def _circle(self, objs):
        results = []
        for i, ob in enumerate(objs):
            for j in range(self.circ_pts):
               pt = ob.copy()
               pt['lon'] = ob['lon'] + math.cos(j * self.angle) * self.radius
               pt['lat'] = ob['lat'] + math.sin(j * self.angle) * self.radius
               results.append(pt)

        return results

    def _towards(self, objs):
        results = []
        for i, ob in enumerate(objs):
           pt = ob.copy()
           direct = 1
           if 'direction' in pt:
               di = pt['direction']
               if di >= 1 and di <= 8:
                   direct = di
           angle = 2*math.pi * (direct-1) / self.directs
           pt['lon'] = ob['lon'] + math.cos(angle) * self.radius
           pt['lat'] = ob['lat'] + math.sin(angle) * self.radius
           pt['direction'] = direct
           results.append(pt)

        return results

    def design_circling(self,objs,start):
        obj_waypoints = self._greedy(objs,start)
        results = self._circle(obj_waypoints)
        return results

    def design_towards_ex(self,objs,start):
        obj_waypoints = self._greedy(objs,start)
        results = self._towards(obj_waypoints)
        return results

    def design_towards(self,objs,start):
        off_objs = self._towards(objs)
        results = self._greedy(off_objs,start)
        return results

