from prometheus_client import start_http_server, Gauge
import random
import time

class MetricServer(object):
    
    def __init__(self, port=8000, addr=''):
        start_http_server(port, addr=addr)
        self.gauges = dict()

    def update_metric(self, metric_name: str, data: float):
        if metric_name not in self.gauges:
            self.gauges[metric_name] = Gauge(f"obdii_{metric_name}", f"OBD-II Data: {metric_name}")
        self.gauges[metric_name].set(data)


def __main():
    metrics = MetricServer()
    cur_speed = 1.0
    while True:
        time.sleep(1)
        cur_speed = cur_speed*0.99 + random.random()*0.01
        metrics.update_metric('speed', cur_speed)


if __name__ == '__main__':
    __main()

