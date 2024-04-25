import traci  # noqa
from sigal import light
import matplotlib.pyplot as plt
from judgment import judgment
# from flow import flow
# from sigal import light,youxian
# import  math
import traci.constants as tc
from priority import priority
from excel import excel

def bus(vehicle_ids):
    vehicle_ids = [vehicle_id for vehicle_id in vehicle_ids if vehicle_id[4] == "myType"]  # 过滤掉非公交车辆
    return vehicle_ids

def map(x,y,z,name):
    plt.plot(x, y, marker='o', linestyle='-')
    plt.plot(x, z, marker='o', linestyle='-')
    # 添加标题和标签
    plt.title('Sample Line Plot')
    plt.xlabel('X-axis Label')
    plt.ylabel('Y-axis Label')
    plt.savefig(f'{name}.png')
    # 显示图形
    plt.show()

# 指定启动SUMO的命令和参数
sumoCmd = ['sumo-gui', '-c', "1.sumocfg"]
traci.start(sumoCmd)
a = ()
b = ()
v=[]
t=[]
x=[]
n=[]

sign = 3
st = end = 0
yxtime = 5
phase_list = ["rrrrrGGGGGGGGGGrr", "rrrrrGGrrrrrrrrGG", "GGGGGGGrrrrrrrrrr"]
phase_time_list = [10, 18, 25]
light_set, time_set = light(phase_list, phase_time_list)
print(light_set, time_set)
bus_start= [0,40, 80, 120]
bus_list= ["bus0","bus1","bus2","bus3"]
for i in range(len(bus_list)):
    name=f"{bus_list[i]}"
    traci.vehicle.add(name, "r0", typeID="myType",depart=bus_start[i], departLane="best",departSpeed=0)#生成公交
for step in range(150000):
    traci.simulationStep()
    time0 = traci.simulation.getTime()  # 获取仿真时间,s
    time = time0 % time_set[-1]  # 确定周期数
    num = time0 // time_set[-1]
    timenow = time0 - time_set[-1] * time  # 确定周期内时间
    timein = light_set[time_set.index(min([x for x in time_set if x > time])) - 1]  # 确定当前相位
    if st == 0:
        traci.trafficlight.setRedYellowGreenState("J1", timein)  # 设置交叉口的信号灯状态
    # vehicle_ids = traci.inductionloop.getLastStepVehicleIDs("det_0")
    vehicle_ids = traci.inductionloop.getVehicleData("det_2") + traci.inductionloop.getVehicleData(
        "det_0") + traci.inductionloop.getVehicleData("det_1")
    vehicle_ids_es = traci.inductionloop.getVehicleData("det_3") + traci.inductionloop.getVehicleData(
        "det_4") + traci.inductionloop.getVehicleData("det_5")
    vehicle_leave = traci.inductionloop.getVehicleData("det_11")+traci.inductionloop.getVehicleData("det_00")+traci.inductionloop.getVehicleData("det_22")
    vehicle_ids = bus(vehicle_ids)
    vehicle_ids_es = bus(vehicle_ids_es)
    vehicle_leave = bus(vehicle_leave)  # 过滤掉非公交车辆
    # if time0>10 and time0<20:
    # traci.trafficlight.setRedYellowGreenState("J1", "rrrrrrrrrrrrrrrrr")
    if vehicle_ids and vehicle_ids[0][0] != a:
        a = vehicle_ids[0][0]  # 获取车辆ID
        print(a)
        arr_time = time + 12
        if arr_time > time_set[-1]:
            arr_time = time + 12 - time_set[-1]
        print(judgment(arr_time, time_set, light_set))
        if judgment(arr_time, time_set, light_set):
            yyy=traci.lanearea.getLastStepVehicleNumber("e2det_1")
            print(yyy)
            st, end, sign = priority(arr_time, time_set)
            print(st, end, sign, time_set[-1])
            st = st + num * time_set[-1]
            end = end + num * time_set[-1] + sign * (time_set[1] - time_set[0])
        # print(f"检测器 'det_0' 检测到的车辆ID: {a}")
        # print(f"当前时间: {time0}")
        # print(f"当前相位: {timein}")
        # print(f"到达时间: {arr_time}")
        print(f"开始时间：{st}")
        print(f"结束时间：{end}")
        if sign==0:
            print("提前")
        if sign==1:
            print("延长")
        if sign==3:
            print("无优先")
    if vehicle_leave and vehicle_leave[0][0] != b:
        b = vehicle_leave[0][0]
        if sign!=3:
            data={
                'time':t,
                'speed':v,
                'num':n,
                'position':x
            }
            excel(data, b)
            map(x, v, n,b)

        t = []
        v = []
        n = []
        x = []
        print(f"检测器 'det_11' 检测到的车辆ID: {vehicle_leave}")
    if not st == 0 and not end == 0:
        if a!=b:
            try:
               # print(v)
               v.append(traci.vehicle.getSpeed(a))
               t.append(time0)
               x.append(-traci.vehicle.getPosition(a)[0]-16.8)
               n.append(len([x for x in  traci.lanearea.getLastStepVehicleIDs("e2det_1") if traci.vehicle.getPosition(x)[0]>traci.vehicle.getPosition(a)[0]]))
            except:
                pass
        #sign=0表示延长绿灯时间，sign=1表示提前绿灯时间
        #延长绿灯时间需要添加黄灯时间，防止交通灯的突然变化
        #提前绿灯时间不需要添加黄灯时间
        if st < time0 < end - 2 and sign == 0:
            traci.trafficlight.setRedYellowGreenState("J1", "rrrrrGGGGGGGGGGrr")
        if st < time0 < end and sign == 1:
                traci.trafficlight.setRedYellowGreenState("J1", "rrrrrGGGGGGGGGGrr")
        if end - 2 <= time0 < end + 2 and sign == 0:
            traci.trafficlight.setRedYellowGreenState("J1", "rrrrryyyyyyyyyyrr")
    # 优化结束后，将st和end置0
    if time0 >= end + 2 and sign == 0:
        st = end = 0
        sign=3


    if time0 >= end and sign == 1:
        st = end = 0
        sign=3


    # if not priority_time and settime!=0:
    #     settime = 0
    # yxtime=0
    tls_state = traci.trafficlight.getRedYellowGreenState("J1")  # 获取交叉口的信号灯状态
    # print(settime)
    # if vehicle_ids_es:
    #     print(f"检测器 'det_3' 检测到的车辆ID: {vehicle_ids_es}")
