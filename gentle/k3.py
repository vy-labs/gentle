import subprocess
from util.paths import get_binary
import os

EXECUTABLE_PATH = get_binary("ext/k3")

class K3:
    def __init__(self, nnet_dir=None, hclg_path=None, proto_langdir=None):
        devnull = open(os.devnull, 'w')
        
        cmd = [EXECUTABLE_PATH]
        
        if nnet_dir is not None:
            cmd.append(nnet_dir)
            cmd.append(hclg_path)
            cmd.append(proto_langdir)

        self._p = subprocess.Popen(cmd,
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=devnull)

    def _cmd(self, c):
        self._p.stdin.write("%s\n" % (c))
        self._p.stdin.flush()

    def push_chunk(self, buf):
        # Wait until we're ready
        self._cmd("push-chunk")
        self._cmd(str(len(buf)/2))
        self._p.stdin.write(buf) #arr.tostring())
        status = self._p.stdout.readline().strip()
        return status == 'ok'

    def get_final(self):
        self._cmd("get-final")
        words = []
        while True:
            line = self._p.stdout.readline()
            if line.startswith("done"):
                break
            parts = line.split(' / ')
            if line.startswith('word'):
                wd = {}
                wd['word'] = parts[0].split(': ')[1]
                wd['start'] = float(parts[1].split(': ')[1])
                wd['duration'] = float(parts[2].split(': ')[1])
                wd['phones'] = []
                words.append(wd)
            elif line.startswith('phone'):
                ph = {}
                ph['phone'] = parts[0].split(': ')[1]
                ph['duration'] = float(parts[1].split(': ')[1])
                words[-1]['phones'].append(ph)

        self._reset()
        return words

    def _reset(self):
        self._cmd("reset");

if __name__=='__main__':
    import numm3
    import sys

    infile = sys.argv[1]
    
    k = K3()

    buf = numm3.sound2np(infile, nchannels=1, R=8000)
    print 'loaded_buf', len(buf)
    
    idx=0
    while idx < len(buf):
        k.push_chunk(buf[idx:idx+160000].tostring())
        print k.get_final()
        idx += 160000