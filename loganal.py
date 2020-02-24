#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-

import os
import sys
import re
import shutil
import optparse
import datetime
import threading

msgtpptn = re.compile('^\s*\[.*\]\s*(?P<msgtp>(.*))\s*:\s*(?P<msgcont>.*)$')

spdptn = re.compile('^\s*(?P<kmph>\d*\.\d)*km/h\s*\(\s*(?P<spdnum>\d*)\)\s*$')

svsptn = re.compile(
    '.*?(?P<spv>unknown|invalid|true|false|CONTROLLED_ACCESS|ROUNDABOUT|MULTIPLY_DIGITIZE D|MAPPROVIDER|NAVINFO|EFFSL_IMPLICIT).*?',
    re.IGNORECASE)
inumptn = re.compile('.*_(?P<inum>\d+).*')

msgLastIndexPosition = 0
msgLastIndexStub = 0
msgLastIndexSegment = 0
msgLastIndexProfileShort = 0
msgLastIndexProfileLong = 0
msgLastIndexMetadata = 0

msgPositionLastTimestamp = 0

msgSegmentLastOffset = 0

maxtsp = 0
mintsp = 0
avgtsp = 0
avgtsperr = 0

msgPositionCounter = 0
msgPositionCounterErr = 0

msgStubCounter = 0
msgStubCounterErr = 0

msgSegmentCounter = 0
msgSegmentCounterErr = 0

msgProfileShortCounter = 0
msgProfileShortCounterErr = 0

msgProfileLongCounter = 0
msgProfileLongCounterErr = 0

msgMetadataCounter = 0
msgMetadataCounterErr = 0

deflogfileh = None
defrenamefileh = None

msgcounter = 0
errmsgcounter = 0

msgtypes = {}
errmsgtypes = {}


def checkErr(errs, err):
    if err is not None:
        errs.append(err)


def getTypeKeyValue(ddict, msgtp, fkey):
    try:
        msgtypedict = ddict[msgtp]
    except:
        ddict[msgtp] = {}
        msgtypedict = ddict[msgtp]
    finally:
        try:
            fkeyvalue = msgtypedict[fkey]
        except:
            msgtypedict[fkey] = []
            fkeyvalue = msgtypedict[fkey]
        finally:
            return fkeyvalue


def setTypeKeyValue(ddict, msgtp, fkey, value):
    fkeyls = getTypeKeyValue(ddict, msgtp, fkey)
    fkeyls = value


def appendTypeKeyValue(ddict, msgtp, fkey, value):
    fkeyls = getTypeKeyValue(ddict, msgtp, fkey)
    if value in fkeyls or len(fkeyls) > 256:
        pass
    else:
        fkeyls.append(value)


def printDdict(ddict):
    infostr = '=' * 80 + '\n'
    infostr += 'there are ' + str(len(ddict)) + '\tmessage types:\t' + ', '.join(ddict.keys())
    print(infostr)
    if deflogfileh is not None:
        deflogfileh.write(infostr + '\n')
    for k, v in ddict.items():
        infostr = '\n' * 5 + '*' * 5 + k + '*' * 5 + '\n'
        infostr += '\tthere are ' + str(len(v)) + '\tfields:\t' + ', '.join(v.keys())
        print(infostr)
        if deflogfileh is not None:
            deflogfileh.write(infostr + '\n')
        for kk, vv in v.items():
            dots = ''
            if len(vv) > 64:
                svv = vv[0:64]
                dots = ', ...'
            else:
                svv = vv
            infostr = '\t' + kk + ' value list: ' + str(len(vv)) + '\n'
            infostr += '\t\t' + ', '.join(svv) + dots
            print(infostr)
            if deflogfileh is not None:
                deflogfileh.write(infostr + '\n')


