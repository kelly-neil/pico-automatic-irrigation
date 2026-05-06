function Section(title, desc, t_content) {
    return {
        title: title,
        desc: desc,
        t_content: t_content,
        $template: "#t_section"
    }
}

PetiteVue.createApp({
    cfg: null,
    data: {
        humidity: 0,
        temperature: 0,
        moisture: 0,
        infrared: 0
    },
    extradata: null,
    loglist: {
        loaded: false,
        data: null
    },
    logfocus: {
        loaded: false,
        status: 0,
        data: null
    },
    selection: {
        monitor_day: null, // current day
        monitor_param: "moisture"
    },
    init() {
        this.liveOnce();
        //this.startLive();
        setInterval(this.liveOnce, 10000);
        fetch("/data/monitor").then((response) => {
            response.json().then((data) => {
                logs = data.logs
            })
        })

        fetch("/data/cfg").then((response) => {
            response.json().then((data) => {
                this.cfg = JSON.stringify(data.cfg, null, 4)
            })
        })
    },
    startLive() {
        // Start an SSE in URL /data/live
        const eventSource = new EventSource('/data/live');
        eventSource.onmessage = (event) => {
            console.log("Data received")
            const data = JSON.parse(event.data).sensors;
            this.data = data;
        };
    },
    liveOnce() {
        // Start with HTTP requests instead
        fetch('/data/liveonce').then((response) => {
            response.json().then((data) => {
                this.data = data.sensors
                this.extradata = data.extra
            })
        })
    },
    fecthLogs(filename) {
        this.logfocus.loaded = false;
        this.logfocus.status = 1
        fetch("/data/monitor?file=" + filename).then((response) => {
            response.json().then((data) => {
                this.logfocus.data = data
                this.logfocus.status = 2
                this.logfocus.loaded = true
                ctx = document.getElementById('logChart').getContext('2d');
                data = {
                    labe
                }

                logChart = new Chart(ctx, {
                    type: "line",
                    options: {
                        spanGaps: true,
                        scales: {
                            x: {
                                type: "time",
                            }
                        }
                    }
                })

                logChart.data = {
                    datasets: [{
                        data: data.moisture
                    }]
                }
            })
        })
    },
    toPercent(decimal) {
        result = Math.round(decimal * 10000) / 100
        return result
    },
    toReadablePIR(bool) {
        return bool ? "Motion detected" : "No motion detected"
    },
    toColor(type, value) {
        function linear(rgb1, rgb2, percent) {
            
            result = new Array(3)

            for (var i = 0; i < 3; i++) {
                result[i] = rgb1[i] + Math.round((rgb2[i] - rgb1[i]) * percent)
            }
            
            return result
        }
        
        rgb = [0, 0, 0]
        switch (type) {
            case "moisture":
                rgb = linear([192, 192, 192], [64, 128, 255], value)
            case "temperature":
                percent = (value - 20) / 20
                console.log("Percent is " + percent)
                rgb = linear([64, 255, 64], [255, 128, 64], percent)
            case "humidity":
                rgb = linear([192, 160, 128], [128, 192, 192], value / 100)
        }
        out = "rgb(" + rgb[0] + ", " + rgb[1] + ", " + rgb[2] + ")"
        out = "background-color: " + out + ";"
        console.log(out)
        return out
    },
    saveConfig() {
        fetch("/data/cfg", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.cfg)
        }).then((response) => {
            response.text().then((text) => {
                if (response.ok) {
                    alert("Saved successfully")
                } else if (response.status == 500) {
                    alert("Something went wrong: " + text)
                }
            })
        })
    }
}).mount('#app')