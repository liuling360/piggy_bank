package main

import (
	"time"
	"log"
	"os"
	"fmt"
	".."
	"github.com/pinterest/bender"
	bthrift "github.com/pinterest/bender/thrift"
	"git.apache.org/thrift.git/lib/go/thrift"
	"github.com/pinterest/bender/hist"
	//"io/ioutil"
	//"github.com/widuu/gojson"
	//"math/rand"
	"bufio"
	//"io"
	"strings"
	"strconv"
	"io"
)

func SyntheticRecommendRequests() chan interface{}{
	c := make(chan interface{}, 5000)

	//f, err := os.Open("output.log_output")
	//f, err := os.Open("22")
	f, err := os.Open("new-sample.log")
	if err != nil {
		fmt.Print(err)
	}

	buf := bufio.NewReader(f)
	for ; len(c)<4999; {
		line, error := buf.ReadString('\n')
		line = strings.TrimSpace(line)
                
                if error != nil || io.EOF == error {
		        break
		}
		lineArray := strings.Split(line, ", ")
		var infoMap map[string]string
		/* 创建集合 */
		infoMap = make(map[string]string)
		for _, info := range lineArray {
			everyInfo := strings.Split(info, ":")
			if 1 == len(everyInfo) {
				infoMap[everyInfo[0]] = ""
			}

			if 3 == len(everyInfo) {
				infoMap["channel"] = everyInfo[1] + everyInfo[2]
			}
			infoMap[everyInfo[0]] = everyInfo[1]
		}

		var request recommend.Request

		_, ok := infoMap["userId"]
		if ok {
			request.UserId = infoMap["userId"]
		}else {
			request.UserId = ""
		}

		_, ok = infoMap["uuid"]
		if ok {
			request.UUID = infoMap["uuid"]
		}

		_, ok = infoMap["country"]
		if ok {
			request.Country = infoMap["country"]
		}

		_, ok = infoMap["channel"]
		if ok {
			request.Channel = infoMap["channel"]
		}

		_, ok = infoMap["yuyan"]
		if ok {
			request.Yuyan = infoMap["yuyan"]
		}

		_, ok = infoMap["num"]
		if ok {
			b,_ := strconv.Atoi(infoMap["num"])
			request.Num = int32(b)
		}

		_, ok = infoMap["finalId"]
		if ok {
			request.FinalId = infoMap["finalId"]
		}

		_, ok = infoMap["type"]
		if ok {
			b,_ := strconv.Atoi(infoMap["type"])
			request.Type = int8(b)
		}

		_, ok = infoMap["interfaceName"]
		if ok {
			request.InterfaceName = infoMap["interfaceName"]
		}

		_, ok = infoMap["hasWiFi"]
		if ok {
			b,_ := strconv.Atoi(infoMap["hasWiFi"])
			request.HasWiFi = int8(b)
		}

		_, ok = infoMap["metaType"]
		if ok {
			s := infoMap["metaType"]
			request.MetaType = &s
		}

		_, ok = infoMap["id"]
		if ok {
			request.ID = infoMap["id"]
		}else{
			request.ID = ""
		}

		_, ok = infoMap["channelId"]
		if ok {
			s := infoMap["channelId"]
			request.ChannelId = &s
		}

		_, ok = infoMap["albumId"]
		if ok {
			s := infoMap["albumId"]
			request.AlbumId = &s
		}

		c <- &request
	}

	close(c)
	return c

}


//func SyntheticRequests() chan interface{}{
//	c := make(chan interface{}, 5000)
//	b, err := ioutil.ReadFile("id_with_type_online.json")
//	if err != nil {
//		fmt.Print(err)
//	}
//	str := string(b)
//	reqJson := gojson.Json(str)
//
//	ids := reqJson.Get("actor").StringtoArray()
//	//fmt.Println(ids)
//	var actorIwt di.IdsWithType
//	actorIwt.Ids = ids
//	actorIwt.Type = "actor"
//	var keyArray = [14]string{
//		"actor", "album",
//		"director", "short_video", "genre",
//		"language", "movie", "playlist",
//		"publisher", "season", "singer",
//		"song", "tv_show", "tv_show_video"}
//
//	for i:=0; i<len(keyArray);i++  {
//		ids := gojson.Json(str).Get(keyArray[i]).StringtoArray()
//		GetOneTypeReq(keyArray[i], ids, c)
//	}
//	close(c)
//
//	return c
//
//}

//func GetOneTypeReq(s string, ids []string, c chan interface{}) {
//	i, end, idLen := 0, 0, 0
//	for ; i<len(ids);  {
//		s2 := rand.NewSource(time.Now().Unix() + int64(i)) //同前面一样的种子
//		r2 := rand.New(s2)
//		idLen = r2.Intn(20) + 5
//		end = i + idLen
//		if end > len(ids){
//			end = len(ids)
//		}
//
//		var idwt di.IdsWithType
//		idwt.Type = s
//		idwt.Ids = ids[i:end]
//
//		var req di.DIRequest
//		req.IdsWithTypes = append(req.IdsWithTypes, &idwt)
//		req.ServiceName = "test_client"
//
//		c <- &req
//		i = end
//	}
//}

//重要:需要跟服务端所用协议一致
func ASExecutor(request interface{}, transport thrift.TTransport) (interface{}, error) {
	pFac := thrift.NewTCompactProtocolFactory()
	client := recommend.NewRecommendServiceClientFactory(transport, pFac)
	return client.Recommend(nil, request.(*recommend.Request))

	//client := di.NewDIServiceClientFactory(transport, pFac)
	//return client.GetDetail(nil, request.(*di.DIRequest))
}

// 主要是用bender的接口，完成压测
func main() {
	intervals := bender.ExponentialIntervalGenerator(100) // qps
	requests := SyntheticRecommendRequests()           //总请求数
	host := "xxx:19889" //press机器

	//host := "127.0.0.1:19959"
	//buffer字节数, clientExec, 超时时间, hosts--写server所在的ip和端口,如非同一机器,保证端口可访问
	//exec := bthrift.NewThriftRequestExec(thrift.NewTBufferedTransportFactory(125), ASExecutor, 10 * time.Second, host)
	//exec := bthrift.NewThriftRequestExec(thrift.NewTCompactProtocolFactory(), ASExecutor, 10 * time.Second, host)
	exec := bthrift.NewThriftRequestExec(thrift.NewTFramedTransportFactory(thrift.NewTTransportFactory()), ASExecutor, 10 * time.Second, host)
	recorder := make(chan interface{}, 128)
	bender.LoadTestThroughput(intervals, requests, exec, recorder)
	l := log.New(os.Stdout, "", log.LstdFlags)
	h := hist.NewHistogram(60000, 1000000)
	bender.Record(recorder, bender.NewLoggingRecorder(l), bender.NewHistogramRecorder(h))
	fmt.Println(h)
}