def checkRange(msgd, key, low, high, errs=[], desp='', notinls=[], mustinls=[]):
    global svsptn, inumptn, msgtypes, errmsgtypes
    err = None
    try:
        valstr = msgd[key]
        try:
            bSpecialValue = False
            value = int(msgd[key])
        except ValueError as e:
            svm = svsptn.match(valstr)
            if svm is not None:
                spcialvalue = svm.group('spv')
                bSpecialValue = True
            else:
                inumm = inumptn.match(valstr)
                if inumm is not None:
                    # print(valstr)
                    value = int(inumm.group('inum'))
        finally:
            if bSpecialValue:
                appendTypeKeyValue(msgtypes, msgd['msgtp'], key, valstr)
                pass
            else:
                appendTypeKeyValue(msgtypes, msgd['msgtp'], key, valstr)
                if desp == '':
                    desp = key
                if value < low or value > high:
                    #### for Stub patch
                    if key == 'subPath' and value == 0 and int(msgd['ofs']) == 8191:
                        pass
                    else:
                        err = '***** ' + desp + ' error *****: out of range [' + str(low) + ', ' + str(
                            high) + '], this =' + str(value) + '(' + str(hex(value)) + ')'
                        appendTypeKeyValue(errmsgtypes, msgd['msgtp'], key, valstr)
                if value in notinls:
                    notinlsstr = ''
                    for i in notinls:
                        notinlsstr += str(i) + ', '
                    err = '***** ' + desp + ' error *****: should not be in [' + notinlsstr + '], this =' + str(value)
                    appendTypeKeyValue(errmsgtypes, msgd['msgtp'], key, valstr)
                if len(mustinls) > 0 and value not in mustinls:
                    mustinlsstr = ''
                    for i in mustinls:
                        mustinlsstr += str(i) + ', '
                    err = '***** ' + desp + ' error *****: should must in [' + mustinlsstr + '], this =' + str(value)
                    appendTypeKeyValue(errmsgtypes, msgd['msgtp'], key, valstr)
    except Exception as e:
        err = str(e)
        appendTypeKeyValue(errmsgtypes, msgd['msgtp'], 'nofield', key)

    checkErr(errs, err)


def handlePosition(msgd):
    errs = []
    global spdptn, msgLastIndexPosition, msgPositionLastTimestamp, msgPositionCounter, msgPositionCounterErr, msgtypes, errmsgtypes
    msgPositionCounter += 1
    if msgd is not None:
        try:
            checkRange(msgd, 'path', 0, 63, errs, 'path id')
            checkRange(msgd, 'ofs', 0, 8190, errs, 'offset')
            checkRange(msgd, 'vstat', -65536, 65536, errs, 'vstat')
            checkRange(msgd, 'index', 0, 3, errs, 'position index')
            checkRange(msgd, 'age', 0, 511, errs, 'age')
            checkRange(msgd, 'heading', 0, 255, errs, 'heading')
            checkRange(msgd, 'probability', 0, 100, errs, 'probability')
            checkRange(msgd, 'confidence', 0, 6, errs, 'confidence')
            checkRange(msgd, 'lane', 0, 7, errs, 'lane')

            ####### check index sequence
            err = None
            idx = int(msgd['index'])
            if idx == 0 or idx == msgLastIndexPosition + 1:
                msgLastIndexPosition = idx
            else:
                err = '***** index error *****: last = ' + str(msgLastIndexPosition) + ', this = ' + str(idx)
                appendTypeKeyValue(errmsgtypes, msgd['msgtp'], 'index', str(idx))
            checkErr(errs, err)

            ####### check speed range
            err = None
            speedstr = msgd['speed']
            sm = spdptn.match(speedstr)
            spdkmph = float(sm.group('kmph'))
            if spdkmph < (-12.8 * 3.6) or spdkmph > (89.2 * 3.6):
                err = '***** speed error *****: out of range [-12.8*3.6, 89.2*3.6] km/h, this =' + speedstr
                appendTypeKeyValue(errmsgtypes, msgd['msgtp'], 'speed', speedstr)
            appendTypeKeyValue(msgtypes, msgd['msgtp'], 'speed', speedstr)
            checkErr(errs, err)

            ####### check time span
            global maxtsp, mintsp, avgtsp, avgtsperr

            err = None
            timestamp = int(msgd['nTimestamp'])
            if msgPositionLastTimestamp == 0:
                msgPositionLastTimestamp = timestamp
            timespan = timestamp - msgPositionLastTimestamp
            if timespan > maxtsp:
                maxtsp = timespan
            if timespan < mintsp:
                mintsp = timespan
            if avgtsp == 0:
                avgtsp = timespan
            else:
                avgtsp = (avgtsp + timespan) / 2.0
            if timespan > 10000:
                if avgtsperr == 0:
                    avgtsperr = timespan
                else:
                    avgtsperr = (avgtsperr + timespan) / 2.0
                err = '***** time span error ***** ' + str(timespan) + '> 10000 : last = ' + str(
                    msgPositionLastTimestamp) + ', this = ' + str(timestamp)
                msgPositionCounterErr += 1
                appendTypeKeyValue(errmsgtypes, msgd['msgtp'], 'timespan', str(timespan))
            appendTypeKeyValue(msgtypes, msgd['msgtp'], 'timespan', str(timespan))
            msgPositionLastTimestamp = timestamp
            checkErr(errs, err)

        except Exception as e:
            err = str(e)
            checkErr(errs, err)
            pass
    return errs


