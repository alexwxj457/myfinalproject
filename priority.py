import traci  # noqa

def priority(arr_time,time_set):
   a=arr_time+5-time_set[1]
   b=time_set[-1]-arr_time+5
   if a<b:
      return time_set[1],arr_time+5,0
   if a>=b:
      return arr_time-5, time_set[-1],1
