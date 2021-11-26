# -*- coding: utf-8 -*-
import sys
import os
import json
import math
import xml.dom.minidom
import datetime
from geopy.distance import geodesic
from waypoints import WayPoints


# 将规划好的航点写入到KML文件中
class WayPointsCoordsDesign:
    def __init__(self):
        # 在内存中创建一个空的文档
        self.doc = xml.dom.minidom.Document()
        # 创建一个根节点Managers对象
        self.kml = self.doc.createElement('kml')
        # 设置根节点的属性
        self.kml.setAttribute('xmlns', 'http://www.opengis.net/kml/2.2')

    def makeKmlFile(self, wayPointsCoords, altitude=50.0, flightSpeed=6.0, hoverTime=1, actionOnFinish='GoHome',
                    gimbalPitch=0, kmlFloder="./KML/"):
        dtime = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        towards = {1: "-90", 2: "-135", 3: "180", 4: "135", 5: "90", 6: "45", 7: "0", 8: "-45"}

        # 将根节点添加到文档对象中
        Document = self.doc.createElement('Document')
        Document.setAttribute('xmlns', '')

        Name = self.doc.createElement('name')
        Name.appendChild(self.doc.createTextNode(dtime))

        Open = self.doc.createElement('open')
        Open.appendChild(self.doc.createTextNode('1'))

        ExtendedData = self.doc.createElement('ExtendedData')
        ExtendedData.setAttribute('xmlns:mis', 'www.dji.com')

        ExtendedData.appendChild(self.creatElement('mis:type', 'Waypoint'))
        ExtendedData.appendChild(self.creatElement('mis:stationType', '0'))

        StyleLine = self.doc.createElement('Style')
        StyleLine.setAttribute('id', 'waylineGreenPoly')

        LineStyle = self.doc.createElement('LineStyle')
        LineStyle.appendChild(self.creatElement('color', 'FF0AEE8B'))
        LineStyle.appendChild(self.creatElement('width', '6'))
        StyleLine.appendChild(LineStyle)

        StylePoint = self.doc.createElement('Style')
        StylePoint.setAttribute('id', 'waypointStyle')
        IconStyle = self.doc.createElement('IconStyle')
        Icon = self.doc.createElement('Icon')
        Href = self.doc.createElement('href')
        Href.appendChild(self.doc.createTextNode('https://cdnen.dji-flighthub.com/static/app/images/point.png'))
        Icon.appendChild(Href)
        IconStyle.appendChild(Icon)
        StylePoint.appendChild(IconStyle)

        Document.appendChild(Name)
        Document.appendChild(Open)
        Document.appendChild(ExtendedData)
        Document.appendChild(StyleLine)
        Document.appendChild(StylePoint)

        Folder = self.doc.createElement('Folder')
        Folder.appendChild(self.creatElement('name', 'Waypoints'))
        Folder.appendChild(self.creatElement('description', 'Waypoints in the Mission.'))

        counter = 0
        for i, point in enumerate(wayPointsCoords):
            counter = counter + 1
            Placemark = self.doc.createElement('Placemark')
            Name = self.doc.createElement('name')
            Name.appendChild(self.doc.createTextNode('Waypoint' + str(counter)))
            Visibility = self.doc.createElement('visibility')
            Visibility.appendChild(self.doc.createTextNode('1'))
            Description = self.doc.createElement('description')
            Description.appendChild(self.doc.createTextNode('Waypoint'))
            StyleUrl = self.doc.createElement('styleUrl')
            StyleUrl.appendChild(self.doc.createTextNode('#waypointStyle'))
            ExtendedData = self.doc.createElement('ExtendedData')
            ExtendedData.setAttribute('xmlns:mis', 'www.dji.com')

            ExtendedData.appendChild(self.creatElement('mis:useWaylineAltitude', 'true'))
            ExtendedData.appendChild(self.creatElement('mis:heading', '0'))
            ExtendedData.appendChild(self.creatElement('mis:turnMode', 'Auto'))
            ExtendedData.appendChild(self.creatElement('mis:gimbalPitch', float(gimbalPitch)))
            ExtendedData.appendChild(self.creatElement('mis:useWaylineSpeed', 'true'))
            ExtendedData.appendChild(self.creatElement('mis:speed', flightSpeed))
            ExtendedData.appendChild(self.creatElement('mis:useWaylineHeadingMode', 'true'))
            ExtendedData.appendChild(self.creatElement('mis:useWaylinePointType', 'true'))
            ExtendedData.appendChild(self.creatElement('mis:pointType', 'LineStop'))
            ExtendedData.appendChild(self.creatElement('mis:cornerRadius', '0.2'))

            # 飞行器偏航角
            angle_pt = towards[int(point['direction'])]
            ExtendedData.appendChild(self.creatElement('mis:actions ', 'AircraftYaw',
                                                       [('param', angle_pt), ('accuracy', 0),
                                                        ('cameraIndex', 0),
                                                        ('payloadType', 0), ('payloadIndex', 0)]))

            # 云台俯仰角
            # ExtendedData.appendChild(self.creatElement('mis:actions ', 'GimbalPitch',
            #                                            [('param', gimbalPitch * 10), ('accuracy', 1),
            #                                             ('cameraIndex', 0),
            #                                             ('payloadType', 0), ('payloadIndex', 0)]))
            if hoverTime != 0:
                # 悬停
                ExtendedData.appendChild(self.creatElement('mis:actions ', 'Hovering',
                                                           [('param', hoverTime * 1000), ('accuracy', 0),
                                                            ('cameraIndex', 0),
                                                            ('payloadType', 0), ('payloadIndex', 0)]))
            # 拍照
            ExtendedData.appendChild(self.creatElement('mis:actions', 'ShootPhoto',
                                                       [('param', 0), ('accuracy', 0), ('cameraIndex', 0),
                                                        ('payloadType', 0), ('payloadIndex', 0)]))

            Point = self.doc.createElement('Point')

            Point.appendChild(self.creatElement('altitudeMode', 'relativeToGround'))

            Point.appendChild(self.creatElement('coordinates', f'{point["lon"]},{point["lat"]},{altitude}'))

            Placemark.appendChild(Name)
            Placemark.appendChild(Visibility)
            Placemark.appendChild(Description)
            Placemark.appendChild(StyleUrl)
            Placemark.appendChild(ExtendedData)
            Placemark.appendChild(Point)
            Folder.appendChild(Placemark)

        # ----------------------------------------
        Placemark = self.doc.createElement('Placemark')

        Name = self.doc.createElement('name')
        Name.appendChild(self.doc.createTextNode('Wayline'))

        Description = self.doc.createElement('description')
        Description.appendChild(self.doc.createTextNode('Wayline'))

        Visibility = self.doc.createElement('visibility')
        Visibility.appendChild(self.doc.createTextNode('1'))

        ExtendedData = self.doc.createElement('ExtendedData')
        ExtendedData.setAttribute('xmlns:mis', 'www.dji.com')

        ExtendedData.appendChild(self.creatElement('mis:altitude', altitude))
        ExtendedData.appendChild(self.creatElement('mis:autoFlightSpeed', flightSpeed))
        ExtendedData.appendChild(self.creatElement('mis:actionOnFinish', actionOnFinish))
        # ExtendedData.appendChild(self.creatElement('mis:headingMode', 'Auto'))  # 朝向下个航点
        ExtendedData.appendChild(self.creatElement('mis:headingMode', 'ControlledByRC'))  # 由遥控器控制
        ExtendedData.appendChild(self.creatElement('mis:gimbalPitchMode', 'UsePointSetting'))
        ExtendedData.appendChild(self.creatElement('mis:powerSaveMode', 'false'))
        ExtendedData.appendChild(self.creatElement('mis:waypointType', 'LineStop'))

        DroneInfo = self.doc.createElement('mis:droneInfo')
        DroneInfo.appendChild(self.creatElement('mis:droneType', 'P4R'))
        DroneInfo.appendChild(self.creatElement('mis:advanceSettings', 'false'))
        DroneInfo.appendChild(self.doc.createElement('mis:droneCameras'))

        DroneHeight = self.doc.createElement('mis:droneHeight')
        DroneHeight.appendChild(self.creatElement('mis:useAbsolute', 'false'))
        DroneHeight.appendChild(self.creatElement('mis:hasTakeoffHeight', 'false'))
        DroneHeight.appendChild(self.creatElement('mis:takeoffHeight', '0.0'))

        DroneInfo.appendChild(DroneHeight)

        ExtendedData.appendChild(DroneInfo)

        LineString = self.doc.createElement('LineString')
        LineString.appendChild(self.creatElement('tessellate', '1'))
        LineString.appendChild(self.creatElement('altitudeMode', 'relativeToGround'))

        coordsText = ''
        for point in wayPointsCoords:
            coordsText += f'{point["lon"]},{point["lat"]},{altitude} '

        LineString.appendChild(self.creatElement('coordinates', coordsText.strip()))

        Placemark.appendChild(Name)
        Placemark.appendChild(Description)
        Placemark.appendChild(Visibility)
        Placemark.appendChild(ExtendedData)
        Placemark.appendChild(self.creatElement('styleUrl', '#waylineGreenPoly'))
        Placemark.appendChild(LineString)

        Document.appendChild(Folder)
        Document.appendChild(Placemark)

        self.kml.appendChild(Document)

        self.doc.appendChild(self.kml)

        filename = dtime + '.kml'
        filepath = os.path.join(kmlFloder, filename)
        fp = open(filepath, 'w')
        self.doc.writexml(fp, indent="", addindent='  ', newl='\n', encoding="UTF-8")
        fp.close()
        return filepath

    def creatElement(self, mod, act, attributeList=None):
        element = self.doc.createElement(str(mod).strip())
        if attributeList is not None:
            for attribute in attributeList:
                element.setAttribute(str(attribute[0]).strip(), str(attribute[1]).strip())
        element.appendChild(self.doc.createTextNode(str(act)))
        return element