def handleStub(msgd):
    errs = []
    global msgStubCounter, msgStubCounterErr, msgLastIndexStub
    if msgd is not None:
        try:
            err = None
            checkRange(msgd, 'path', 0, 63, errs, 'path id', notinls=range(1, 8))
            checkRange(msgd, 'ofs', 0, 8191, errs, 'offset')
            checkRange(msgd, 'update', 0, 1, errs, 'Update')
            checkRange(msgd, 'subPath', 5, 63, errs, 'subpath id', notinls=[7])
            checkRange(msgd, 'turnAngle', 0, 255, errs, 'turn angle')  # TODO: check the range
            checkRange(msgd, 'formOfWay', 0, 15, errs, 'form of way')
            checkRange(msgd, 'relativeProbability', 0, 100, errs, 'relative probability')
            checkRange(msgd, 'lanesInDrivDir', 0, 7, errs, 'lanes in driving direction')
            checkRange(msgd, 'lanesInOppoDir', 0, 3, errs, 'lanes in opposite direction')
            checkRange(msgd, 'isRightOfWay', 0, 3, errs, 'right of way')
            checkRange(msgd, 'isLastStubAtOffset', 0, 1, errs, 'last stub at offset')
            checkRange(msgd, 'isCalRoute', 0, 2, errs, 'part of calculated route')
            checkRange(msgd, 'isComplexIntersection', 0, 3, errs, 'complex intersection')
            checkRange(msgd, 'functionalClass', 0, 7, errs, 'functional class')
            # ####### check index sequence
            # idx = int(msgd['index'])
            # if idx == 0 or idx == msgLastIndexStub + 1:
            #   msgLastIndexStub = idx
            # else:
            #   err = '***** index error *****: last = ' + str(msgLastIndexStub) + ', this = ' + str(idx)

        except Exception as e:
            err = str(e)
            checkErr(errs, err)
            pass
    return errs


