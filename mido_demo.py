#pygame barebones?
#volume
#instrument
#latency

import mido
from mido import Message
#mido.set_backend('mido.backends.pygame')
import time

print(mido.get_input_names())
print(mido.get_output_names())
in_portname = None
out_portname = 'Microsoft GS Wavetable Synth'
try:
    with mido.open_input(in_portname) as in_port, mido.open_output(out_portname, autoreset=True) as out_port:
        print('Using input: {}'.format(in_port))
        print('Using output: {}'.format(out_port))
        print('Waiting for messages...')
        for message in in_port:
            out_port.send(message)
            print('Received {}'.format(message))
except KeyboardInterrupt:
    pass
