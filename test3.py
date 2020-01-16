#!/usr/bin/env python

from midiutil import MIDIFile
import random

degrees  = [ 62, 64, 65, 67, 69, 71, 72,74]  # MIDI note number
##degrees = [66,68,70,71,72,74,75,76,77]
track    = 0
channel  = 0
time     = 0    # In beats
duration = 1    # In beats
tempo    = 60   # In BPM
volume   = 100  # 0-127, as per the MIDI standard
transpose = -2
octaves = 2

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                      # automatically)
MyMIDI.addTempo(track, time, tempo)

ndegrees = []
for i in range(1,octaves):
    for j in range(0, len(degrees)):
        ndegrees.append(degrees[j]+12*i)
        ndegrees.append(degrees[j]-12*i)
ndegrees += degrees
degrees = ndegrees
## build song 
phrs = 100
rpt = [1,2,3,8]
nrpt = [1,2,3,8]
phrslen = [4,8,12,16,20,24,28,32,36]
phrslensets = []
phrssets = 5
sng = []
rptphrs = 0
phrslens = 0
nts = {}
ntlen = [0.25,.5,.75, 1]

def buildphrslensets(phrslen, phrssets):
    phrslensets = []
    for i in range(0, phrssets):
        phrsnum = random.randint(2,len(phrslen)-1)
        nphrs = []
        maxphrs = random.randint(2,36)
        for j in range (0, phrsnum):
            nphrs.append(random.randint(2,maxphrs))
        phrslensets.append(nphrs)
    return phrslensets

def buildphrase(degrees, phrslen, ntlen):
    def buildtimedistr(timed):
        timedists = []
        for i in range(0,9):
            timedist = []
            for j in range(0, random.randint(3,10)):
                timedist.append(random.choice(timed))
            timedists.append(timedist)
        return timedists

    nts = []
    picklen = 36
    picklen = random.randint(6,picklen)
    ## assign weights
    nweights = []
    for i in range(0, picklen):
        if len(nweights) == 0:
            nweights.append(random.random()*.35+.65)
        else:
            nweights.append(random.random()*.5+.5)##nweights[-1]*(random.random()*.05+.95))
    ## assign time distribution
    timedistr = [.75,.7,.65,.6,.5,.5,.25,.25,.2,.25,.35,.2,.15]
    tpicks = []
    timedistrs = buildtimedistr(timedistr)
    timedistr = random.choice(timedistrs)
    for i in range(0, picklen):
        tpicks.append(random.choice(timedistr))

    ## pick picklen notes
    npicks = []
    for i in range(0, picklen):
        npicks.append([tpicks[i], random.choice(degrees)])
    nts = random.choices(population=npicks, weights=nweights,k=phrslen)
    print(nts)
    # for i in range(0, phrslen):
    #     ntp = random.choice(degrees)
    #     nttp = random.choice(ntlen)
    #     np = {}
    #     np[ntp] = nttp
    #     nts.append(np)
    return nts

def setArrangement(oldwphrs, phrs):
    ## oldwphrs length
    tphlen = 0 ## total phrase time
    nts = []  
    for i in range(0, len(oldwphrs)):
        ind = random.randint(0,len(oldwphrs)-1)
        rptphrlen = oldwphrs[ind][1]
        for j in range(0,rptphrlen):
            nts += oldwphrs[ind][0]
    return nts     

ants = []
oldwphrs = []  
phrslensets = buildphrslensets(phrslen, phrssets)      
for i in range(0, phrs):
    wphrs = []
    
    if rptphrs == 0:
        rptphrs = random.choice(rpt)
        nts = {}
        nphrslen = random.choice(phrslensets)
        phrslens = random.choice(nphrslen)
        
        wphrs = buildphrase(degrees, phrslens, ntlen)
        oldwphrs.append([wphrs,rptphrs])
        # ants += wphrs
    # else:
    #     ants += wphrs 
    rptphrs -= 1
ants = setArrangement(oldwphrs,phrs)
ttime = 0
for time, pitch in ants:
    ttime += time
    MyMIDI.addNote(track, channel, pitch+transpose, ttime, duration, volume)

with open("C:\\Users\\chris\\MuiscPy\\major-scale.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)