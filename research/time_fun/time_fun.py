# -*- coding: UTF-8 -*-
import time, datetime
from functools import wraps
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def time_me(fn):
  def _wrapper(*args, **kwargs):
    start = time.clock()
    fn(*args, **kwargs)
    print "%s cost %s second"%(fn.__name__, time.clock() - start)
    return _wrapper


import time
from functools import wraps

def fn_timer(function):
  @wraps(function)
  def function_timer(*args, **kwargs):
    t0 = time.time()
    result = function(*args, **kwargs)
    t1 = time.time()
    print ("Total time running %s: %s seconds" %
       (function.func_name, str(t1-t0))
       )
    return result
  return function_timer

@fn_timer
def test():
  print "test"
  return 0


@fn_timer
def random_sort(n):
  return sorted([random.random() for i in range(n)])

def get_current_datestr():
  dt = (datetime.datetime.now() - datetime.timedelta(days =0)).strftime("%Y-%m-%d")
  return dt

def get_current_timestr():
  dt = (datetime.datetime.now() - datetime.timedelta(days =0)).strftime("%Y-%m-%d %H:%M:%S")
  return dt

def get_yesterday_datestr():
  dt = (datetime.datetime.now() - datetime.timedelta(days =1)).strftime("%Y%m%d")
  return dt

def datetime_timestamp(dt):
   #dt为字符串
   #中间过程，一般都需要将字符串转化为时间数组
   time.strptime(dt, '%Y-%m-%d %H:%M:%S')
   ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
   #将"2012-03-28 06:53:40"转化为时间戳
   s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
   return int(s)

def time_diff(t1, t2):
    t1 = datetime_timestamp(t1)
    t2 = datetime_timestamp(t2)
    diff = abs(t1 - t2)/(3600*24*365.0)
    return round(diff, 2)


if __name__ == '__main__':
  random_sort(100)