def handleSegment(msgd):
    errs = []
    global msgSegmentCounter, msgSegmentCounterErr, msgLastIndexSegment, msgSegmentLastOffset, errmsgtypes

    msgSegmentCounter += 1
    if msgd is not None:
        try:
            err = None
            checkRange(msgd, 'path', 4, 63, errs, 'path id', notinls=[5, 6, 7])
            checkRange(msgd, 'ofs', 0, 8191, errs, 'offset')
            checkRange(msgd, 'update', 0, 1, errs, 'Update')
            checkRange(msgd, 'funcClass', 0, 7, errs, 'functional class')
            checkRange(msgd, 'formOfWay', 0, 15, errs, 'form of way')
            checkRange(msgd, 'speedLimit', 5, 160, errs, 'speed limit')  # TODO: check the range
            checkRange(msgd, 'speedLimitType', 0, 8, errs, 'speed limit type')
            checkRange(msgd, 'lanesInDrivDir', 0, 7, errs, 'lanes in driving direction')
            checkRange(msgd, 'lanesInOppoDir', 0, 3, errs, 'lanes in opposite direction')
            checkRange(msgd, 'isTunnel', 0, 3, errs)
            checkRange(msgd, 'isBridge', 0, 3, errs)
            checkRange(msgd, 'isDivRoad', 0, 3, errs)
            checkRange(msgd, 'isBuildUpArea', 0, 3, errs)
            checkRange(msgd, 'isCalRoute', 0, 2, errs, 'part of calculated route')
            checkRange(msgd, 'isComplexIntersection', 0, 3, errs, 'is complex intersection')
            checkRange(msgd, 'relativeProbability', 0, 100, errs, 'relative probability')

            # ####### check index sequence
            # idx = int(msgd['index'])
            # if idx == 0 or idx == msgLastIndexSegment + 1:
            #   msgLastIndexSegment = idx
            # else:
            #   err = '***** index error *****: last = ' + str(msgLastIndexSegment) + ', this = ' + str(idx)
            ####### check time span

            offset = int(msgd['ofs'])
            if msgSegmentLastOffset == 0:
                msgSegmentLastOffset = offset
            doffset = offset - msgSegmentLastOffset
            if doffset > 1000:
                err = '***** offset error ***** ' + str(doffset) + '> 1000 : last = ' + str(
                    msgSegmentLastOffset) + ', this = ' + str(offset)
                appendTypeKeyValue(errmsgtypes, msgd['msgtp'], 'ofs', str(doffset))
                msgSegmentCounterErr += 1
            msgSegmentLastOffset = offset


        except Exception as e:
            err = str(e)
            checkErr(errs, err)
            pass
    return errs


def handleProfileShort(msgd):
    errs = []
    global msgProfileShortCounter, msgProfileShortCounterErr, msgLastIndexProfileShort
    if msgd is not None:
        try:
            err = None
            checkRange(msgd, 'type', 0, 31, errs, 'profile type')
            checkRange(msgd, 'isCtrlPoint', 0, 1, errs)
            checkRange(msgd, 'isUpdate', 0, 1, errs, 'is update')
            checkRange(msgd, 'value', 0, 1023, errs, 'value')
            checkRange(msgd, 'accuracyClass', 0, 3, errs)
            checkRange(msgd, 'path', 8, 63, errs, 'path id')
            checkRange(msgd, 'offs', 0, 8191, errs, 'offset')

            # ####### check index sequence
            # idx = int(msgd['index'])
            # if idx == 0 or idx == msgLastIndexProfileShort + 1:
            #   msgLastIndexProfileShort = idx
            # else:
            #   err = '***** index error *****: last = ' + str(msgLastIndexProfileShort) + ', this = ' + str(idx)

        except Exception as e:
            err = str(e)
            checkErr(errs, err)
            pass
    return errs


def handleProfileLong(msgd):
    errs = []
    global msgProfileLongCounter, msgProfileLongCounterErr, msgLastIndexProfileLong
    if msgd is not None:
        try:
            err = None
            checkRange(msgd, 'type', 0, 31, errs, 'profile type')
            checkRange(msgd, 'isCtrlPoint', 0, 1, errs)
            checkRange(msgd, 'isUpdate', 0, 1, errs, 'is update')
            checkRange(msgd, 'value', 0, pow(2, 32) - 1, errs, 'value')
            # checkRange(msgd, 'accuracyClass', 255, 255, errs)
            checkRange(msgd, 'path', 8, 63, errs, 'path id')
            checkRange(msgd, 'offs', 0, 8191, errs, 'offset')
            # ####### check index sequence
            # idx = int(msgd['index'])
            # if idx == 0 or idx == msgLastIndexProfileLong + 1:
            #   msgLastIndexProfileLong = idx
            # else:
            #   err = '***** index error *****: last = ' + str(msgLastIndexProfileLong) + ', this = ' + str(idx)

        except Exception as e:
            err = str(e)
            checkErr(errs, err)
            pass
    return errs


