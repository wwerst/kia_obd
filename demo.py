import time
import obd


def spin(connection):
    cmd = obd.commands.ENGINE_LOAD # select an OBD command (sensor)
    response = connection.query(cmd) # send the command, and parse the response
    print(f'Engine Load: {response.value:.3f}') # returns unit-bearing values thanks to Pint
    cmd = obd.commands.PIDS_A
    response = connection.query(cmd)
    print(f'PIDS_A: {response.value}')


def main():
    # See https://github.com/brendan-w/python-OBD/issues/93
    # Note, for FiXD device, the pin code is 1234
    try:
        connection = obd.OBD('/dev/rfcomm1') # auto-connects to USB or RF port

        cmd = obd.commands.PIDS_A
        response = connection.query(cmd)
        print(f'PIDS_A: {response.value}')
        for i in range(32):
            print(f'PID {hex(i+1)} Supported: {response.value[i]}')

        cmd = obd.commands.PIDS_B
        response = connection.query(cmd)
        print(f'PIDS_B: {response.value}')
        for i in range(32):
            print(f'PID {hex(32+i+1)} Supported: {response.value[i]}')

        cmd = obd.commands.PIDS_C
        response = connection.query(cmd)
        print(f'PIDS_C: {response.value}')
        for i in range(32):
            print(f'PID {hex(64+i+1)} Supported: {response.value[i]}')

        start_time = time.time()
        LOOP_TIME = 1.0  # seconds

        while True:
            spin(connection)
            time.sleep(max(0, LOOP_TIME + start_time - time.time()))
            start_time = time.time()
    finally:
        connection.close()


if __name__ == '__main__':
    main()
