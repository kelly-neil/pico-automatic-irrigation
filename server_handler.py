import os
import gc
from phew import connect_to_wifi, server
import phew
import phew.server
import sensors_json
import asyncio
import time
import json
import random
import logger
from sensors_manager import SensorLoopManager
web_path = "/web"


async def run(stopSignal, loop: SensorLoopManager):
    def fileGenerator(file, chunk_size=1024):
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk
            
    """
    async def SSELiveGenerator():
        while True:
            print("Generating")
            await asyncio.sleep(10)
            result = loop.last_result
            yield "data: {}\n\n".format(sensors_json.format_livedata(result))
    """

    """
    class SSEGenerator():
        def __init__(self):
            pass

        def __aiter__(self):
            return self

        async def __anext__(self):
            await asyncio.sleep(10)
            result = loop.last_result
            return "data: {}\n\n".format(sensors_json.format_livedata(result))
    """
    
    def returnCSVResponse(file, filename: str = "data.csv", downloaded = False) -> server.Response:
        headers = {}

        if downloaded:
            headers["Content-Type"] = "text/csv"
            headers["Content-Disposition"] = "attachment; filename=" + filename
        
        return server.Response(fileGenerator(file), status=200, headers=headers)


    @server.route("/<path>", methods=["GET"])
    def get(request, path):
        print("Got root request")
        abspath = web_path + request.path

        try:
            isdir = (os.stat(abspath)[0] & 0x4000) != 0
        except OSError:
            return server.Response("File not found",status=404)

        if isdir:
            abspath += "/index.html"
        gc.collect()
        file = open(abspath, "rb", 1024)

        ctype = "application/octet-stream"
        # change ctype according to file extension
        if abspath.endswith(".html"):
            ctype = "text/html"
        elif abspath.endswith(".js"):
            ctype = "application/javascript"
        elif abspath.endswith(".css"):
            ctype = "text/css"
        elif abspath.endswith(".png"):
            ctype = "image/png"
        elif abspath.endswith(".jpg"):
            ctype = "image/jpg"

        return server.Response(fileGenerator(file), status=200, headers={"Content-Type": ctype})

    @server.route("/test/test", methods=["GET"])
    def test(request):
        return "Hello World!", 200

    @server.route("/debug/stop", methods=["GET"])
    def stop(request):
        import sensors_manager
        loop.stop()
        stopSignal()
        asyncio.get_event_loop().stop()
        asyncio.get_event_loop().close()
        return "Stop signal is sent, this will take a few seconds before everything has stopped.", 200

    @server.route("/debug/water", methods=["GET"])
    def water(request):
        out = ""

        if "duration" in request.query.keys():
            duration = int(request.query["duration"])
            asyncio.create_task(loop.waterManual(duration))
            out += "Watering for {} seconds \n".format(duration)
        else:
            asyncio.create_task(loop.water())
            out += "Watering... default settings used"

        return "Watering", 200

    @server.route("/data/live", methods=["GET"])
    def data(request):
        print("Data request was received")
        #return sensors_json.fetch_live_data(), 200
        return server.Response(SSELiveGenerator(), status=200, headers={
            "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
            "Connection": "keep-alive",}
        )

    @server.route("/data/liveonce", methods=["GET"])
    def dataonce(request):
        print("Data request was received")
        result = loop.last_result
        return sensors_json.format_livedata(result), 200
    
    @server.route("/data/logview", methods=["GET"])
    def logview(request):
        if "file" in request.query.keys():
            target = request.query["file"]
        else:
            target = logger.formatDate(logger.now())

        return server.redirect("/data/logview/" + target + "-data.csv")
    
    @server.route("/data/logview/<path>", methods=["GET"])
    def logview_file(request, path):
        path = logger.LOG_DIR + path
        print("Attempt file fetch: ", path)
        file = open(path, "rb", 1024)
        return returnCSVResponse(file, downloaded=False)
    
    @server.route("/data/logdownload", methods=["GET"])
    def logdownload(request):
        if "file" in request.query.keys():
            target = request.query["file"]
        else:
            target = logger.formatDate(logger.now())

        return server.redirect("/data/logdownload/" + target + "-data.csv")
    
    @server.route("/data/logdownload/<path>", methods=["GET"])
    def logdownload_file(request, path):
        file = open(logger.LOG_DIR + path, "rb", 1024)
        return returnCSVResponse(file, path, True)
    
    @server.route("/data/monitor", methods=["GET"])
    def monitor(request):
        if "file" in request.query.keys():
            import csv
            out = {
                "moisture": [{
                    "data": []
                }],
                "temperature": [{
                    "data": []
                }],
                "humidity": [{
                    "data": []
                }],
            }
            target = request.query["file"]
            file = open(logger.LOG_DIR + target, "rb", 1024)

            # read the file line by line
            while True:
                line = file.readline()
                if not line:
                    break
                line = line.decode("utf-8")
                line = line.split(",")
                """
                out["time"].append(line[0])
                out["moisture"].append(line[1])
                out["temperature"].append(line[2])
                out["humidity"].append(line[3])
                """
                out["moisture"][0]["data"].append({"x": line[0], "y": line[1]})
                out["temperature"][0]["data"].append({"x": line[0], "y": line[2]})
                out["humidity"][0]["data"].append({"x": line[0], "y": line[3]})

            return json.dumps(out), 200
        else:
            import os
            out = {"logs": []}
            list = os.listdir("/sd/log")

            # filter to files ending with -data.csv
            list = [x for x in list if x.endswith("-data.csv")]

            for file in list:
                out["logs"].append(file)

            return json.dumps(out), 200

    @server.catchall()
    def catchall(request):
        gc.collect()
        return "Not found", 404

    server.run()
    print("Server stopped!")

async def wifi(ssid, password):
    web_ip = await connect_to_wifi(ssid, password, 10)
    print("The web panel would be avaialbe at: http://" + str(web_ip))
    return web_ip