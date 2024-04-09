function Section(title, desc, t_content) {
    return {
        title: title,
        desc: desc,
        t_content: t_content,
        $template: "#t_section"
    }
}

PetiteVue.createApp({
    data: {
        humidity: 0,
        temperature: 0,
        moisture: 0,
        infrared: 0
    },
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
        //this.startLive(); // never, ever works.
        setInterval(this.liveOnce, 10000);
        fetch("/data/monitor").then((response) => {
            response.json().then((data) => {
                logs = data.logs
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
                this.data = data.sensors;
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
    }
}).mount('#app')