def handleMetadata(msgd):
    errs = []
    global msgMetadataCounter, msgMetadataCounterErr, msgLastIndexMetadata
    if msgd is not None:
        try:
            err = None
            checkRange(msgd, 'countryCode', 0, 1023, errs)
            checkRange(msgd, 'regionCode', 0, 32767, errs)
            checkRange(msgd, 'drivingSideRight', 0, 1, errs)
            checkRange(msgd, 'speedUnitMPH', 0, 1, errs)
            # checkRange(msgd, 'mapProvider', 0, 7, errs)
            # checkRange(msgd, 'protocolVersion', 0, 3, errs)
            # checkRange(msgd, 'mapVersion', 0, 8191, errs)
            checkRange(msgd, 'hardwareVersion', 0, 511, errs)
            # ####### check index sequence
            # idx = int(msgd['index'])
            # if idx == 0 or idx == msgLastIndexMetadata + 1:
            #   msgLastIndexMetadata = idx
            # else:
            #   err = '***** index error *****: last = ' + str(msgLastIndexMetadata) + ', this = ' + str(idx)

        except Exception as e:
            err = str(e)
            checkErr(errs, err)
            pass
    return errs


def handleMsg(msgcont):
    msgdict = {}
    if msgcont is not None:
        msgfls = msgcont.split(',')
        for itf in msgfls:
            itfp = itf.split('=')
            if len(itfp) == 2:
                msgdict[itfp[0].strip()] = itfp[1].strip()
    return msgdict


def handleFile(infile):
    global msgtpptn, deflogfileh, defrenamefileh, msgcounter, errmsgcounter, msgtypes, errmsgtypes
    fstr = '\n' * 5 + 'handling file: ' + infile + '\n'
    if deflogfileh is not None:
        try:
            deflogfileh.write(fstr.encode('utf-8'))
        except:
            deflogfileh.write(fstr)
    utf8fn = infile  # .encode('utf-8')
    global msgLastIndexPosition, msgPositionLastTimestamp

    msgLastIndexPosition = 0
    msgPositionLastTimestamp = 0
    if os.path.isfile(utf8fn):
        fh = open(utf8fn)
        lnum = 0
        for ln in fh:
            lnum += 1
            m = msgtpptn.match(ln.strip())
            if m != None:
                msgcounter += 1
                msgtp = m.group('msgtp').strip()
                msgcont = m.group('msgcont').strip()
                msgdict = handleMsg(msgcont)
                msgdict['msgtp'] = msgtp
                # if msgcont is not None:
                #   msgfls = msgcont.split(',')
                #   for itf in msgfls:
                #     itfp = itf.split('=')
                #     if len(itfp) == 2:
                #       msgdict[itfp[0].strip()] = itfp[1].strip()
                err = []
                if msgtp == 'Position':
                    err = handlePosition(msgdict)
                elif msgtp == 'Stub':
                    err = handleStub(msgdict)
                elif msgtp == 'Segment':
                    err = handleSegment(msgdict)
                elif msgtp == 'Profile Short':
                    err = handleProfileShort(msgdict)
                elif msgtp == 'Profile Long':
                    err = handleProfileLong(msgdict)
                elif msgtp == 'Metadata':
                    err = handleMetadata(msgdict)

                if len(err):
                    errstr = (''  # + 'Exception at line ' + str(lnum)  + ' in file ' + infile + ': ' + '\n'
                              # + msgtp + '\t' + msgcont + '----->\n'
                              + ln.strip() + ' ----->\n'
                              + '\t' + '\n\t'.join(err) + '\n')
                    print(errstr)
                    if deflogfileh is not None:
                        try:
                            deflogfileh.write(errstr.encode('utf-8'))
                        except:
                            deflogfileh.write(errstr)
                    errmsgcounter += 1
                    if msgtp not in errmsgtypes:
                        errmsgtypes.append(msgtp)
        fh.close()
    else:
        print('!!!not a file!!!  ' + utf8fn)


