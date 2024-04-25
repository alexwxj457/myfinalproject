def judgment(arr_time,time_set,light_set):
    arr_light = light_set[time_set.index(min([x for x in time_set if x > arr_time])) - 1]  # 到达相位
    print(f"到达相位: {arr_light}")
    print(f"到达时间: {arr_time}")
    if arr_light != "rrrrrGGGGGGGGGGrr" or time_set[1]<arr_time <time_set[2]-2:
        return True
    else:
        return False
