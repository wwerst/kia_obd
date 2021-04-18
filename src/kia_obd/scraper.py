import time
import obd

from prom_client import MetricServer

metric_server = MetricServer()


def spin_pid_list(connection, pid_list):
    for pid_num in pid_list:
        cmd = obd.commands[1][pid_num]
        response = connection.query(cmd)
        if response is not None and response.value is not None:
            data_name = f"{cmd.name}_pid{pid_num}_{response.value.units}"
            metric_server.update_metric(data_name, response.value.magnitude)
        else:
            print(f"None received {pid_num}, {cmd.name}")


def main():
    # See https://github.com/brendan-w/python-OBD/issues/93
    # Note, for FiXD device, the pin code is 1234
    try:
        connection = obd.OBD('/dev/rfcomm1') # auto-connects to USB or RF port

        valid_pids = []
        cmd = obd.commands.PIDS_A
        response = connection.query(cmd)
        print(f'PIDS_A: {response.value}')
        for i in range(32):
            pid_num = i+1
            if response.value[i] == 1 and i != 31:
                valid_pids.append(pid_num)
            print(f'PID {hex(pid_num)} Supported: {response.value[i]}')

        cmd = obd.commands.PIDS_B
        response = connection.query(cmd)
        print(f'PIDS_B: {response.value}')
        for i in range(32):
            pid_num = 32+i+1
            if response.value[i] == 1 and i != 31:
                valid_pids.append(pid_num)
            print(f'PID {hex(pid_num)} Supported: {response.value[i]}')

        cmd = obd.commands.PIDS_C
        response = connection.query(cmd)
        print(f'PIDS_C: {response.value}')
        for i in range(32):
            pid_num = 64+i+1
            if response.value[i] == 1 and i != 31:
                valid_pids.append(pid_num)
            print(f'PID {hex(pid_num)} Supported: {response.value[i]}')

        blacklist_pids = [
            obd.commands.FUEL_STATUS.pid,
            obd.commands.O2_SENSORS.pid,
            obd.commands.OBD_COMPLIANCE.pid,
            obd.commands.STATUS.pid,
            obd.commands.STATUS_DRIVE_CYCLE.pid,
        ]

        scan_pids = [p for p in valid_pids if p not in blacklist_pids]

        start_time = time.time()
        LOOP_TIME_GOAL = 2.0  # seconds

        while True:
            spin_pid_list(connection, scan_pids)
            spin_time = time.time() - start_time
            print(f'Loop took {spin_time:.3f} seconds')
            print()
            print()
            print()
            time.sleep(max(0, LOOP_TIME_GOAL - spin_time))
            start_time = time.time()
    finally:
        connection.close()


if __name__ == '__main__':
    main()
