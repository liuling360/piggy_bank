#coding=utf-8
import time
import os
import sys
import json
import redis
import logging
from time_fun import fn_timer

REDIS_URL    = 'xxx'
REDIS_PORT   = 6379

class RedisUtil(object):

    def __init__(self):
        self._redis_pool = redis.ConnectionPool(host=REDIS_URL, port=REDIS_PORT)

    def get_redis(self) :
        return redis.StrictRedis(connection_pool = self._redis_pool)

    @fn_timer
    def get_test(self, num=1000, pipe=False) :
        key = 'test-0'
        redis = self.get_redis()
        if pipe == False:
            for i in range(0, num):
                redis.get(key)
        else :
            pipe = redis.pipeline()
            for i in range(0, num):
                pipe.get(key)
            results = pipe.execute()
            print results

    @fn_timer
    def set_test(self, num=1000, pipe=False) :
        key = 'test-0'
        redis = self.get_redis()
        if pipe == False:
            for i in range(0, num):
                redis.set(key, 'hiupahjkdipajioapjpai')
        else :
            pipe = redis.pipeline()
            for i in range(0, num):
                pipe.set(key, 'hiupahjkdipajioapjpai')
            pipe.execute()


    @fn_timer
    def zadd_test(self, num=1000, pipe=False) :
        key = 'zadd-test-0'
        value = 'f382460a7c7c3597ef34b139ecda7e59'
        redis = self.get_redis()
        if pipe == False:
            for i in range(0, num):
                redis.zadd(key, i, value + str(i))
        else :
            pipe = redis.pipeline()
            for i in range(0, num):
                pipe.zadd(key, i, value + str(i))
            pipe.execute()

    @fn_timer
    def hset_test(self, num=1000, pipe=False) :
        key = 'hash-test-0'
        v = 'f382460a7c7c3597ef34b139ecda7e59'
        value = ''
        for i in range(0, 100):
           value += v
        redis = self.get_redis()
        if pipe == False:
            for i in range(0, num):
                redis.hset(key, str(i), value)
        else :
            pipe = redis.pipeline()
            for i in range(0, num):
                pipe.hset(key, str(i), value)
            pipe.execute()


    @fn_timer
    def prepare_history_flow(self, num=1000):
        try:
            redis = self.get_redis()
            pipe = redis.pipeline()
            key_history = 'history-set-test'
            pipe.delete(key_history)
            pipe.execute()

        except Exception, e:
            print e

    @fn_timer
    def prepare_process_flow(self, num=1000):
        time_stamp = 1523514396
        v = 'f382460a7c7c3597ef34b139ecda7e59'
        value = ''
        for i in range(0, 100):
           value += v
        try:
            redis = self.get_redis()
            pipe = redis.pipeline()
            key_history = 'history-set-test'
            key_result_ids = 'result-id-set-test'
            key_result_objs = 'result-obj-hash-test'
            pipe.delete(key_history)
            pipe.delete(key_result_ids)
            pipe.delete(key_result_objs)
            #for i in range(0, num/2):
            #    pipe.zadd(key_history, '10000000000', str(2 * i))
            for i in range(0, num):
                pipe.zadd(key_result_ids, (float)(i) / 1000000000000.0 + 1, i)
            for i in range(0, num):
                pipe.hset(key_result_objs, str(i), value)
            pipe.execute()

        except Exception, e:
        # 发生watcherror时业务应该怎样处理，丢弃事务或者重试
            print e




    @fn_timer
    def test_process_flow(self, x=10):
        time_stamp = 1523514396
        try:
            redis = self.get_redis()
            pipe = redis.pipeline()
            key_history = 'history-set-test'
            key_result_ids = 'result-id-set-test'
            key_result_ids_temp = 'result-id-set-test-temp'
            key_result_objs = 'result-obj-hash-test'
            pipe.watch(key_result_ids, key_history)
            pipe.multi()
            pipe.zunionstore(key_result_ids_temp, {key_result_ids:1, key_history:0}, aggregate='MIN')
            pipe.zremrangebyscore(key_result_ids_temp, 0, 0)
            pipe.zremrangebyrank(key_result_ids_temp, x, -1)
            pipe.zrangebyscore(key_result_ids_temp, '-inf', '+inf')
            pipe.zunionstore(key_history, {key_result_ids_temp:time_stamp, key_history:1}, aggregate='MAX')
            pipe.zremrangebyrank(key_history, 800, -1)
            results = pipe.execute()
            pipe.unwatch()
            #results = redis.zrange(key_result_ids, 0, 10, withscores=True)
            #results = redis.zrange(key_history, -10, -1, withscores=True)
            #results = redis.zrange(key_result_ids_temp, 0, x - 1, withscores=True)
            print results
        #except redis.exceptions.WatchError:
        except Exception, e:
        # 发生watcherror时业务应该怎样处理，丢弃事务或者重试
            print e
            pass

    def test(self) :
        self.set_test(num=1000, pipe=True)
        self.get_test(num=1000, pipe=True)
        #self.set_test(num=1000)
        #self.get_test(num=1000)
        self.zadd_test(num=1000, pipe=True)
        self.zadd_test(num=1000)
        self.hset_test(num=1000, pipe=True)
        self.hset_test(num=1000)
        print "\n\n\n"

if __name__ == '__main__':
    redis_util = RedisUtil()
    #redis_util.test()
    redis_util.prepare_process_flow(num=1000)
    print "======================================================"
    for i in range(0, 1000):
        redis_util.test_process_flow()