def light(phase_list,phase_time_list):#设置信号灯
    yelltime=4#黄灯时间
    yellow_list=[x.replace('G','y') for x in phase_list]#将绿灯变为黄灯
    light_list=[]
    time_gap_list=[0]
    time_list=[]
    for i in range(len(yellow_list)):
        light_list.append(phase_list[i])
        light_list.append(yellow_list[i])#每个相位之后加入黄灯
        time_gap_list.append(phase_time_list[i])
        time_gap_list=time_gap_list+[yelltime]#加入黄灯时间，得到个相位及黄灯的保持时间
    for i in range(len(time_gap_list)):
        x=(2*time_gap_list)[:i+1]
        time_list.append(sum(x))#叠加得到单个周期内各相位及黄灯开始时间

    return light_list,time_list#输出相位和时间的组合
# x=[ "rrrrrGGGrrrrrrrGGGrr","rrrrrrrrGGrrrrrrrrGG","GGGrrrrrrrGGGrrrrrrr","rrrGGrrrrrrrrGGrrrrr"]
# y=[33,15,33,15]
# print(light(x,y))
# # import time

import time

# def light_cycle(t):
#     tsl_shdaj="dasdas"
#
#
#
#
def youxian(time, youxian_time, youxian_light, light_list, time_list):#需要优化时，导入当前时间，优化后目标相位及时间，信号灯的原始相位和时间

    n = light_list.index(youxian_light)#找到优化目标相位在原始相位列表的位置
   #找到当前时刻在原始相位时间列表的前后元素的位置位置
    mmm=time_list.index(max([x for x in time_list if x <= time]))
    sss=time_list.index(min([x for x in time_list if x > time]))
    #需要分两种情况，在单个相位内，需要优化的时刻在优化目标相位的前面还是后面
    #在前面
    if time < time_list[n]:
            vi = [x + youxian_time for x in [time] + time_list[sss:n + 1]]#获取原始时间列表内处于目前时间和目标相位结束时间范围内的时间，加上优化时间
            vi.insert(1,vi[0]+3)#给优化的相位之后加入绿灯。优化相位的绿灯时间大于优化时间-黄灯时间，这里需要加上一个黄灯防止交通灯的突然变化

            ll = [time,time+3] + vi + [time_list[n + 1]]#[time,time+3]在优化相位之前加入当前相位的黄灯时间，防止交通灯的突然变化
            t = light_list[mmm:n + 1]
            positions = [index for index, char in enumerate(light_list[n]) if char == "G"]
            string_list = list(light_list[mmm + 1])
            for i in positions:
                string_list[i]="r"
            modified_string = "".join(string_list)
            t = [modified_string] + [light_list[n]] + [light_list[n + 1]] + t  # 得到对应的信号灯相位插入相位的黄灯时间
    #在后面
    else:
         #这里比较复杂，举个例子，例如现在的输入为(103,6,'rrrrrrrrGGrrrrrrrrGG',light_set,time_set)
         # light_set, time_set=['rrrrrGGGrrrrrrrGGGrr', 'rrrrryyyrrrrrrryyyrr',
          # 'rrrrrrrrGGrrrrrrrrGG', 'rrrrrrrryyrrrrrrrryy',
          # 'GGGrrrrrrrGGGrrrrrrr', 'yyyrrrrrrryyyrrrrrrr',
          # 'rrrGGrrrrrrrrGGrrrrr', 'rrryyrrrrrrrryyrrrrr'],
          # [0, 33, 36, 51, 54, 87, 90, 105, 108])
          v2 = time_list[1:n + 1]#v2=[33, 36]，及列表的第二个元素到目标优化相位的开始时间
          vi=time_list[sss:]#vi=[87, 90, 105, 108]，即当前时间之后的下一个相位开始时间到就列表末尾
          v2 = [x + youxian_time for x in v2]
          vi = [x + youxian_time for x in [time]+vi]#加上优化时间
          vi=vi+v2#合并列表
          vi.insert(1,vi[0]+3)#黄灯时间，同上

          v2=[num - time_list[-1] if num >time_list[-1]  else num for num in vi]#大于周期元素减去周期
          first_greater_than_ten = vi.index(min(num for num in vi if num>=time_list[-1]))#找到第一个超过周期的元素，并在她后面加个0
                                                                                         #目的是当一个周期结束，time继续从0开始，需要添加一个时间段，
                                                                                         #  保持和前一个时间段信号灯一致
          v2.insert(first_greater_than_ten, 0)
          ll=[time,time+3] + v2 + [time_list[n+1]]    #同上

          t = light_list[mmm:]
          # positions = [index for index, char in enumerate(light_list[n]) if char == "g"]
          # gligh = light_list[mmm + 1][:positions[0]] + len(positions) * "g" + light_list[mmm + 1][positions[-1] + 1:]
          positions = [index for index, char in enumerate(light_list[n]) if char == "G"]
          string_list = list(light_list[sss])
          for i in positions:
                string_list[i] = "r"
          modified_string = "".join(string_list)
          t =[modified_string] + [light_list[n], light_list[n + 1]] + t+light_list[0:n+1]  # 插入相位的黄灯时间
          t.insert(first_greater_than_ten+1, t[first_greater_than_ten+1])


    return t,ll
# phase_list = ["rrrrrGGGrrrrrrrGGGrr", "rrrrrrrrGGrrrrrrrrGG", "GGGrrrrrrrGGGrrrrrrr", "rrrGGrrrrrrrrGGrrrrr"]
# phase_time_list = [33, 15, 33, 15]
# light_set, time_set = light(phase_list, phase_time_list)
# x=youxian(70,6,'rrrrrrrrGGrrrrrrrrGG',light_set,time_set)
# print(x)
# #
