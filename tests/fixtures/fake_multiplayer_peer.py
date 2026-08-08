#!/usr/bin/env python3
import argparse, signal, sys, time

parser=argparse.ArgumentParser(); parser.add_argument('--role',required=True); parser.add_argument('--ready-delay',type=float,default=.03); parser.add_argument('--complete-delay',type=float,default=.05); parser.add_argument('--fail',action='store_true')
args=parser.parse_args(); running=True
def stop(*_):
    global running; running=False
if hasattr(signal,'SIGTERM'): signal.signal(signal.SIGTERM,stop)
time.sleep(args.ready_delay)
print('UAP_NET_READY' if args.role=='server' else 'UAP_NET_CONNECTED',flush=True)
if args.fail: print('UAP_TEST_FAILED',flush=True); sys.exit(3)
if args.role!='server': time.sleep(args.complete_delay); print('UAP_TEST_COMPLETE',flush=True)
while running: time.sleep(.02)
