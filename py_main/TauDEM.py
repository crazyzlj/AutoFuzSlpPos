# Script Name: TauDEM functions
# 
# Created By:  David Tarboton
# Date:        9/28/11
# Revised By:  Liang-Jun Zhu (zlj@lreis.ac.cn)
# Date:        3/5/15
# Modified  :  Integrate to one file. Run without arcpy. Same name with executable files.
# Revised By:  Liang-Jun Zhu
# Date:        4/14/15
# Modified  :  add path to TauDEM executable program


# Program: TauDEM and extensions based on TauDEM parallelized framework
# 
# Revised By:  Liang-Jun Zhu
# Date From :  3/20/15
# Email     :  zlj@lreis.ac.cn
#

import os
import platform
import subprocess
from Nomenclature import Log_all, Log_runtime
from Util import WriteLog, WriteTimeLog, StringMatch

sysstr = platform.system()
if sysstr == "Windows":
    LF = '\r'
elif sysstr == "Linux":
    LF = '\n'


## Write log
def outputLog(title, lines):
    contentList = []
    timeDict = {'name': None, 'readt': 0, 'writet': 0, 'computet': 0, 'totalt': 0}
    timeDict['name'] = title
    contentList.append('\n')
    contentList.append("#### %s ####" % title)
    for line in lines:
        contentList.append(line.split(LF)[0])
        # print line
        if line.find("Read time") >= 0:
            timeDict['readt'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Compute time") >= 0:
            timeDict['computet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Write time") >= 0:
            timeDict['writet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Total time") >= 0:
            timeDict['totalt'] = line.split(LF)[0].split(':')[-1]
    WriteLog(Log_all, contentList)
    WriteTimeLog(Log_runtime, timeDict)

def MPIHeader(mpiexeDir, inputProc, hostfile=None):
    if mpiexeDir is not None:
        cmd = '"' + mpiexeDir + os.sep + 'mpiexec"'
    else:
        cmd = '"mpiexec"'
    if inputProc > 8 and hostfile is not None:
        cmd = cmd + ' -f ' + hostfile + ' -n '
    else:
        cmd += ' -n '
    return cmd

## Basic Grid Analysis
def pitremove(inZfile, inputProc, outFile, mpiexeDir = None, exeDir = None, hostfile = None):
    print "PitRemove......"
    print "Input Elevation file: " + inZfile
    print "Input Number of Processes: " + str(inputProc)
    print "Output Pit Removed Elevation file: " + outFile
    # Construct the taudem command line.  Put quotes around file names in case there are spaces
    cmd = MPIHeader(mpiexeDir, inputProc, hostfile)
    if exeDir is None:
        cmd = cmd + str(inputProc) + ' pitremove -z ' + '"' + inZfile + '"' + ' -fel ' + '"' + outFile + '"'
    else:
        cmd = cmd + str(
                inputProc) + ' ' + exeDir + os.sep + 'pitremove -z ' + '"' + inZfile + '"' + ' -fel ' + '"' + outFile + '"'

    print "Command Line: " + cmd
    ##os.system(cmd)
    process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    outputLog("PitRemove", process.stdout.readlines())

def ConnectDown(ad8, outlet, inputProc, mpiexeDir = None, exeDir = None, hostfile = None):
    print "Generating outlet shapefile from areaD8......"
    print "Input areaD8 file: " + ad8
    print "Input Number of Processes: " + str(inputProc)
    print "Output outlet File: " + outlet

    # Construct command
    cmd = MPIHeader(mpiexeDir, inputProc, hostfile)
    if exeDir is None:
        cmd = cmd + str(inputProc) + ' connectdown -ad8 ' + '"' + ad8 + '"' + ' -o ' + '"' + outlet + '"'
    else:
        cmd = cmd + str(
                inputProc) + ' ' + exeDir + os.sep + 'connectdown -ad8 ' + '"' + ad8 + '"' + ' -o ' + '"' + outlet + '"'

    print "Command Line: " + cmd
    ##os.system(cmd)
    process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    outputLog("ConnectDown", process.stdout.readlines())


def D8FlowDir(fel, inputProc, p, sd8, mpiexeDir = None, exeDir = None, hostfile = None):
    print "Calculating D8 flow direction......"
    print "Input Pit Filled Elevation file: " + fel
    print "Input Number of Processes: " + str(inputProc)
    print "Output D8 Flow Direction File: " + p
    print "Output D8 Slope File: " + sd8
    # Construct command
    cmd = MPIHeader(mpiexeDir, inputProc, hostfile)

    if exeDir is None:
        cmd = cmd + str(inputProc) + ' d8flowdir -fel ' + '"' + fel + '"' + ' -p ' + '"' + p + '"' + \
              ' -sd8 ' + '"' + sd8 + '"'
    else:
        cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'd8flowdir -fel ' + '"' + fel + '"' + ' -p ' + '"' + p +\
              '"' + ' -sd8 ' + '"' + sd8 + '"'

    print "Command Line: " + cmd
    ##os.system(cmd)
    process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    outputLog("D8FlowDir", process.stdout.readlines())


def DinfFlowDir(fel, inputProc, ang, slp, mpiexeDir = None, exeDir = None, hostfile = None):
    print "Calculating D-infinity direction......"
    print "Input Pit Filled Elevation file: " + fel
    print "Input Number of Processes: " + str(inputProc)
    print "Output Dinf Flow Direction File: " + ang
    print "Output Dinf Slope File: " + slp
    # Construct command 
    cmd = MPIHeader(mpiexeDir, inputProc, hostfile)

    if exeDir is None:
        cmd = cmd + str(inputProc) + ' dinfflowdir -fel ' + '"' + fel + '"' + ' -ang ' + '"' + ang + '"' +\
              ' -slp ' + '"' + slp + '"'
    else:
        cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'dinfflowdir -fel ' + '"' + fel + '"' + ' -ang ' +\
              '"' + ang + '"' + ' -slp ' + '"' + slp + '"'

    print "Command Line: " + cmd
    # os.system(cmd)
    process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    outputLog("DinfFlowDir", process.stdout.readlines())


def AreaD8(p, Shapefile, weightgrid, edgecontamination, inputProc, ad8, mpiexeDir = None, exeDir = None,
           hostfile = None):
    print "Calculating D8 contributing area......"
    print "Input D8 Flow Direction file: " + p
    if os.path.exists(Shapefile):
        print "Input Outlets Shapefile: " + Shapefile
    if os.path.exists(weightgrid):
        print "Input Weight Grid: " + weightgrid
    print "Edge Contamination: " + edgecontamination
    print "Input Number of Processes: " + str(inputProc)
    print "Output D8 Contributing Area Grid: " + ad8
    # Construct command
    cmd = MPIHeader(mpiexeDir, inputProc, hostfile)

    if exeDir is None:
        cmd = cmd + str(inputProc) + ' aread8 -p ' + '"' + p + '"' + ' -ad8 ' + '"' + ad8 + '"'
    else:
        cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'aread8 -p ' + '"' + p + '"' + ' -ad8 ' + '"' + ad8 + '"'
    if os.path.exists(Shapefile):
        cmd = cmd + ' -o ' + '"' + Shapefile + '"'
    if os.path.exists(weightgrid):
        cmd = cmd + ' -wg ' + '"' + weightgrid + '"'
    if StringMatch(edgecontamination, 'false') or edgecontamination is False:
        cmd += ' -nc '

    print "Command Line: " + cmd
    # os.system(cmd)
    process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    outputLog("D8 contributing area", process.stdout.readlines())


def AreaDinf(ang, shapefile, weightgrid, edgecontamination, inputProc, sca, mpiexeDir = None, exeDir = None,
             hostfile = None):
    print "Calculating D-infinity contributing area......"
    print "Input Dinf Flow Direction file: " + ang
    if os.path.exists(shapefile):
        print "Input Outlets Shapefile: " + shapefile
    if os.path.exists(weightgrid):
        print "Input Weight Grid: " + weightgrid
    print "Edge Contamination: " + edgecontamination
    print "Input Number of Processes: " + str(inputProc)
    print "Output Dinf Specific Catchment Area Grid: " + sca
    # Construct command
    cmd = MPIHeader(mpiexeDir, inputProc, hostfile)

    if exeDir is None:
        cmd = cmd + str(inputProc) + ' areadinf -ang ' + '"' + ang + '"' + ' -sca ' + '"' + sca + '"'
    else:
        cmd = cmd + str(
                inputProc) + ' ' + exeDir + os.sep + 'areadinf -ang ' + '"' + ang + '"' + ' -sca ' + '"' + sca + '"'
    if os.path.exists(shapefile):
        cmd = cmd + ' -o ' + '"' + shapefile + '"'
    if os.path.exists(weightgrid):
        cmd = cmd + ' -wg ' + '"' + weightgrid + '"'
    if StringMatch(edgecontamination, 'false') or edgecontamination is False:
        cmd += ' -nc '

    print "Command Line: " + cmd
    # os.system(cmd)
    process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    outputLog("D-inf contributing area", process.stdout.readlines())


## Specialized grid analysis

def DinfDistDown(ang, fel, src, statisticalmethod, distancemethod, edgecontamination, wg, inputProc, dd,
                 mpiexeDir = None, exeDir = None, hostfile = None):
    print "Calculating distance down to stream based on D-infinity model......"
    print "Input D-Infinity Flow Direction Grid: " + ang
    print "Input Pit Filled Elevation Grid: " + fel
    print "Input Stream Raster Grid: " + src
    print "Statistical Method: " + statisticalmethod
    print "Distance Method: " + distancemethod
    print "Edge Contamination: " + edgecontamination
    if wg is not None and os.path.exists(wg):
        print "Input Weight Path Grid: " + wg
    print "Input Number of Processes: " + str(inputProc)
    print "Output D-Infinity Drop to Stream Grid: " + dd

    # Construct command
    if StringMatch(statisticalmethod, 'Average'):
        statmeth = 'ave'
    elif StringMatch(statisticalmethod, 'Maximum'):
        statmeth = 'max'
    elif StringMatch(statisticalmethod,'Minimum'):
        statmeth = 'min'
    else:
        statmeth = 'ave'
    if StringMatch(distancemethod, 'Horizontal'):
        distmeth = 'h'
    elif StringMatch(distancemethod, 'Vertical'):
        distmeth = 'v'
    elif StringMatch(distancemethod, 'Pythagoras'):
        distmeth = 'p'
    elif StringMatch(distancemethod, 'Surface'):
        distmeth = 's'
    else:
        distmeth = 's'
    cmd = MPIHeader(mpiexeDir, inputProc, hostfile)

    if exeDir is None:
        cmd = cmd + str(inputProc) + ' dinfdistdown -fel ' + '"' + fel + '"' + ' -ang ' + '"' + ang + '"' + \
              ' -src ' + '"' + src + '"' + ' -dd ' + '"' + dd + '"' + ' -m ' + statmeth + ' ' + distmeth
    else:
        cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'dinfdistdown -fel ' + '"' + fel + '"' + \
              ' -ang ' + '"' + ang + '"' + ' -src ' + '"' + src + '"' + ' -dd ' + '"' + dd + '"' + ' -m ' + \
              statmeth + ' ' + distmeth

    if wg is not None and os.path.exists(wg):
        cmd = cmd + ' -wg ' + '"' + wg + '"'
    if StringMatch(edgecontamination, 'false') or edgecontamination is False:
        cmd += ' -nc '

    print "Command Line: " + cmd
    # os.system(cmd)
    process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    outputLog("Dinf distance down", process.stdout.readlines())


def MoveOutletsToStreams(p, src, shapefile, maxdistance, inputProc, om, mpiexeDir = None, exeDir = None,
                         hostfile = None):
    print "Moving outlet point(s) to streams......"
    print "Input D8 Flow Direction Grid: " + p
    print "Input Stream Raster Grid: " + src
    print "Input Outlets Shapefile: " + shapefile
    print "Minimum Threshold Value: " + str(maxdistance)
    print "Input Number of Processes: " + str(inputProc)

    print "Output Outlet Shapefile: " + om

    # Construct command
    cmd = MPIHeader(mpiexeDir, inputProc, hostfile)

    if exeDir is None:
        cmd = cmd + str(inputProc) + ' moveoutletstostreams -p ' + '"' + p + '"' + ' -src ' + '"' + src + \
              '"' + ' -o ' + '"' + shapefile + '"' + ' -om ' + '"' + om + '"' + ' -md ' + str(maxdistance)
    else:
        cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'moveoutletstostreams -p ' + '"' + p + '"' + \
              ' -src ' + '"' + src + '"' + ' -o ' + '"' + shapefile + '"' + ' -om ' + '"' + om + '"' + \
              ' -md ' + str(maxdistance)

    print "Command Line: " + cmd
    # os.system(cmd)
    process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    outputLog("Moving outlet point to streams", process.stdout.readlines())

def StreamNet(filledDem, flowDir, acc, streamRaster, modifiedOutlet, streamOrder, chNetwork, chCoord,
              streamNet, subbasin,inputProc, mpiexeDir = None, exeDir = None,hostfile = None):
    cmd = MPIHeader(mpiexeDir, inputProc, hostfile)
    if exeDir is not None:
        exe = exeDir + os.sep + "streamnet"
    else:
        exe = "streamnet"
    cmd += " %d %s -fel %s -p %s -ad8 %s -src %s -o %s  -ord %s -tree %s -coord %s -net %s -w %s" % (
        inputProc, exe, filledDem, flowDir, acc, streamRaster, modifiedOutlet, streamOrder, chNetwork, chCoord,
        streamNet, subbasin)

    print cmd
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    outputLog("Stream net", process.stdout.readlines())

def Threshold(ssa, mask, threshold, inputProc, src, mpiexeDir = None, exeDir = None, hostfile = None):
    print "Stream definition according to threshold......"
    print "Input Accumulated Stream Source Grid: " + ssa
    if os.path.exists(mask):
        print "Input Mask Grid: " + mask
    print "Threshold: " + str(threshold)
    print "Input Number of Processes: " + str(inputProc)

    print "Output Stream Raster Grid: " + src

    # Construct command
    cmd = MPIHeader(mpiexeDir, inputProc, hostfile)

    if exeDir is None:
        cmd = cmd + str(inputProc) + ' threshold -ssa ' + '"' + ssa + '"' + ' -src ' + '"' + src + '"' + \
              ' -thresh ' + str(threshold)
    else:
        cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'threshold -ssa ' + '"' + ssa + '"' + ' -src ' + \
              '"' + src + '"' + ' -thresh ' + str(threshold)

    if os.path.exists(mask):
        cmd = cmd + ' -mask ' + mask

    print "Command Line: " + cmd
    # os.system(cmd)
    process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    outputLog("Threshold to define stream", process.stdout.readlines())

def StreamSkeleton(filledDem, streamSkeleton, inputProc, mpiexeDir=None, exeDir=None, hostfile = None):
    cmd = MPIHeader(mpiexeDir, inputProc, hostfile)
    if exeDir is not None:
        exe = exeDir + os.sep + "peukerdouglas"
    else:
        exe = "peukerdouglas"
    cmd += "%d %s -fel %s -ss %s" % (inputProc, exe, filledDem, streamSkeleton)

    print cmd
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    outputLog("Stream skeleton based on Peuker-Douglas", process.stdout.readlines())

def DropAnalysis(fel, p, ad8, ssa, shapefile, minthresh, maxthresh, numthresh, logspace, inputProc, drp,
                 mpiexeDir = None, exeDir = None, hostfile = None):
    print "Stream drop analysis for the optimal threshold......"
    print "Input Pit Filled Elevation Grid: " + fel
    print "Input D8 Flow Direction Grid: " + p
    print "Input D8 Contributing Area Grid: " + ad8
    print "Input Accumulated Stream Source Grid: " + ssa
    print "Input Outlets Shapefile: " + shapefile
    print "Minimum Threshold Value: " + str(minthresh)
    print "Maximum Threshold Value: " + str(maxthresh)
    print "Number of Threshold Values: " + str(numthresh)
    if logspace:
        print "Spacing method: logarithmic spacing"
    else:
        print "Spacing method: linear spacing"
    print "Input Number of Processes: " + str(inputProc)

    print "Output Drop Analysis Text File: " + drp

    # Construct command
    cmd = MPIHeader(mpiexeDir, inputProc, hostfile)

    if exeDir is None:
        cmd = cmd + str(inputProc) + ' dropanalysis -fel ' + '"' + fel + '"' + ' -p ' + '"' + p + '"' + ' -ad8 ' +\
              '"' + ad8 + '"' + ' -ssa ' + '"' + ssa + '"' + ' -o ' + '"' + shapefile + '"' + ' -drp ' + '"' + drp + \
              '"' + ' -par ' + str(minthresh) + ' ' + str(maxthresh) + ' ' + str(numthresh) + ' '
    else:
        cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'dropanalysis -fel ' + '"' + fel + '"' + ' -p ' + \
              '"' + p + '"' + ' -ad8 ' + '"' + ad8 + '"' + ' -ssa ' + '"' + ssa + '"' + ' -o ' + '"' + shapefile + \
              '"' + ' -drp ' + '"' + drp + '"' + ' -par ' + str(minthresh) + ' ' + str(maxthresh) + ' ' +\
              str(numthresh) + ' '
    if logspace:
        cmd += '0'
    else:
        cmd += '1'

    print "Command Line: " + cmd
    # os.system(cmd)
    process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    outputLog("Drop analysis", process.stdout.readlines())


####   Functions added by Liangjun Zhu    ####

def D8DistDownToStream(p, fel, src, dist, distancemethod, thresh, inputProc, mpiexeDir = None, exeDir = None,
                       hostfile = None):
    print "Calculating distance down to stream based on D8 model......"
    print "Input D8 Flow Direction Grid: " + p
    print "Input filled DEM: " + fel
    print "Input Stream Raster Grid: " + src
    print "Distance calculating method: " + distancemethod
    print "Threshold: " + str(thresh)
    print "Input Number of Processes: " + str(inputProc)
    print "Output Distance To Streams: " + dist
    if StringMatch(distancemethod, 'Horizontal'):
        distmeth = 'h'
    elif StringMatch(distancemethod, 'Vertical'):
        distmeth = 'v'
    elif StringMatch(distancemethod, 'Pythagoras'):
        distmeth = 'p'
    elif StringMatch(distancemethod, 'Surface'):
        distmeth = 's'
    else:
        distmeth = 's'
    cmd = MPIHeader(mpiexeDir, inputProc, hostfile)

    if exeDir is None:
        cmd = cmd + str(inputProc) + ' d8distdowntostream -p ' + '"' + p + '"' + ' -fel ' + '"' + fel + '"' + \
              ' -src ' + '"' + src + '"' + ' -dist ' + '"' + dist + '"' + ' -m ' + distmeth + ' -thresh ' + str(thresh)
    else:
        cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'd8distdowntostream -p ' + '"' + p + '"' + ' -fel ' + \
              '"' + fel + '"' + ' -src ' + '"' + src + '"' + ' -dist ' + '"' + dist + '"' + ' -m ' + distmeth + \
              ' -thresh ' + str(thresh)

    print "Command Line: " + cmd
    # os.system(cmd)
    process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    outputLog("D8 distance down", process.stdout.readlines())


def D8DistUpToRidge(p, fel, du, distancemethod, statisticalmethod, inputProc, rdg = None, mpiexeDir = None,
                    exeDir = None, hostfile = None):
    print "Calculating distance up to ridges based on D8 model......"
    print "Input D8 Flow Direction Grid: " + p
    print "Input Pit Filled Elevation Grid: " + fel
    if not rdg is None:
        print "Input Ridge Source Grid: " + rdg
    print "Statistical Method: " + statisticalmethod
    print "Distance Method: " + distancemethod
    print "Input Number of Processes: " + str(inputProc)
    print "Output D-Infinity Distance Up: " + du

    # Construct command
    if StringMatch(statisticalmethod, 'Average'):
        statmeth = 'ave'
    elif StringMatch(statisticalmethod, 'Maximum'):
        statmeth = 'max'
    elif StringMatch(statisticalmethod,'Minimum'):
        statmeth = 'min'
    else:
        statmeth = 'ave'
    if StringMatch(distancemethod, 'Horizontal'):
        distmeth = 'h'
    elif StringMatch(distancemethod, 'Vertical'):
        distmeth = 'v'
    elif StringMatch(distancemethod, 'Pythagoras'):
        distmeth = 'p'
    elif StringMatch(distancemethod, 'Surface'):
        distmeth = 's'
    else:
        distmeth = 's'

    cmd = MPIHeader(mpiexeDir, inputProc, hostfile)
    if exeDir is None:
        cmd = cmd + str(inputProc) + ' d8distuptoridge -p '
    else:
        cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'd8distuptoridge -p '
    if not rdg is None:
        cmd = cmd + '"' + p + '"' + ' -fel ' + '"' + fel + '"' + ' -rdg ' + '"' + rdg + '"' + ' -du ' + '"' + du + \
              '"' + ' -m ' + statmeth + ' ' + distmeth
    else:
        cmd = cmd + '"' + p + '"' + ' -fel ' + '"' + fel + '"' + ' -du ' + '"' + du + '"' + ' -m ' + statmeth + \
              ' ' + distmeth

    print "Command Line: " + cmd
    # os.system(cmd)
    process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    outputLog("D8 distance up", process.stdout.readlines())


def DinfDistUpToRidge(ang, fel, slp, propthresh, statisticalmethod, distancemethod, edgecontamination, inputProc, du,
                      rdg = None, mpiexeDir = None, exeDir = None, hostfile = None):
    print "Calculating distance up to ridges based on D-infinity model......"
    print "Input D-Infinity Flow Direction Grid: " + ang
    print "Input Pit Filled Elevation Grid: " + fel
    print "Input Slope Grid: " + slp
    if not rdg is None:
        print "Input Ridge Source Grid: " + rdg
    print "Input Proportion Threshold: " + str(propthresh)
    print "Statistical Method: " + statisticalmethod
    print "Distance Method: " + distancemethod
    print "Edge Contamination: " + edgecontamination
    print "Input Number of Processes: " + str(inputProc)

    print "Output D-Infinity Distance Up: " + du

    # Construct command
    if StringMatch(statisticalmethod, 'Average'):
        statmeth = 'ave'
    elif StringMatch(statisticalmethod, 'Maximum'):
        statmeth = 'max'
    elif StringMatch(statisticalmethod,'Minimum'):
        statmeth = 'min'
    else:
        statmeth = 'ave'
    if StringMatch(distancemethod, 'Horizontal'):
        distmeth = 'h'
    elif StringMatch(distancemethod, 'Vertical'):
        distmeth = 'v'
    elif StringMatch(distancemethod, 'Pythagoras'):
        distmeth = 'p'
    elif StringMatch(distancemethod, 'Surface'):
        distmeth = 's'
    else:
        distmeth = 's'

    cmd = MPIHeader(mpiexeDir, inputProc, hostfile)

    if exeDir is None:
        cmd = cmd + str(inputProc) + ' dinfdistuptoridge '
    else:
        cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'dinfdistuptoridge '
    if not rdg is None:
        cmd = cmd + ' -ang ' + '"' + ang + '"' + ' -fel ' + '"' + fel + '"' + ' -slp ' + '"' + slp + '"' + \
              ' -rdg ' + '"' + rdg + '"' + ' -du ' + '"' + du + '"' + ' -m ' + statmeth + ' ' + distmeth + \
              ' -thresh ' + str(propthresh)
    else:
        cmd = cmd + ' -ang ' + '"' + ang + '"' + ' -fel ' + '"' + fel + '"' + ' -slp ' + '"' + slp + '"' + \
              ' -du ' + '"' + du + '"' + ' -m ' + statmeth + ' ' + distmeth + ' -thresh ' + str(propthresh)
    if StringMatch(edgecontamination, 'false') or edgecontamination is False:
        cmd += ' -nc '

    print "Command Line: " + cmd
    # os.system(cmd)
    process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    outputLog("Dinf distance up", process.stdout.readlines())


def Curvature(inputProc, fel, prof = None, plan = None, horiz = None, unspher = None, ave = None, max = None,
              min = None, mpiexeDir = None, exeDir = None, hostfile = None):
    cmd = MPIHeader(mpiexeDir, inputProc, hostfile)

    if exeDir is None:
        cmd = cmd + str(inputProc) + ' curvature'
    else:
        cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'curvature'
    if prof is None and plan is None and horiz is None and unspher is None and ave is None and \
                    max is None and min is None:
        cmd = cmd + ' -fel ' + '"' + fel + '"'
    else:
        cmd = cmd + ' -fel ' + '"' + fel + '"' + ' -out '
    print "Input Pit Filled Elevation Grid: " + fel
    if not prof is None:
        print "Output Profile Curvature Grid: " + prof
        cmd = cmd + ' -prof ' + '"' + prof + '" '
    if not plan is None:
        print "Output Plan Curvature Grid: " + plan
        cmd = cmd + ' -plan ' + '"' + plan + '" '
    if not horiz is None:
        print "Output Horizontal Curvature Grid: " + horiz
        cmd = cmd + ' -horiz ' + '"' + horiz + '" '
    if not unspher is None:
        print "Output Nnsphericity Grid: " + unspher
        cmd = cmd + ' -unspher ' + '"' + unspher + '" '
    if not ave is None:
        print "Output Average Curvature Grid: " + ave
        cmd = cmd + ' -ave ' + '"' + ave + '" '
    if not max is None:
        print "Output Maximum Curvature Grid: " + max
        cmd = cmd + ' -max ' + '"' + max + '" '
    if not min is None:
        print "Output Minimum Curvature Grid: " + min
        cmd = cmd + ' -min ' + '"' + min + '" '

    print "Command Line: " + cmd
    print "Input Number of Processes: " + str(inputProc)
    # os.system(cmd)
    process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    outputLog("Curvature", process.stdout.readlines())


def SelectTypLocSlpPos(inputConf, outputConf, inputProc, outlog = None, mpiexeDir = None, exeDir = None,
                       hostfile = None):
    print "Selecting Typical Slope Position Location and Calculating Fuzzy Inference Parameters"
    print "    Input configuration file: " + inputConf
    print "    Output configuration file: " + outputConf
    if outlog is not None:
        print "    Output Log file: " + outlog
    cmd = MPIHeader(mpiexeDir, inputProc, hostfile)

    if exeDir is None:
        cmd = cmd + str(inputProc) + ' selecttyplocslppos ' + '"' + inputConf + '"' + ' "' + outputConf + '"'
    else:
        cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'selecttyplocslppos ' + '"' + inputConf + \
              '"' + ' "' + outputConf + '"'
    if outlog is not None:
        cmd = cmd + ' "' + outlog + '" '

    print "Command Line: " + cmd
    print "Input Number of Processes: " + str(inputProc)
    ##os.system(cmd)
    process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    title = "Select Typical Location of %s" % inputConf.rpartition(os.sep)[-1]
    outputLog(title, process.stdout.readlines())


def FuzzySlpPosInference(config, inputProc, mpiexeDir = None, exeDir = None, hostfile = None):
    print "Fuzzy Slope Position Inference"
    print "    Configuration file: " + config
    cmd = MPIHeader(mpiexeDir, inputProc, hostfile)

    if exeDir is None:
        cmd = cmd + str(inputProc) + ' fuzzyslpposinference ' + '"' + config + '"'
    else:
        cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'fuzzyslpposinference ' + '"' + config + '"'

    print "Command Line: " + cmd
    print "Input Number of Processes: " + str(inputProc)
    ##os.system(cmd)
    process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    title = "Fuzzy Slope Position Inference of %s" % config.rpartition(os.sep)[-1]
    outputLog(title, process.stdout.readlines())


def HardenSlpPos(rdg, shd, bks, fts, vly, inputProc, hard, maxsimi, sechard = None, secsimi = None, spsim = None,
                 spsi = None, mpiexeDir = None, exeDir = None, hostfile = None):
    print "Harden Slope Position Inference"
    print "Ridge Similarity file: " + rdg
    print "Shoulder slope similarity file: " + shd
    print "Back slope similarity file: " + bks
    print "Foot slope similarity file: " + fts
    print "Valley similarity file: " + vly
    print "Hard slope position file: " + hard
    print "Maximum similarity: " + maxsimi
    cmd = MPIHeader(mpiexeDir, inputProc, hostfile)

    if exeDir is None:
        cmd = cmd + str(inputProc) + ' hardenslppos -rdg ' + '"' + rdg + '"' + ' -shd ' + '"' + shd + '"' + \
              ' -bks ' + '"' + bks + '"' + ' -fts ' + '"' + fts + '"' + ' -vly ' + '"' + vly + '"' + \
              ' -maxS ' + '"' + hard + '" ' + '"' + maxsimi + '"'
    else:
        cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'hardenslppos -rdg ' + '"' + rdg + '"' + ' -shd ' + \
              '"' + shd + '"' + ' -bks ' + '"' + bks + '"' + ' -fts ' + '"' + fts + '"' + ' -vly ' + '"' + \
              vly + '"' + ' -maxS ' + '"' + hard + '" ' + '"' + maxsimi + '"'
    if (not sechard is None) and (not secsimi is None):
        print "Second Hard slope position file: " + sechard
        print "Second Maximum similarity: " + secsimi
        cmd = cmd + ' -secS ' + '"' + sechard + '" ' + '"' + secsimi + '"'
        if (not spsim is None) and (not spsi is None):
            print "Slope Position Sequence Index: " + spsi
            cmd = cmd + ' -m ' + str(spsim) + ' "' + spsi + '"'

    print "Command Line: " + cmd
    print "Input Number of Processes: " + str(inputProc)
    ##os.system(cmd)
    process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    outputLog("Harden classification", process.stdout.readlines())


def SimpleCalculator(inputa, inputb, output, operator, inputProc, mpiexeDir = None, exeDir = None, hostfile = None):
    cmd = MPIHeader(mpiexeDir, inputProc, hostfile)

    if exeDir is None:
        cmd = cmd + str(inputProc) + ' simplecalculator -in ' + '"' + inputa + '"' + ' "' + inputb + '"' + \
              ' -out ' + '"' + output + '"' + ' -op ' + str(operator)
    else:
        cmd = cmd + str(inputProc) + ' ' + exeDir + os.sep + 'simplecalculator -in ' + '"' + inputa + '"' + ' "' + \
              inputb + '"' + ' -out ' + '"' + output + '"' + ' -op ' + str(operator)

    print "Command Line: " + cmd
    print "Input Number of Processes: " + str(inputProc)
    ##os.system(cmd)
    process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    outputLog("Simple Calculator", process.stdout.readlines())

def RPISkidmore(vlysrc, rdgsrc, rpi, inputProc, vlytag=1, rdgtag=1, dist2vly=None, dist2rdg=None,
                mpiexeDir = None, exeDir = None,hostfile = None):
    cmd = MPIHeader(mpiexeDir, inputProc, hostfile)
    if exeDir is not None:
        exe = exeDir + os.sep + "rpiskidmore"
    else:
        exe = "rpiskidmore"
    cmd += " %d %s -vly %s -rdg %s -rpi %s" % (inputProc, exe, vlysrc, rdgsrc, rpi)
    if vlytag > 0:
        cmd += " -vlytag %d" % vlytag
    if rdgtag > 0:
        cmd += " -rdgtag %d" % rdgtag
    if dist2vly is not None:
        cmd += " -dist2vly %s" % dist2vly
    if dist2rdg is not None:
        cmd += " -dist2rdg %s" % dist2rdg
    print cmd
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    outputLog("RPI (skidmore, 1990)", process.stdout.readlines())
####           END DEFINITION             ####