def handlePath(infile, bRename=False):
    global defrenamefileh, deflogfileh
    try:
        fname = os.path.basename(infile).decode('utf-8')
        fdirn = os.path.abspath(os.path.dirname(infile).decode('utf-8'))
    except AttributeError:
        fname = os.path.basename(infile)
        fdirn = os.path.abspath(os.path.dirname(infile))
    finally:
        ofname = os.path.join(fdirn, fname)

        if deflogfileh is None:
            deflogfileh = open(os.path.join(fdirn, 'anal.log'), 'a')

        if bRename:
            if defrenamefileh is None:
                defrenamefileh = open(os.path.join(fdirn, 'rename.log'), 'a')

            nfname = os.path.abspath(os.path.join(fdirn, '_' + fname))
            lines = ''
            if os.path.isfile(ofname):
                try:
                    os.rename(ofname, nfname)
                    # shutil.move(ofname.encode('utf-8'), nfname.encode('utf-8'))
                    line = ofname + '::>>' + nfname + '\n'
                    lines += line
                    if defrenamefileh is not None:
                        try:
                            defrenamefileh.write(lines.encode('utf-8'))
                        except:
                            defrenamefileh.write(lines)
                except Exception as e:
                    print('!!!!! rename failed !!!!!  ' + ofname + '' + str(e))
                    nfname = ofname
            return nfname
        else:
            return ofname


def handleFiles(fls):
    print('----- finding files -----\n')
    print(fls)
    for i, fn in enumerate(fls):
        cfn = handlePath(fn, True)
        handleFile(cfn)
    global msgcounter, errmsgcounter, msgtypes, errmsgtypes
    if len(fls) > 0:
        printDdict(msgtypes)
        printDdict(errmsgtypes)
        print('total messages: ' + str(msgcounter) + '\t exception messages: ' + str(errmsgcounter))


def getFolderFiles(folder):
    fls = os.listdir(folder)
    fls.sort()
    filels = []
    for nn in fls:
        if nn.startswith('Debug_Av2') and nn.endswith('.txt'):
            filels.append(os.path.join(folder, nn))
    return filels


defargfolder = ''


def handleFolder():
    global defargfolder, defrenamefileh

    if os.path.isfile(defargfolder):
        handleFiles([defargfolder])
    else:
        fls = getFolderFiles(defargfolder)
        handleFiles(fls)
        global maxtsp, mintsp, avgtsp, avgtsperr, msgPositionCounter, msgPositionCounterErr
        print('time span statics:')
        print('max', 'min', 'avg', 'avg err', 'position msgs', 'err position msgs')
        print(maxtsp, mintsp, avgtsp, avgtsperr, msgPositionCounter, msgPositionCounterErr)
    try:
        defrenamefileh.close()
        deflogfileh.close()
    except:
        pass
    queryt = threading.Timer(1.0, handleFolder)
    queryt.start()


def renameRB(folder):
    rnfname = os.path.join(folder, 'rename.log')
    if os.path.isfile(rnfname):
        rfh = open(rnfname)
        for ln in rfh:
            (npth, opth) = ln.strip().split('::>>')
            # print(lnls)
            try:
                os.rename(opth, npth)
                # shutil.move(npth, opth)
            except:
                pass
        rfh.close()

    fls = os.listdir(folder)
    fls.sort()
    filels = []
    for nn in fls:
        if nn.startswith('_Debug_Av2') and nn.endswith('.txt'):
            filels.append(os.path.join(folder, nn))
            os.rename(os.path.join(folder, nn), os.path.join(folder, nn[1:]))


def main():
    parser = optparse.OptionParser('%prog -f folder or file [-c BC]')

    parser.add_option('-f', dest='Folder', type='string', help='specify a folder or file')
    parser.add_option('-c', dest='Config', type='string',
                      help='configuration: B for renaming back the log file, C for clearing the outpupt')

    (options, args) = parser.parse_args()
    folder = options.Folder
    config = options.Config

    global defargfolder
    if folder is not None:
        defargfolder = folder
        if config is not None:
            dirname = defargfolder
            if os.path.isfile(defargfolder):
                dirname = os.path.dirname(defargfolder)
            if 'B' in config:
                renameRB(folder)
                rnfname = os.path.join(dirname, 'rename.log')
                if os.path.isfile(rnfname):
                    os.remove(rnfname)
            if 'C' in config:
                lgfname = os.path.join(dirname, 'anal.log')
                if os.path.isfile(lgfname):
                    os.remove(lgfname)
        else:
            handleFolder()

    else:
        # print('Please config a folder or file, by using -f')
        parser.print_help()


if __name__ == '__main__':
    main()
