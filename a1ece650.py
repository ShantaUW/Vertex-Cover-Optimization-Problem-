import sys
import re

from Find_Intersection_Final import line,point,intersect,Segment,partly,is_same_Line

#Global_Variables
RoadNameList=[]
RoadsDict={}
invalid_input_from_user = []

#Validity Checker
def validity(i):
    if re.match(r"^a\s+(\"(([\w]+)\s?)+\")\s+(((\(-?\d+,-?\d+\))\s?)\s?)+$", i):
        add_Roads(i)
    elif re.match(r"^c\s+(\"(([\w]+)\s?)+\")\s+(((\(-?\d+,-?\d+\))\s?)\s?)+$", i):
        change_Roads(i)
    elif re.match(r"^r\s+(\"(([\w]+)\s?)+\")\s?$", i):
        remove_Roads(i)
    elif re.match(r"^g\s?$", i):
        graph_Generator()
    elif re.match(r"\n",i):
        print ('Error: Please input road data correctly.')
    else:
        print ('Error: Input data format unrecognised.')
#For User Input
def getStreetName(data):
    data = re.search('("(.*?)"|\'(.*?)\')', data)
    name = data.group(0)
    return name[1:len(name) - 1]

def getStreetCord(data):
    find_coordinate = re.findall(r'(\(.*?\))', data)
    return find_coordinate
#For processing
def add_Roads(data):
    if str(getStreetName(data).lower().strip()) in (RoadsDict.keys()):
        print ('Error: Road already exists')
    else:
        get_road_coordinate_details(data)

def get_road_coordinate_details(data):
    RoadsDict[str(getStreetName(data)).lower().strip()] = getStreetCord(data)
    return RoadsDict

def change_Roads(data):
    if str(getStreetName(data).lower().strip()) in (RoadsDict.keys()):
        RoadsDict[str(getStreetName(data)).lower().strip()] = getStreetCord(data)
    else:
        print ('Error: Can not update. Road not found.')
def remove_Roads(data):
    if str(getStreetName(data).lower().strip()) in (RoadsDict.keys()):
        del RoadsDict[str(getStreetName(data)).lower().strip()]
    else:
        print ('Error: Road Name is not found in dictionary. Can not remove: ', data)
#For graph

def graph_Generator():
    lines_list_roads = Create_Lines_From_Road_Coordinates()
    resultVertices, resultVerticesList = find_Intesection(lines_list_roads)
    resultVertices = set(resultVertices)
    resultVertices_List = list(resultVertices)

    f_vertices(resultVertices_List)
    verticesList = findingEdge(resultVertices_List, get_List_From_Matrix(lines_list_roads),resultVerticesList)
    last_setEdge(verticesList)

def f_vertices(data):
    x = 0
    strig = " "
    for j in data:
        k = get_Points_From_String(j)
        x=x+1
        stg = " {}: {} ".format(x, k)
        strig = strig + "\n" + stg

    print "V = {" + strig + "\n}"


def last_setEdge(data):
    Ed = []
    newE = " "
    for edge in data:
        data = tuple(edge)
        Ed.append(data)
    for items in Ed:
        if items == Ed[-1]:
            newE = newE + "\n" + str(items)
        else:
            newE = newE + "\n" + str(items) + ","
    print 'E = {', newE.replace('(', '<').replace(')', '>').replace(' ', ''), '\n}'

def get_Points_From_String(point_string):
    coordinate = re.split(',', point_string)
    return point(coordinate[0], coordinate[1])


def findingEdge(resultVertices_List, lines_List, resultVerticesList):
    verticesList = []
    for i in range(len(resultVertices_List) - 1):
        point1 = get_Points_From_String(resultVertices_List[i])
        for j in range(i + 1, len(resultVertices_List)):
            point2 = get_Points_From_String(resultVertices_List[j])
            if havingEdge(point1, point2, lines_List):
                if (resultVerticesList[resultVertices_List[i]] or resultVerticesList[resultVertices_List[j]]):
                    if not any_Intersection_Point(point1, point2, resultVerticesList):
                        verticesList.append([i + 1, j + 1])

    return verticesList

def any_Intersection_Point(point1, point2, resultVerticesList):
    for key, value in resultVerticesList.iteritems():
        if (value):
            point = get_Points_From_String(key)
            if ((not is_SamePoint(point, point1)) and (not is_SamePoint(point, point2))):
                lies_Between = Segment(point1, point2).is_Between(point)
                if lies_Between:
                    return True
    return False
def is_SamePoint(point1,point2):
    if(point1.x == point2.x and point1.y == point2.y):
        return True
    return False

def havingEdge(point1, point2, lines_List):
    for line in lines_List:
        lies_Between = Segment(line.src, line.dst).is_Between(point1) and Segment(line.src, line.dst).is_Between(point2)
        if lies_Between:
            return True
    return False


def get_List_From_Matrix(road_Lines):
    l_s = []
    for r_s in road_Lines:
        for i in r_s:
            l_s.append(i)
    return l_s