def predict(start, points, speed, hover_time):
    maxDis = 0
    total_journey = 0
    total_time = 12

    cur = start
    _points = points.copy()
    _points.append(start)
    for pt in _points:
        dis = geodesic((start['lat'], start['lon']), (pt['lat'], pt['lon'])).m
        maxDis = max(maxDis, dis)
        line = geodesic((cur['lat'], cur['lon']), (pt['lat'], pt['lon'])).m
        total_journey += line
        total_time += float(line) / float(speed)
        total_time += 14 + hover_time
        cur = pt
    total_time += 50 * 2 / float(speed)

    return maxDis, total_journey, total_time


def design(data):
    flight_altitude = float(data['altitude'])
    speed = float(data['speed'])
    hover_time = int(data["hoverTime"])
    start = data['start']
    points = data['points']
    actOnFinish = data['actionOnFinish']
    r = data['radius']
    path = data['path']

    gimbalPitch = round(math.atan(r / (flight_altitude - 3)) * 180 / math.pi - 90)

    # 航迹规划
    WayPointsOrd = WayPoints(radius=r)
    wayPointsorder = WayPointsOrd.design_towards(points, start)

    # 生成航线KML文件
    wpsd = WayPointsCoordsDesign()
    kmlPath = wpsd.makeKmlFile(wayPointsorder, altitude=flight_altitude, flightSpeed=speed, hoverTime=hover_time,
                               actionOnFinish=actOnFinish, gimbalPitch=gimbalPitch, kmlFloder=path)

    maxDis, total_journey, total_time = predict(start, wayPointsorder, speed, hover_time)
    ret = {'flightAltitude': flight_altitude,  # 飞行高度
           'radius': r,  # 航点半径
           'gimbalPitch': gimbalPitch,  # 俯仰角
           'farthestDistance': f"{maxDis:.2f}",  # 最远距离
           'flightDistance': f"{total_journey:.2f}",  # 飞行总距离
           'timecost': total_time,  # 预计耗时
           'points': wayPointsorder,  # 飞行航点
           'path': kmlPath}  # kml存储路径
    print(json.dumps(ret))


if __name__ == "__main__":


    data = {
        "points": [{
            "id": "3304211052071929",
            "lon": 120.896214689,
            "lat": 30.9157438184,
            "altitude": 50.0,
            "direction": 2,
            "match": []
        }, {
            "id": "3304211052070788",
            "lon": 120.896217375,
            "lat": 30.9158275551,
            "altitude": 50.0,
            "direction": 3,
            "match": [3304211052072105]
        }, {
            "id": "3304211052071931",
            "lon": 120.896224053,
            "lat": 30.9159021463,
            "altitude": 50.0,
            "direction": 5,
            "match": ["3304211052070790"]
        }],
        "path": "./KML",
        "speed": 6.0,
        "hoverTime": 0,
        "radius": 25.0,
        "actionOnFinish": "GoHome",
        "altitude": 25.0,
        "start": {
            "lon": 120.89665871247377,
            "lat": 30.915756274594212
        }
    }

    # points = data["points"]


    design(data)
    # design(json.loads(sys.argv[1]))
