from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from redisconect.models import redisInfo, operationlog
from redis.sentinel import Sentinel
from rediscluster import RedisCluster
from redis import Redis
import time
import json


class RedisClient(WebsocketConsumer):
    def connect(self):
        try:
            self.redisId = self.scope['query_string']
            self.redisinfo = redisInfo.objects.get(id=self.redisId)
            self.redistype = self.redisinfo.redistype
            self.nodelist = self.redisinfo.nodelist
            self.mastername = self.redisinfo.mastername
            if self.redistype == 'Sentinel':
                cluster_nodes = [(i.split(':')[0], int(i.split(':')[1])) for i in self.nodelist.split(',')]
                con = Sentinel(cluster_nodes, socket_timeout=0.5)
                self.connect = con.master_for(self.mastername, decode_responses=False)
            elif self.redistype == "Cluster":
                cluster_nodes = [{"host": i.split(':')[0], "port":int(i.split(':')[1])} for i in self.nodelist.split(',')]
                self.connect = RedisCluster(startup_nodes=cluster_nodes, decode_responses=False)
            elif self.redistype == "Single":
                host = self.nodelist.split(':')[0]
                port = int(self.nodelist.split(':')[1])
                self.connect = Redis(host, port, decode_responses=False)
            self.accept()
            self.send(json.dumps({"message": "redis connect successful"}))
        except:
            self.accept()
            self.send(json.dumps({"message": "redis connect failed"}))
            self.disconnect(400)

    def disconnect(self, code):
        self.close()

    def receive(self, text_data):
        try:
            text_data = json.loads(text_data)
            command = text_data['cmd0'].lower()
            res = ''
            if command == "close":
                res = "connect closed"
                self.send(text_data=json.dumps({
                    "message": res
                }))
                self.disconnect(400)
            elif command == "info":
                res = self.redis_info()
            elif command == "get":
                res = self.redis_get(text_data['cmd1'])
            elif command == 'hget':
                res = self.redis_hget(text_data['cmd1'], text_data['cmd2'])
            elif command == "hgetall":
                res = self.redis_hgetall(text_data['cmd1'])
            elif command == "slowlog":
                if 'cmd1' in text_data.keys():
                    res = self.redis_slowlog(int(text_data['cmd1']))
                else:
                    res = self.redis_slowlog()
            elif command == "slowloglen":
                res = self.redis_slowloglen()
            elif command == "slowlogrest":
                res = self.redis_slowlogres()
            elif command == "scan":
                res = self.redis_scan(text_data['cmd1'])
            elif command == 'hscan':
                res = self.redis_hscan(text_data['cmd1'], text_data['cmd2'])
            else:
                res = "指令错误"
        except KeyError:
            res = "缺少参数"
        except Exception as e:
            res = "无法获取数据"
        finally:
            createcontent = operationlog.objects.create(
                redisname=self.redisinfo.projectname + '-' + self.redisinfo.redisname,
                operation=text_data,
                operator=self.redisinfo.director
            )
            if res == '':
                res = "数据为空"
            self.send(text_data=json.dumps({
                "message": res
            }))

    def redis_info(self):
        res = self.connect.info()
        if self.redistype == "Cluster":
            res_o = ''
            for k, v in res.items():
                res_o = res_o + "node: " + k + '\n'
                for j, p in v.items():
                    res_o = res_o + json.dumps(j) + ": " + json.dumps(p) + '\n'
                res_o = res_o + '\n'
            res = res_o
        return res

    def redis_get(self, keys):
        res = self.connect.get(keys)
        if res != '':
            return res.decode()
        else:
            return "No Data"

    def redis_hget(self, name, keys):
        res = self.connect.hget(name, keys)
        if res != '':
            return res.decode()
        else:
            return "No Data"

    def redis_hgetall(self, name):
        res = self.connect.hgetall(name)
        res_o = {}
        for k, v in res.items():
            res_o[k.decode()] = v.decode()
        if res_o != '':
            return res_o
        else:
            return "数据为空"

    def redis_slowlog(self, num=None):
        res = self.connect.slowlog_get()
        if len(res) > 0 and self.redistype == "Cluster":
            res_o = ''
            for k, v in res.items():
                for j in v:
                    slog = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(j['start_time'])) + ' [' + j['command'].decode() + '] ' + str(j['duration']) + ' ' + k + '\n'
                    res_o = res_o + slog
        elif len(res) > 0:
            res_o = ''
            for i in range(len(res)):
                for k, v in res[i].items():
                    slog = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(res[i]['start_time'])) + ' [' + res[i]['command'].decode() + '] ' + str(res[i]['duration']) + ' ' + '\n'
                    res_o = res_o + slog
        else:
            res_o = "NO Data"
        return res_o

    def redis_slowloglen(self):
        res = self.connect.slowlog_len()
        return res

    def redis_slowlogres(self):
        self.connect.slowlog_reset()
        return "slowlog reset successful"

    def redis_scan(self, keys):
        res = [k.decode() for k in self.connect.scan_iter(keys, count=1000)]
        if res != '':
            return res
        else:
            return "No Data"

    def redis_hscan(self, name, keys):
        res = self.connect.hscan_iter(name, keys, count=1000)
        res_o = ''
        for k in res:
            res_o = res_o + k[0].decode() + ": " + k[1].decode() + '\n'
        if res_o != '':
            return res_o
        else:
            return "No Data"