def Create_Lines_From_Road_Coordinates():
    lines_list_roads = []

    for key, values in RoadsDict.iteritems():
        lines_list = []
        for p in range(len(values) - 1):
            coordinate_1 = values[p][1:len(values[p]) - 1]
            coordinate_2 = values[p + 1][1:len(values[p + 1]) - 1]
            coordinate_1 = re.split(',', coordinate_1)
            coordinate_2 = re.split(',', coordinate_2)
            li = line(point(coordinate_1[0], coordinate_1[1]), point(coordinate_2[0], coordinate_2[1]))
            lines_list.append(li)
        lines_list_roads.append(lines_list)

    return lines_list_roads

def find_Intesection(lines_list_roads):
    results = []
    resultVerticesList={}
    for l in range(len(lines_list_roads) - 1):
        lines_List = lines_list_roads[l]
        for m in range(len(lines_List)):
            line = lines_List[m]
            road_List_To_Compare = get_List_From_Matrix(lines_list_roads[l + 1:len(lines_list_roads)])
            for n in range(len(road_List_To_Compare)):
                intesection_Line = road_List_To_Compare[n]
                intersect_Point = intersect(line, intesection_Line)

                if (is_same_Line(intesection_Line, line) and (intersect_Point.x == 0 and intersect_Point.y == 0)):
                    intersect_String = str(line.src.x) + ',' + str(line.src.y)
                    results.append(intersect_String)

                    if not resultVerticesList.has_key(intersect_String):
                        resultVerticesList[intersect_String] = True

                    intersect_String = str(line.dst.x) + ',' + str(line.dst.y)
                    results.append(intersect_String)

                    if not resultVerticesList.has_key(intersect_String):
                        resultVerticesList[intersect_String] = True

                    intersect_String = str(intesection_Line.src.x) + ',' + str(intesection_Line.src.y)
                    results.append(intersect_String)

                    if not resultVerticesList.has_key(intersect_String):
                        resultVerticesList[intersect_String] = True

                    intersect_String = str(intesection_Line.dst.x) + ',' + str(intesection_Line.dst.y)
                    results.append(intersect_String)

                    if not resultVerticesList.has_key(intersect_String):
                        resultVerticesList[intersect_String] = True

                if (not (intersect_Point.x == 0 and intersect_Point.y == 0)):
                    intersection_validity = Segment(intesection_Line.src, intesection_Line.dst).is_Between(
                        intersect_Point) and Segment(line.src, line.dst).is_Between(intersect_Point)

                    if intersection_validity:
                        intersect_String = str(intersect_Point.x) + ',' + str(intersect_Point.y)
                        results.append(intersect_String)

                        if not resultVerticesList.has_key(intersect_String):
                            resultVerticesList[intersect_String] = True

                        intersect_String = str(line.src.x) + ',' + str(line.src.y)
                        results.append(intersect_String)

                        if not resultVerticesList.has_key(intersect_String):
                            resultVerticesList[intersect_String] = False

                        intersect_String = str(line.dst.x) + ',' + str(line.dst.y)
                        results.append(intersect_String)

                        if not resultVerticesList.has_key(intersect_String):
                            resultVerticesList[intersect_String] = False

                        intersect_String = str(intesection_Line.src.x) + ',' + str(intesection_Line.src.y)
                        results.append(intersect_String)

                        if not resultVerticesList.has_key(intersect_String):
                            resultVerticesList[intersect_String] = False

                        intersect_String = str(intesection_Line.dst.x) + ',' + str(intesection_Line.dst.y)
                        results.append(intersect_String)

                        if not resultVerticesList.has_key(intersect_String):
                            resultVerticesList[intersect_String] = False
                    else:
                        intersect_String = str(line.src.x) + ',' + str(line.src.y)
                        if not resultVerticesList.has_key(intersect_String):
                            resultVerticesList[intersect_String] = False

                        intersect_String = str(line.dst.x) + ',' + str(line.dst.y)
                        if not resultVerticesList.has_key(intersect_String):
                            resultVerticesList[intersect_String] = False

                        intersect_String = str(intesection_Line.src.x) + ',' + str(intesection_Line.src.y)
                        if not resultVerticesList.has_key(intersect_String):
                            resultVerticesList[intersect_String] = False

                        intersect_String = str(intesection_Line.dst.x) + ',' + str(intesection_Line.dst.y)
                        if not resultVerticesList.has_key(intersect_String):
                            resultVerticesList[intersect_String] = False
                else:
                    intersect_String = str(line.src.x) + ',' + str(line.src.y)
                    if not resultVerticesList.has_key(intersect_String):
                        resultVerticesList[intersect_String] = False
                    intersect_String = str(line.dst.x) + ',' + str(line.dst.y)

                    if not resultVerticesList.has_key(intersect_String):
                        resultVerticesList[intersect_String] = False
                    intersect_String = str(intesection_Line.src.x) + ',' + str(intesection_Line.src.y)

                    if not resultVerticesList.has_key(intersect_String):
                        resultVerticesList[intersect_String] = False
                    intersect_String = str(intesection_Line.dst.x) + ',' + str(intesection_Line.dst.y)

                    if not resultVerticesList.has_key(intersect_String):
                        resultVerticesList[intersect_String] = False

    return results, resultVerticesList


#main
def main():
    while True:
        line = sys.stdin.readline()
        try:

            if line == '':
                break

            else:
                b = line.strip()
                validity(b)

        except:
            print("Error,Please give input correctly.")
    sys.exit(0)

if __name__ == '__main__':
    main()