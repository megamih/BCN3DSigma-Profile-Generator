#!/usr/bin/python -tt
# coding: utf-8

# Guillem Àvila Padró - Oct 2017
# Released under GNU LICENSE
# https://opensource.org/licenses/GPL-3.0

import math
import uuid
import os

import ProgenSettings as PS
import Logger

def simplify3DProfile(machine, printMode, hotendLeft, hotendRight, filamentLeft, filamentRight):
    if printMode not in machine['printMode'] or (printMode != 'regular' and (hotendLeft['id'] != hotendRight['id'] or filamentLeft['id'] != filamentRight['id'])):
        return
    elif printMode != 'regular':
        hotendRight = dict([('id', 'None')])
    fff = []
    fff.append('<?xml version="1.0" encoding="utf-8"?>')
    for q in PS.profilesData['quality']:
        if q['id'] == 'Standard':
            defaultPrintQualityBase = 'Standard'
            break
        else:
            defaultPrintQualityBase = PS.profilesData['quality'][0]['id']
    if hotendLeft['id'] == 'None':
        if hotendRight['id'] == 'None':
            return
        else:            
            fileName = "BCN3D "+machine['name']+" - Right Extruder "+str(hotendRight['nozzleSize'])+" Only ("+filamentRight['id']+")"
            defaultPrintQuality = 'Right Extruder - '+defaultPrintQualityBase
            extruderPrintOptions = ['Right Extruder']
            filamentLeft = dict([('id', '')])
    elif hotendRight['id'] == 'None':
        if printMode == 'regular':
            fileName = "BCN3D "+machine['name']+" - Left Extruder "+str(hotendLeft['nozzleSize'])+" Only ("+filamentLeft['id']+")"
            defaultPrintQuality = 'Left Extruder - '+defaultPrintQualityBase
        else:
            fileName = "BCN3D "+machine['name']+" - "+str(hotendLeft['nozzleSize'])+" "+printMode.title()+" Mode ("+filamentLeft['id']+")"
            defaultPrintQuality = printMode.title()+' Mode - '+defaultPrintQualityBase
        extruderPrintOptions = ['Left Extruder']
        filamentRight = dict([('id', '')])
    else:
        fileName = "BCN3D "+machine['name']+" - "+str(hotendLeft['nozzleSize'])+" Left ("+filamentLeft['id']+"), "+str(hotendRight['nozzleSize'])+" Right ("+filamentRight['id']+")"
        defaultPrintQuality = 'Left Extruder - '+defaultPrintQualityBase
        extruderPrintOptions = ['Left Extruder', 'Right Extruder', 'Both Extruders']
    fff.append('<profile name="'+fileName+'" version="ProGen '+PS.progenVersionNumber+' (Build '+PS.progenBuildNumber+')" app="S3D-Software 3.1.1">')
    fff.append('  <baseProfile></baseProfile>')
    fff.append('  <printMaterial></printMaterial>')
    fff.append('  <printQuality>'+defaultPrintQuality+'</printQuality>') #+extruder+secondaryExtruderAction+str(quality['id'])+
    if hotendLeft['id'] != 'None':
        fff.append('  <printExtruders>Left Extruder Only</printExtruders>')
    else:
        fff.append('  <printExtruders>Right Extruder Only</printExtruders>')        
    if hotendLeft['id'] != 'None':
        fff.append('  <extruder name="Left Extruder '+str(hotendLeft['nozzleSize'])+'">')
        fff.append('    <toolheadNumber>0</toolheadNumber>')
        fff.append('    <diameter>'+str(hotendLeft['nozzleSize'])+'</diameter>')
        fff.append('    <autoWidth>0</autoWidth>')
        fff.append('    <width>'+str(hotendLeft['nozzleSize'] * 0.875)+'</width>')
        fff.append('    <extrusionMultiplier>'+str(filamentLeft['extrusionMultiplier'])+'</extrusionMultiplier>')
        fff.append('    <useRetract>1</useRetract>')
        fff.append('    <retractionDistance>'+str(filamentLeft['retractionDistance'])+'</retractionDistance>')
        fff.append('    <extraRestartDistance>0</extraRestartDistance>')
        fff.append('    <retractionZLift>0.05</retractionZLift>')
        fff.append('    <retractionSpeed>'+str(filamentLeft['retractionSpeed']*60)+'</retractionSpeed>')
        fff.append('    <useCoasting>0</useCoasting>')
        fff.append('    <coastingDistance>0.2</coastingDistance>')
        fff.append('    <useWipe>1</useWipe>')
        fff.append('    <wipeDistance>5</wipeDistance>')
        fff.append('  </extruder>')
    else:
        fff.append('  <extruder name="">')
        fff.append('    <toolheadNumber>0</toolheadNumber>')
        fff.append('    <diameter>0</diameter>')
        fff.append('    <autoWidth>0</autoWidth>')
        fff.append('    <width>0</width>')
        fff.append('    <extrusionMultiplier>0</extrusionMultiplier>')
        fff.append('    <useRetract>0</useRetract>')
        fff.append('    <retractionDistance>0</retractionDistance>')
        fff.append('    <extraRestartDistance>0</extraRestartDistance>')
        fff.append('    <retractionZLift>0</retractionZLift>')
        fff.append('    <retractionSpeed>0</retractionSpeed>')
        fff.append('    <useCoasting>0</useCoasting>')
        fff.append('    <coastingDistance>0</coastingDistance>')
        fff.append('    <useWipe>1</useWipe>')
        fff.append('    <wipeDistance>0</wipeDistance>')
        fff.append('  </extruder>')
    if hotendRight['id'] != 'None':
        fff.append('  <extruder name="Right Extruder '+str(hotendRight['nozzleSize'])+'">')
        fff.append('    <toolheadNumber>1</toolheadNumber>')
        fff.append('    <diameter>'+str(hotendRight['nozzleSize'])+'</diameter>')
        fff.append('    <autoWidth>0</autoWidth>')
        fff.append('    <width>'+str(hotendRight['nozzleSize'] * 0.875)+'</width>')
        fff.append('    <extrusionMultiplier>'+str(filamentRight['extrusionMultiplier'])+'</extrusionMultiplier>')
        fff.append('    <useRetract>1</useRetract>')
        fff.append('    <retractionDistance>'+str(filamentRight['retractionDistance'])+'</retractionDistance>')
        fff.append('    <extraRestartDistance>0</extraRestartDistance>')
        fff.append('    <retractionZLift>0.05</retractionZLift>')
        fff.append('    <retractionSpeed>'+str(filamentRight['retractionSpeed']*60)+'</retractionSpeed>')
        fff.append('    <useCoasting>0</useCoasting>')
        fff.append('    <coastingDistance>0.2</coastingDistance>')
        fff.append('    <useWipe>1</useWipe>')
        fff.append('    <wipeDistance>5</wipeDistance>')
        fff.append('  </extruder>')
    fff.append('  <primaryExtruder>0</primaryExtruder>')
    fff.append('  <layerHeight>0.2</layerHeight>')
    fff.append('  <topSolidLayers>4</topSolidLayers>')
    fff.append('  <bottomSolidLayers>4</bottomSolidLayers>')
    fff.append('  <perimeterOutlines>3</perimeterOutlines>')
    fff.append('  <printPerimetersInsideOut>1</printPerimetersInsideOut>')
    fff.append('  <startPointOption>3</startPointOption>')
    fff.append('  <startPointOriginX>105</startPointOriginX>')
    fff.append('  <startPointOriginY>300</startPointOriginY>')
    fff.append('  <sequentialIslands>0</sequentialIslands>')
    fff.append('  <spiralVaseMode>0</spiralVaseMode>')
    fff.append('  <firstLayerHeightPercentage>125</firstLayerHeightPercentage>')
    fff.append('  <firstLayerWidthPercentage>100</firstLayerWidthPercentage>')
    fff.append('  <firstLayerUnderspeed>0.85</firstLayerUnderspeed>')
    fff.append('  <useRaft>0</useRaft>')
    fff.append('  <raftExtruder>0</raftExtruder>')
    fff.append('  <raftTopLayers>2</raftTopLayers>')
    fff.append('  <raftBaseLayers>2</raftBaseLayers>')
    fff.append('  <raftOffset>3</raftOffset>')
    fff.append('  <raftSeparationDistance>0.2</raftSeparationDistance>')
    fff.append('  <raftTopInfill>85</raftTopInfill>')    
    fff.append('  <aboveRaftSpeedMultiplier>0.3</aboveRaftSpeedMultiplier>')
    fff.append('  <useSkirt>1</useSkirt>')
    fff.append('  <skirtExtruder>999</skirtExtruder>')
    fff.append('  <skirtLayers>1</skirtLayers>')
    fff.append('  <skirtOutlines>2</skirtOutlines>')
    fff.append('  <skirtOffset>4</skirtOffset>')
    fff.append('  <usePrimePillar>0</usePrimePillar>')
    fff.append('  <primePillarExtruder>999</primePillarExtruder>')
    fff.append('  <primePillarWidth>15</primePillarWidth>')
    fff.append('  <primePillarLocation>7</primePillarLocation>')
    fff.append('  <primePillarSpeedMultiplier>1</primePillarSpeedMultiplier>')
    fff.append('  <useOozeShield>0</useOozeShield>')
    fff.append('  <oozeShieldExtruder>999</oozeShieldExtruder>')
    fff.append('  <oozeShieldOffset>2</oozeShieldOffset>')
    fff.append('  <oozeShieldOutlines>1</oozeShieldOutlines>')
    fff.append('  <oozeShieldSidewallShape>1</oozeShieldSidewallShape>')
    fff.append('  <oozeShieldSidewallAngle>30</oozeShieldSidewallAngle>')
    fff.append('  <oozeShieldSpeedMultiplier>1</oozeShieldSpeedMultiplier>')
    fff.append('  <infillExtruder>1</infillExtruder>')
    fff.append('  <internalInfillPattern>Grid</internalInfillPattern>')
    fff.append('  <externalInfillPattern>Rectilinear</externalInfillPattern>')
    fff.append('  <infillPercentage>20</infillPercentage>')
    fff.append('  <outlineOverlapPercentage>25</outlineOverlapPercentage>')
    fff.append('  <infillExtrusionWidthPercentage>100</infillExtrusionWidthPercentage>')
    fff.append('  <minInfillLength>3</minInfillLength>')
    fff.append('  <infillLayerInterval>1</infillLayerInterval>')
    fff.append('  <internalInfillAngles>45,-45</internalInfillAngles>')
    fff.append('  <overlapInternalInfillAngles>1</overlapInternalInfillAngles>')
    fff.append('  <externalInfillAngles>45,-45</externalInfillAngles>')
    fff.append('  <generateSupport>0</generateSupport>')
    fff.append('  <supportExtruder>0</supportExtruder>')
    fff.append('  <supportInfillPercentage>25</supportInfillPercentage>')
    fff.append('  <supportExtraInflation>1</supportExtraInflation>')
    fff.append('  <supportBaseLayers>0</supportBaseLayers>')
    fff.append('  <denseSupportExtruder>0</denseSupportExtruder>')
    fff.append('  <denseSupportLayers>5</denseSupportLayers>')
    fff.append('  <denseSupportInfillPercentage>75</denseSupportInfillPercentage>')
    fff.append('  <supportLayerInterval>1</supportLayerInterval>')

    fff.append('  <supportHorizontalPartOffset>0.7</supportHorizontalPartOffset>')
    fff.append('  <supportUpperSeparationLayers>1</supportUpperSeparationLayers>')
    fff.append('  <supportLowerSeparationLayers>1</supportLowerSeparationLayers>')

    fff.append('  <supportType>0</supportType>')
    fff.append('  <supportGridSpacing>1</supportGridSpacing>')
    fff.append('  <maxOverhangAngle>60</maxOverhangAngle>')
    fff.append('  <supportAngles>90</supportAngles>')
    if hotendLeft['id'] != 'None':
        fff.append('  <temperatureController name="Left Extruder '+str(hotendLeft['nozzleSize'])+'">')
        fff.append('    <temperatureNumber>0</temperatureNumber>')
        fff.append('    <isHeatedBed>0</isHeatedBed>')
        fff.append('    <relayBetweenLayers>0</relayBetweenLayers>')
        fff.append('    <relayBetweenLoops>0</relayBetweenLoops>')
        fff.append('    <stabilizeAtStartup>0</stabilizeAtStartup>')
        fff.append('    <setpoint layer="1" temperature="150"/>')
        fff.append('  </temperatureController>')
    if hotendRight['id'] != 'None':
        fff.append('  <temperatureController name="Right Extruder '+str(hotendRight['nozzleSize'])+'">')
        fff.append('    <temperatureNumber>1</temperatureNumber>')
        fff.append('    <isHeatedBed>0</isHeatedBed>')
        fff.append('    <relayBetweenLayers>0</relayBetweenLayers>')
        fff.append('    <relayBetweenLoops>0</relayBetweenLoops>')
        fff.append('    <stabilizeAtStartup>0</stabilizeAtStartup>')
        fff.append('    <setpoint layer="1" temperature="150"/>')
        fff.append('  </temperatureController>')
    if (hotendLeft['id'] != 'None' and filamentLeft['bedTemperature'] > 0) or (hotendRight['id'] != 'None' and filamentRight['bedTemperature'] > 0):
        fff.append('  <temperatureController name="Heated Bed">')
        fff.append('    <temperatureNumber>0</temperatureNumber>')
        fff.append('    <isHeatedBed>1</isHeatedBed>')
        fff.append('    <relayBetweenLayers>0</relayBetweenLayers>')
        fff.append('    <relayBetweenLoops>0</relayBetweenLoops>')
        fff.append('    <stabilizeAtStartup>0</stabilizeAtStartup>')
        fff.append('    <setpoint layer="1" temperature="50"/>')
        fff.append('  </temperatureController>')
    fff.append('  <fanSpeed>')
    fff.append('    <setpoint layer="1" speed="0" />')
    fff.append('    <setpoint layer="2" speed="100"/>')
    fff.append('  </fanSpeed>')
    fff.append('  <blipFanToFullPower>0</blipFanToFullPower>')
    fff.append('  <adjustSpeedForCooling>1</adjustSpeedForCooling>')
    fff.append('  <minSpeedLayerTime>5</minSpeedLayerTime>')
    fff.append('  <minCoolingSpeedSlowdown>75</minCoolingSpeedSlowdown>')
    fff.append('  <increaseFanForCooling>1</increaseFanForCooling>')
    fff.append('  <minFanLayerTime>5</minFanLayerTime>')
    fff.append('  <maxCoolingFanSpeed>100</maxCoolingFanSpeed>')
    fff.append('  <increaseFanForBridging>1</increaseFanForBridging>')
    fff.append('  <bridgingFanSpeed>100</bridgingFanSpeed>')
    fff.append('  <use5D>1</use5D>')
    fff.append('  <relativeEdistances>0</relativeEdistances>')
    fff.append('  <allowEaxisZeroing>1</allowEaxisZeroing>')
    fff.append('  <independentExtruderAxes>0</independentExtruderAxes>')
    fff.append('  <includeM10123>0</includeM10123>')
    fff.append('  <stickySupport>1</stickySupport>')
    fff.append('  <applyToolheadOffsets>0</applyToolheadOffsets>')
    fff.append('  <gcodeXoffset>0</gcodeXoffset>')
    fff.append('  <gcodeYoffset>0</gcodeYoffset>')
    fff.append('  <gcodeZoffset>0</gcodeZoffset>')
    fff.append('  <overrideMachineDefinition>1</overrideMachineDefinition>')
    fff.append('  <machineTypeOverride>0</machineTypeOverride>')
    if printMode == 'regular':
        fff.append('  <strokeXoverride>'+str(machine['width'])+'</strokeXoverride>')
    elif printMode == 'mirror':
        fff.append('  <strokeXoverride>'+str(int(machine['width']/2. - (abs(machine['extruderHead'][0][0]) + abs(machine['extruderHead'][2][0]))/2.))+'</strokeXoverride>')
    elif printMode == 'duplication':
        fff.append('  <strokeXoverride>'+str(int(machine['width']/2.))+'</strokeXoverride>')
    fff.append('  <strokeYoverride>'+str(machine['depth'])+'</strokeYoverride>')
    fff.append('  <strokeZoverride>'+str(machine['height'])+'</strokeZoverride>')
    fff.append('  <originOffsetXoverride>0</originOffsetXoverride>')
    fff.append('  <originOffsetYoverride>0</originOffsetYoverride>')
    fff.append('  <originOffsetZoverride>0</originOffsetZoverride>')
    fff.append('  <homeXdirOverride>-1</homeXdirOverride>')
    fff.append('  <homeYdirOverride>-1</homeYdirOverride>')
    fff.append('  <homeZdirOverride>-1</homeZdirOverride>')
    fff.append('  <flipXoverride>1</flipXoverride>')
    fff.append('  <flipYoverride>-1</flipYoverride>')
    fff.append('  <flipZoverride>1</flipZoverride>')
    fff.append('  <toolheadOffsets>0,0|0,0|0,0|0,0|0,0|0,0</toolheadOffsets>')
    fff.append('  <overrideFirmwareConfiguration>1</overrideFirmwareConfiguration>')
    fff.append('  <firmwareTypeOverride>RepRap (Marlin/Repetier/Sprinter)</firmwareTypeOverride>')
    fff.append('  <GPXconfigOverride>r2</GPXconfigOverride>')
    fff.append('  <baudRateOverride>250000</baudRateOverride>')
    fff.append('  <overridePrinterModels>0</overridePrinterModels>')
    fff.append('  <printerModelsOverride></printerModelsOverride>')
    fff.append('  <startingGcode></startingGcode>')
    fff.append('  <layerChangeGcode></layerChangeGcode>')
    fff.append('  <retractionGcode></retractionGcode>')
    fff.append('  <toolChangeGcode></toolChangeGcode>')
    fff.append('  <endingGcode>M104 S0 T0\t\t\t;left extruder heater off,M104 S0 T1\t\t\t;right extruder heater off,M140 S0\t\t\t;heated bed heater off,G91\t\t\t;relative positioning,G1 Z+0.5 E-5 Y+10 F[travel_speed]\t;move Z up a bit and retract filament,G28 X0 Y0\t\t\t;move X/Y to min endstops so the head is out of the way,M84\t\t\t;steppers off,G90\t\t\t;absolute positioning,</endingGcode>')
    fff.append('  <exportFileFormat>gcode</exportFileFormat>')
    fff.append('  <celebration>0</celebration>')
    fff.append('  <celebrationSong>Random Song</celebrationSong>')
    fff.append('  <postProcessing></postProcessing>')
    fff.append('  <defaultSpeed>2400</defaultSpeed>')
    fff.append('  <outlineUnderspeed>0.85</outlineUnderspeed>')
    fff.append('  <solidInfillUnderspeed>0.85</solidInfillUnderspeed>')
    fff.append('  <supportUnderspeed>0.9</supportUnderspeed>')
    fff.append('  <rapidXYspeed>12000</rapidXYspeed>')
    fff.append('  <rapidZspeed>1002</rapidZspeed>') # If this value changes, Simplify3D bug correction post script should be adapted
    fff.append('  <minBridgingArea>10</minBridgingArea>')
    fff.append('  <bridgingExtraInflation>0</bridgingExtraInflation>')
    fff.append('  <bridgingExtrusionMultiplier>1</bridgingExtrusionMultiplier>')
    fff.append('  <bridgingSpeedMultiplier>1.5</bridgingSpeedMultiplier>')
    fff.append('  <useFixedBridgingAngle>0</useFixedBridgingAngle>')
    fff.append('  <fixedBridgingAngle>0</fixedBridgingAngle>')
    fff.append('  <applyBridgingToPerimeters>1</applyBridgingToPerimeters>')
    fff.append('  <filamentDiameters>2.85|2.85|2.85|2.85|2.85|2.85</filamentDiameters>')
    fff.append('  <filamentPricesPerKg>19.95|19.95|19.95|19.95|19.95|19.95</filamentPricesPerKg>')
    fff.append('  <filamentDensities>1.25|1.25|1.25|1.25|1.25|1.25</filamentDensities>')
    fff.append('  <useMinPrintHeight>0</useMinPrintHeight>')
    fff.append('  <minPrintHeight>0</minPrintHeight>')
    fff.append('  <useMaxPrintHeight>0</useMaxPrintHeight>')
    fff.append('  <maxPrintHeight>0</maxPrintHeight>')
    fff.append('  <useDiaphragm>0</useDiaphragm>')
    fff.append('  <diaphragmLayerInterval>5</diaphragmLayerInterval>')
    fff.append('  <robustSlicing>1</robustSlicing>')
    fff.append('  <mergeAllIntoSolid>0</mergeAllIntoSolid>')
    fff.append('  <onlyRetractWhenCrossingOutline>0</onlyRetractWhenCrossingOutline>')
    fff.append('  <retractBetweenLayers>1</retractBetweenLayers>')
    fff.append('  <useRetractionMinTravel>1</useRetractionMinTravel>')
    fff.append('  <retractionMinTravel>1.5</retractionMinTravel>')
    fff.append('  <retractWhileWiping>1</retractWhileWiping>')
    fff.append('  <onlyWipeOutlines>1</onlyWipeOutlines>')
    fff.append('  <avoidCrossingOutline>1</avoidCrossingOutline>')
    fff.append('  <maxMovementDetourFactor>3</maxMovementDetourFactor>')
    fff.append('  <toolChangeRetractionDistance>8</toolChangeRetractionDistance>')
    fff.append('  <toolChangeExtraRestartDistance>0</toolChangeExtraRestartDistance>')
    fff.append('  <toolChangeRetractionSpeed>2400</toolChangeRetractionSpeed>')
    fff.append('  <externalThinWallType>0</externalThinWallType>')
    fff.append('  <internalThinWallType>2</internalThinWallType>')
    fff.append('  <thinWallAllowedOverlapPercentage>10</thinWallAllowedOverlapPercentage>')
    fff.append('  <singleExtrusionMinLength>1</singleExtrusionMinLength>')
    fff.append('  <singleExtrusionMinPrintingWidthPercentage>50</singleExtrusionMinPrintingWidthPercentage>')
    fff.append('  <singleExtrusionMaxPrintingWidthPercentage>200</singleExtrusionMaxPrintingWidthPercentage>')
    fff.append('  <singleExtrusionEndpointExtension>0.2</singleExtrusionEndpointExtension>')
    fff.append('  <horizontalSizeCompensation>0</horizontalSizeCompensation>')
    # fff.append('  <overridePrinterModels>1</overridePrinterModels>')
    # fff.append('  <printerModelsOverride>BCN3DSigma.stl</printerModelsOverride>')
    # fff.append('  <autoConfigureMaterial name="'+str(filamentLeft)+" Left, "+str(filamentRight)+" Right"+'">')
    for extruder in extruderPrintOptions:
        for quality in sorted(PS.profilesData['quality'], key=lambda k: k['index']):
            infillPercentage = quality['infillPercentage']
            infillLayerInterval = 1
            overlapInternalInfillAngles = 1
            generateSupport = 0
            supportHorizontalPartOffset = 0.7
            supportUpperSeparationLayers = 1
            supportLowerSeparationLayers = 1
            supportAngles = '90'
            supportInfillPercentage = 25
            denseSupportInfillPercentage = 75
            avoidCrossingOutline = 1
            fanActionOnToolChange1 = ''
            fanActionOnToolChange2 = ''
            if extruder in ['Left Extruder', 'Right Extruder']:
                # MEX
                if extruder == 'Left Extruder':
                    # MEX Left
                    primaryExtruder = 0
                    primaryFilament = filamentLeft
                    primaryHotend = hotendLeft
                    layerHeight = getLayerHeight(primaryHotend, quality)
                    firstLayerHeight = primaryHotend['nozzleSize'] / 2.
                    defaultSpeed, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, layerHeight, firstLayerHeight, infillLayerInterval, quality, 'MEX Left')
                    hotendLeftTemperature = temperatureAdjustedToFlow(filamentLeft, hotendLeft, layerHeight, defaultSpeed)
                    purgeValuesT0 = purgeValues(hotendLeft, filamentLeft, defaultSpeed, layerHeight)
                    if 'Both Extruders' in extruderPrintOptions:
                        layerHeightTemp = getLayerHeight(hotendRight, quality)
                        defaultSpeedTemp, firstLayerUnderspeedTemp, outlineUnderspeedTemp, supportUnderspeedTemp = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, layerHeightTemp, firstLayerHeight, infillLayerInterval, quality, 'MEX Right')
                        hotendRightTemperature = temperatureAdjustedToFlow(filamentRight, hotendRight, layerHeightTemp, defaultSpeedTemp)
                        purgeValuesT1 = purgeValues(hotendRight, filamentRight, defaultSpeedTemp, layerHeightTemp)
                    else:
                        hotendRightTemperature = hotendLeftTemperature
                        purgeValuesT1 = purgeValuesT0
                else:
                    # MEX Right
                    primaryExtruder = 1
                    primaryFilament = filamentRight
                    primaryHotend = hotendRight
                    layerHeight = getLayerHeight(primaryHotend, quality)
                    firstLayerHeight = primaryHotend['nozzleSize'] / 2.
                    defaultSpeed, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, layerHeight, firstLayerHeight, infillLayerInterval, quality, 'MEX Right')
                    hotendRightTemperature = temperatureAdjustedToFlow(filamentRight, hotendRight, layerHeight, defaultSpeed)
                    purgeValuesT1 = purgeValues(hotendRight, filamentRight, defaultSpeed, layerHeight)
                    if 'Both Extruders' in extruderPrintOptions:
                        layerHeightTemp = getLayerHeight(hotendLeft, quality)
                        defaultSpeedTemp, firstLayerUnderspeedTemp, outlineUnderspeedTemp, supportUnderspeedTemp = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, layerHeightTemp, firstLayerHeight, infillLayerInterval, quality, 'MEX Left')
                        hotendLeftTemperature = temperatureAdjustedToFlow(filamentLeft, hotendLeft, layerHeightTemp, defaultSpeedTemp)
                        purgeValuesT0 = purgeValues(hotendLeft, filamentLeft, defaultSpeedTemp, layerHeightTemp)
                    else:
                        hotendLeftTemperature = hotendRightTemperature
                        purgeValuesT0 = purgeValuesT1
                infillExtruder = primaryExtruder
                supportExtruder = primaryExtruder
                bedTemperature = primaryFilament['bedTemperature']
                secondaryExtruderAction = ' - '
            else:
                # IDEX                
                if filamentLeft['isSupportMaterial'] != filamentRight['isSupportMaterial']:
                    # IDEX, Support Material
                    generateSupport = 1
                    supportHorizontalPartOffset = 0.1
                    supportUpperSeparationLayers = 0
                    supportLowerSeparationLayers = 0
                    supportAngles = '90,0'
                    supportInfillPercentage = 25
                    denseSupportInfillPercentage = 100
                    if filamentLeft['isSupportMaterial']:
                        # IDEX, Support Material in Left Hotend
                        primaryExtruder = 1
                        primaryFilament = filamentRight
                        primaryHotend = hotendRight
                        layerHeight = min(getLayerHeight(hotendRight, quality), hotendLeft['nozzleSize']*0.5)
                        firstLayerHeight = min(hotendLeft['nozzleSize'], hotendRight['nozzleSize']) / 2.
                        secondaryExtruderAction = ' (Left Ext. for supports) - '
                        defaultSpeed, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, layerHeight, firstLayerHeight, infillLayerInterval, quality, 'IDEX, Supports with Left')
                        purgeValuesT0 = purgeValues(hotendLeft, filamentLeft, defaultSpeed * supportUnderspeed, layerHeight)
                        purgeValuesT1 = purgeValuesT0
                        hotendLeftTemperature = temperatureAdjustedToFlow(filamentLeft, hotendLeft, layerHeight, defaultSpeed*supportUnderspeed)
                        hotendRightTemperature = temperatureAdjustedToFlow(filamentRight, hotendRight, layerHeight, defaultSpeed)
                        fanActionOnToolChange1 = '{IF NEWTOOL=0} M107'+"\t\t"+';disable fan for support material,'
                        fanActionOnToolChange2 = '{IF NEWTOOL=1} M106 S'+str(fanSpeed(primaryHotend, primaryFilament, hotendRightTemperature, layerHeight))+"\t\t"+';enable fan for part material,'
                    else:
                        # IDEX, Support Material in Right Hotend
                        primaryExtruder = 0
                        primaryFilament = filamentLeft
                        primaryHotend = hotendLeft
                        layerHeight = min(getLayerHeight(hotendLeft, quality), hotendRight['nozzleSize']*0.5)
                        firstLayerHeight = min(hotendLeft['nozzleSize'], hotendRight['nozzleSize']) / 2.
                        secondaryExtruderAction = ' (Right Ext. for supports) - '
                        defaultSpeed, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, layerHeight, firstLayerHeight, infillLayerInterval, quality, 'IDEX, Supports with Right')
                        purgeValuesT0 = purgeValues(hotendLeft, filamentLeft, defaultSpeed, layerHeight)
                        purgeValuesT1 = purgeValues(hotendRight, filamentRight, defaultSpeed * supportUnderspeed, layerHeight)
                        hotendLeftTemperature = temperatureAdjustedToFlow(filamentLeft, hotendLeft, layerHeight, defaultSpeed)
                        hotendRightTemperature = temperatureAdjustedToFlow(filamentRight, hotendRight, layerHeight, defaultSpeed*supportUnderspeed)
                        fanActionOnToolChange1 = '{IF NEWTOOL=0} M106 S'+str(fanSpeed(primaryHotend, primaryFilament, hotendLeftTemperature, layerHeight))+"\t\t"+';enable fan for part material,'
                        fanActionOnToolChange2 = '{IF NEWTOOL=1} M107'+"\t\t"+';disable fan for support material,' 
                    infillExtruder = primaryExtruder
                    supportExtruder = abs(primaryExtruder-1)                    
                else:
                    # IDEX, Combined Infill
                    avoidCrossingOutline = 0
                    if hotendLeft['nozzleSize'] <= hotendRight['nozzleSize']:
                        # IDEX, Combined Infill (Right Hotend has thicker or equal nozzle)
                        primaryExtruder = 0
                        primaryFilament = filamentLeft
                        primaryHotend = hotendLeft
                        layerHeight = min(getLayerHeight(primaryHotend, quality), hotendRight['nozzleSize']*0.5)
                        firstLayerHeight = primaryHotend['nozzleSize'] / 2.
                        infillLayerInterval = int(str((hotendRight['nozzleSize']*0.5)/layerHeight).split('.')[0])
                        defaultSpeed, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, layerHeight, firstLayerHeight, infillLayerInterval, quality, 'IDEX, Infill with Right')
                        hotendLeftTemperature = temperatureAdjustedToFlow(filamentLeft, hotendLeft, layerHeight, max(defaultSpeed,defaultSpeed*outlineUnderspeed))
                        hotendRightTemperature = temperatureAdjustedToFlow(filamentRight, hotendRight, layerHeight*infillLayerInterval, defaultSpeed)
                        secondaryExtruderAction = ' (Right Ext. for infill) - '
                        if primaryFilament['fanPercentage'][1] != 0:
                            fanActionOnToolChange1 = '' # '{IF NEWTOOL=0} M106 S'+str(fanSpeed(primaryHotend, primaryFilament, hotendLeftTemperature, layerHeight))+"\t\t"+';enable fan for perimeters,'
                            fanActionOnToolChange2 = '' # '{IF NEWTOOL=1} M107'+"\t\t"+';disable fan for infill,'
                        purgeValuesT0 = purgeValues(hotendLeft, filamentLeft, defaultSpeed, layerHeight)
                        purgeValuesT1 = purgeValues(hotendRight, filamentRight, defaultSpeed, layerHeight * infillLayerInterval)
                    else:
                        # IDEX, Combined Infill (Left Hotend has thicker nozzle)
                        primaryExtruder = 1
                        primaryFilament = filamentRight
                        primaryHotend = hotendRight
                        layerHeight = min(getLayerHeight(primaryHotend, quality), hotendLeft['nozzleSize']*0.5)
                        firstLayerHeight = primaryHotend['nozzleSize'] / 2.
                        infillLayerInterval = int(str((hotendLeft['nozzleSize']*0.5)/layerHeight).split('.')[0])
                        defaultSpeed, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, layerHeight, firstLayerHeight, infillLayerInterval, quality, 'IDEX, Infill with Left')
                        hotendLeftTemperature = temperatureAdjustedToFlow(filamentLeft, hotendLeft, layerHeight*infillLayerInterval, defaultSpeed)
                        hotendRightTemperature = temperatureAdjustedToFlow(filamentRight, hotendRight, layerHeight, max(defaultSpeed,defaultSpeed*outlineUnderspeed))
                        secondaryExtruderAction = ' (Left Ext. for infill) - '
                        if primaryFilament['fanPercentage'][1] != 0:
                            fanActionOnToolChange1 = '' # '{IF NEWTOOL=0} M107'+"\t\t"+';disable fan for infill,'
                            fanActionOnToolChange2 = '' # '{IF NEWTOOL=1} M106 S'+str(fanSpeed(primaryHotend, primaryFilament, hotendRightTemperature, layerHeight))+"\t\t"+';enable fan for perimeters,'
                        purgeValuesT0 = purgeValues(hotendLeft, filamentLeft, defaultSpeed, layerHeight * infillLayerInterval)
                        purgeValuesT1 = purgeValues(hotendRight, filamentRight, defaultSpeed, layerHeight)
                    infillExtruder = abs(primaryExtruder-1)
                    supportExtruder = primaryExtruder
                    firstLayerHeight = primaryHotend['nozzleSize'] / 2.
                bedTemperature = max(filamentLeft['bedTemperature'], filamentRight['bedTemperature'])
                        
            firstLayerHeightPercentage = int(firstLayerHeight * 100 / float(layerHeight))
            perimeterOutlines = max(3, int(round(quality['wallWidth'] / primaryHotend['nozzleSize']))) # 3 minimum Perimeters needed
            topSolidLayers = max(5, int(round(quality['topBottomWidth'] / layerHeight)))        # 5 minimum layers needed
            bottomSolidLayers = topSolidLayers
            raftExtruder = primaryExtruder
            skirtExtruder = primaryExtruder
            useCoasting, useWipe, onlyRetractWhenCrossingOutline, retractBetweenLayers, useRetractionMinTravel, retractWhileWiping, onlyWipeOutlines = retractValues(primaryFilament)
            startPurgeLengthT0, toolChangePurgeLengthT0, purgeSpeedT0, sParameterT0, eParameterT0, pParameterT0 = purgeValuesT0
            startPurgeLengthT1, toolChangePurgeLengthT1, purgeSpeedT1, sParameterT1, eParameterT1, pParameterT1 = purgeValuesT1
            fff.append('  <autoConfigureQuality name="'+extruder+secondaryExtruderAction+str(quality['id'])+'">')
            fff.append('    <globalExtrusionMultiplier>1</globalExtrusionMultiplier>')
            fff.append('    <fanSpeed>')
            fff.append('      <setpoint layer="1" speed="0" />')
            if primaryExtruder == 0:
                fff.append('      <setpoint layer="2" speed="'+str(fanSpeed(primaryHotend, primaryFilament, hotendLeftTemperature, layerHeight))+'" />')
            else:
                fff.append('      <setpoint layer="2" speed="'+str(fanSpeed(primaryHotend, primaryFilament, hotendRightTemperature, layerHeight))+'" />')
            fff.append('    </fanSpeed>')
            fff.append('    <filamentDiameter>'+str(primaryFilament['filamentDiameter'])+'</filamentDiameter>')
            fff.append('    <filamentPricePerKg>'+str(primaryFilament['filamentPricePerKg'])+'</filamentPricePerKg>')
            fff.append('    <filamentDensity>'+str(primaryFilament['filamentDensity'])+'</filamentDensity>')
            if hotendLeft['id'] != 'None':
                fff.append('    <extruder name="Left Extruder '+str(hotendLeft['nozzleSize'])+'">')
                fff.append('      <toolheadNumber>0</toolheadNumber>')
                fff.append('      <diameter>'+str(hotendLeft['nozzleSize'])+'</diameter>')
                fff.append('      <autoWidth>0</autoWidth>')
                fff.append('      <width>'+str(hotendLeft['nozzleSize'] * 0.875)+'</width>')
                fff.append('      <extrusionMultiplier>'+str(filamentLeft['extrusionMultiplier'])+'</extrusionMultiplier>')
                fff.append('      <useRetract>1</useRetract>')
                fff.append('      <retractionDistance>'+str(filamentLeft['retractionDistance'])+'</retractionDistance>')
                fff.append('      <extraRestartDistance>0</extraRestartDistance>')
                fff.append('      <retractionZLift>'+("%.2f" % (layerHeight/2.))+'</retractionZLift>')
                fff.append('      <retractionSpeed>'+str(filamentLeft['retractionSpeed']*60)+'</retractionSpeed>')
                fff.append('      <useCoasting>'+str(retractValues(filamentLeft)[0])+'</useCoasting>')
                fff.append('      <coastingDistance>'+str(coastVolume(hotendLeft, filamentLeft) / (layerHeight * hotendLeft['nozzleSize']))+'</coastingDistance>')
                fff.append('      <useWipe>'+str(retractValues(filamentLeft)[1])+'</useWipe>')
                fff.append('      <wipeDistance>'+str(hotendLeft['nozzleSize']*12.5)+'</wipeDistance>')
                fff.append('    </extruder>')
            if hotendRight['id'] != 'None':
                fff.append('    <extruder name="Right Extruder '+str(hotendRight['nozzleSize'])+'">')
                fff.append('      <toolheadNumber>1</toolheadNumber>')
                fff.append('      <diameter>'+str(hotendRight['nozzleSize'])+'</diameter>')
                fff.append('      <autoWidth>0</autoWidth>')
                fff.append('      <width>'+str(hotendRight['nozzleSize'] * 0.875)+'</width>')
                fff.append('      <extrusionMultiplier>'+str(filamentRight['extrusionMultiplier'])+'</extrusionMultiplier>')
                fff.append('      <useRetract>1</useRetract>')
                fff.append('      <retractionDistance>'+str(filamentRight['retractionDistance'])+'</retractionDistance>')
                fff.append('      <extraRestartDistance>0</extraRestartDistance>')
                fff.append('      <retractionZLift>'+str(layerHeight/2)+'</retractionZLift>')
                fff.append('      <retractionSpeed>'+str(filamentRight['retractionSpeed']*60)+'</retractionSpeed>')
                fff.append('      <useCoasting>'+str(retractValues(filamentRight)[0])+'</useCoasting>')
                fff.append('      <coastingDistance>'+str(coastVolume(hotendRight, filamentRight) / (layerHeight * hotendRight['nozzleSize']))+'</coastingDistance>')
                fff.append('      <useWipe>'+str(retractValues(filamentRight)[1])+'</useWipe>')
                fff.append('      <wipeDistance>'+str(hotendRight['nozzleSize']*12.5)+'</wipeDistance>')
                fff.append('    </extruder>')
            fff.append('    <primaryExtruder>'+str(primaryExtruder)+'</primaryExtruder>')
            fff.append('    <raftExtruder>'+str(raftExtruder)+'</raftExtruder>')
            fff.append('    <raftSeparationDistance>'+str(primaryHotend['nozzleSize'] * 0.55)+'</raftSeparationDistance>')
            fff.append('    <skirtExtruder>'+str(skirtExtruder)+'</skirtExtruder>')
            fff.append('    <infillExtruder>'+str(infillExtruder)+'</infillExtruder>')
            fff.append('    <supportExtruder>'+str(supportExtruder)+'</supportExtruder>')
            fff.append('    <generateSupport>'+str(generateSupport)+'</generateSupport>')
            fff.append('    <layerHeight>'+str(layerHeight)+'</layerHeight>')
            fff.append('    <firstLayerHeightPercentage>'+str(firstLayerHeightPercentage)+'</firstLayerHeightPercentage>')
            fff.append('    <topSolidLayers>'+str(topSolidLayers)+'</topSolidLayers>')
            fff.append('    <bottomSolidLayers>'+str(bottomSolidLayers)+'</bottomSolidLayers>')
            fff.append('    <perimeterOutlines>'+str(perimeterOutlines)+'</perimeterOutlines>')
            fff.append('    <infillPercentage>'+str(infillPercentage)+'</infillPercentage>')
            fff.append('    <infillLayerInterval>'+str(infillLayerInterval)+'</infillLayerInterval>')
            fff.append('    <defaultSpeed>'+str(defaultSpeed)+'</defaultSpeed>')
            fff.append('    <firstLayerUnderspeed>'+str(firstLayerUnderspeed)+'</firstLayerUnderspeed>')
            fff.append('    <outlineUnderspeed>'+str(outlineUnderspeed)+'</outlineUnderspeed>')
            fff.append('    <supportUnderspeed>'+str(supportUnderspeed)+'</supportUnderspeed>')
            fff.append('    <supportInfillPercentage>'+str(supportInfillPercentage)+'</supportInfillPercentage>')
            fff.append('    <denseSupportInfillPercentage>'+str(denseSupportInfillPercentage)+'</denseSupportInfillPercentage>')
            fff.append('    <avoidCrossingOutline>'+str(avoidCrossingOutline)+'</avoidCrossingOutline>')
            fff.append('    <overlapInternalInfillAngles>'+str(overlapInternalInfillAngles)+'</overlapInternalInfillAngles>')
            fff.append('    <supportHorizontalPartOffset>'+str(supportHorizontalPartOffset)+'</supportHorizontalPartOffset>')
            fff.append('    <supportUpperSeparationLayers>'+str(supportUpperSeparationLayers)+'</supportUpperSeparationLayers>')
            fff.append('    <supportLowerSeparationLayers>'+str(supportLowerSeparationLayers)+'</supportLowerSeparationLayers>')
            fff.append('    <supportAngles>'+str(supportAngles)+'</supportAngles>')
            fff.append('    <onlyRetractWhenCrossingOutline>'+str(onlyRetractWhenCrossingOutline)+'</onlyRetractWhenCrossingOutline>')
            fff.append('    <retractBetweenLayers>'+str(retractBetweenLayers)+'</retractBetweenLayers>')
            fff.append('    <useRetractionMinTravel>'+str(useRetractionMinTravel)+'</useRetractionMinTravel>')
            fff.append('    <retractWhileWiping>'+str(retractWhileWiping)+'</retractWhileWiping>')
            fff.append('    <onlyWipeOutlines>'+str(onlyWipeOutlines)+'</onlyWipeOutlines>')
            fff.append('    <minBridgingArea>10</minBridgingArea>')
            fff.append('    <bridgingExtraInflation>0</bridgingExtraInflation>')
            if generateSupport == 0:
                bridgingSpeedMultiplier = 1.5
            else:
                bridgingSpeedMultiplier = 1
            fff.append('    <bridgingExtrusionMultiplier>'+str(round(primaryFilament['extrusionMultiplier']*(1/bridgingSpeedMultiplier), 2))+'</bridgingExtrusionMultiplier>')
            fff.append('    <bridgingSpeedMultiplier>'+str(bridgingSpeedMultiplier)+'</bridgingSpeedMultiplier>')
            if hotendLeft['id'] != 'None':
                fff.append('    <temperatureController name="Left Extruder '+str(hotendLeft['nozzleSize'])+'">')
                fff.append('      <temperatureNumber>0</temperatureNumber>')
                fff.append('      <isHeatedBed>0</isHeatedBed>')
                fff.append('      <relayBetweenLayers>0</relayBetweenLayers>')
                fff.append('      <relayBetweenLoops>0</relayBetweenLoops>')
                fff.append('      <stabilizeAtStartup>0</stabilizeAtStartup>')
                fff.append('      <setpoint layer="1" temperature="'+str(getTemperature(hotendLeft, filamentLeft, "highTemperature"))+'"/>')
                fff.append('      <setpoint layer="2" temperature="'+str(hotendLeftTemperature)+'"/>')
                fff.append('    </temperatureController>')
            if hotendRight['id'] != 'None':
                fff.append('    <temperatureController name="Right Extruder '+str(hotendRight['nozzleSize'])+'">')
                fff.append('      <temperatureNumber>1</temperatureNumber>')
                fff.append('      <isHeatedBed>0</isHeatedBed>')
                fff.append('      <relayBetweenLayers>0</relayBetweenLayers>')
                fff.append('      <relayBetweenLoops>0</relayBetweenLoops>')
                fff.append('      <stabilizeAtStartup>0</stabilizeAtStartup>')
                fff.append('      <setpoint layer="1" temperature="'+str(getTemperature(hotendRight, filamentRight, "highTemperature"))+'"/>')
                fff.append('      <setpoint layer="2" temperature="'+str(hotendRightTemperature)+'"/>')
                fff.append('    </temperatureController>')
            if (hotendLeft['id'] != 'None' and filamentLeft['bedTemperature'] > 0) or (hotendRight['id'] != 'None' and filamentRight['bedTemperature'] > 0):
                fff.append('    <temperatureController name="Heated Bed">')
                fff.append('      <temperatureNumber>0</temperatureNumber>')
                fff.append('      <isHeatedBed>1</isHeatedBed>')
                fff.append('      <relayBetweenLayers>0</relayBetweenLayers>')
                fff.append('      <relayBetweenLoops>0</relayBetweenLoops>')
                fff.append('      <stabilizeAtStartup>0</stabilizeAtStartup>')
                fff.append('      <setpoint layer="1" temperature="'+str(bedTemperature)+'"/>')
                fff.append('    </temperatureController>')
            if hotendLeft['id'] != 'None' and hotendRight['id'] != 'None':                    
                fff.append('    <toolChangeGcode>{IF NEWTOOL=0} T0\t\t\t;Start tool switch 0,{IF NEWTOOL=0} G1 F2400 E0,{IF NEWTOOL=0} M800 F'+str(purgeSpeedT0)+' S'+str(sParameterT0)+' E'+str(eParameterT0)+' P'+str(pParameterT0)+'\t\t;SmartPurge - Needs Firmware v01-1.2.3,;{IF NEWTOOL=0} G1 F'+str(purgeSpeedT0)+' E'+str(toolChangePurgeLengthT0)+'\t\t;Default purge value,'+fanActionOnToolChange1+',{IF NEWTOOL=1} T1\t\t\t;Start tool switch 1,{IF NEWTOOL=1} G1 F2400 E0,{IF NEWTOOL=1} M800 F'+str(purgeSpeedT1)+' S'+str(sParameterT1)+' E'+str(eParameterT1)+' P'+str(pParameterT1)+'\t\t;SmartPurge - Needs Firmware v01-1.2.3,;{IF NEWTOOL=1} G1 F'+str(purgeSpeedT1)+' E'+str(toolChangePurgeLengthT1)+'\t\t;Default purge,'+fanActionOnToolChange2+",G4 P2000\t\t\t\t;Stabilize Hotend's pressure,G92 E0\t\t\t\t;Zero extruder,G1 F3000 E-4.5\t\t\t\t;Retract,G1 F[travel_speed]\t\t\t;End tool switch,G91,G1 F[travel_speed] Z2,G90</toolChangeGcode>")
            else:
                fff.append('    <toolChangeGcode/>')
            if primaryFilament['isFlexibleMaterial']:
                reducedAccelerationForPerimeters = 2000
            else:
                reducedAccelerationForPerimeters = accelerationForPerimeters(primaryHotend['nozzleSize'], layerHeight, int(defaultSpeed/60. * outlineUnderspeed))
            postProcessingScript = r'{REPLACE "; outer perimeter" "; outer perimeter\nM204 S'+str(reducedAccelerationForPerimeters)+r'"},{REPLACE "; inner perimeter" "; inner perimeter\nM204 S2000"},{REPLACE "; solid layer" "; solid layer\nM204 S2000"},{REPLACE "; infill" "; infill\nM204 S2000",{REPLACE "; support" "; support\nM204 S2000"},{REPLACE "; layer end" "; layer end\nM204 S2000"},{REPLACE "F12000\nG1 Z'+str(round(layerHeight*firstLayerHeightPercentage/100., 3))+r' F1002\nG92 E0" "F12000G1 Z'+str(round(layerHeight*firstLayerHeightPercentage/100., 3))+r' F1002\nG1 E0.0000 F720\nG92 E0"}'
            fff.append('  </autoConfigureQuality>')

            # if dataLog != '--no-data' :
            #     # Store flows, speeds, temperatures and other data
            #     data = extruder, defaultSpeed, infillLayerInterval, layerHeight, hotendLeft, hotendRight, primaryExtruder, infillExtruder, supportExtruder, filamentLeft, filamentRight, quality, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed, firstLayerHeightPercentage, hotendLeftTemperature, hotendRightTemperature, bedTemperature
            #     Logger.writeData(data)

    # fff.append('  </autoConfigureMaterial>')

    # Start gcode must be defined in autoConfigureExtruders. Otherwise you have problems with the first heat sequence in Dual Color prints.
    if hotendLeft['id'] != 'None':
        if printMode == 'regular':
            fff.append('  <autoConfigureExtruders name="Left Extruder Only"  allowedToolheads="1">')
            fff.append('    <startingGcode>;Sigma ProGen '+PS.progenVersionNumber+' (Build '+PS.progenBuildNumber+'),T0,'+firstHeatSequence(hotendLeft, hotendRight, hotendLeftTemperature, 0, bedTemperature, 'Simplify3D')+',G21\t\t;metric values,G90\t\t;absolute positioning,M82\t\t;set extruder to absolute mode,M107\t\t;start with the fan off,G28 X0 Y0\t\t;move X/Y to min endstops,G28 Z0\t\t;move Z to min endstops,G92 E0\t\t;zero the extruded length,G1 Z5 F200\t\t;safety Z axis movement,G1 F'+str(purgeSpeedT0)+' E'+str(startPurgeLengthT0)+'\t;extrude '+str(startPurgeLengthT0)+'mm of feed stock,G92 E0\t\t;zero the extruded length again</startingGcode>')
        else:
            fff.append('  <autoConfigureExtruders name="Extruders in '+printMode+' mode"  allowedToolheads="1">')
            if printMode == 'mirror':
                printModeGcode = ',M605 S6\t\t;enable mirror mode'
            else:
                printModeGcode = ',M605 S5\t\t;enable duplication mode'
            fff.append('    <startingGcode>;Sigma ProGen '+PS.progenVersionNumber+' (Build '+PS.progenBuildNumber+'),,'+firstHeatSequence(hotendLeft, hotendLeft, hotendLeftTemperature, hotendLeftTemperature, bedTemperature, 'Simplify3D')+',G21\t\t;metric values,G90\t\t;absolute positioning,M108 P1\t\t;enable layer fan for idle extruder,M107\t\t;start with the fan off,G28 X0 Y0\t\t;move X/Y to min endstops,G28 Z0\t\t;move Z to min endstops,T1\t\t;switch to the right extruder,G92 E0\t\t;zero the extruded length,G1 F'+str(purgeSpeedT0)+' E'+str(startPurgeLengthT0)+'\t;extrude '+str(startPurgeLengthT0)+'mm of feed stock,G92 E0\t\t;zero the extruded length again,G1 F200 E-9,T0\t\t;switch to the left extruder,G92 E0\t\t;zero the extruded length,G1 F'+str(purgeSpeedT0)+' E'+str(startPurgeLengthT0)+'\t;extrude '+str(startPurgeLengthT0)+'mm of feed stock,G92 E0\t\t;zero the extruded length again'+printModeGcode+'</startingGcode>')
        postProcessingScript += ',{REPLACE "M104 S'+str(hotendRightTemperature)+' T1" ""}'
        fff.append('    <postProcessing>'+postProcessingScript+'</postProcessing>')
        fff.append('  </autoConfigureExtruders>')
    if hotendRight['id'] != 'None':
        fff.append('  <autoConfigureExtruders name="Right Extruder Only"  allowedToolheads="1">')
        fff.append('    <startingGcode>;Sigma ProGen '+PS.progenVersionNumber+' (Build '+PS.progenBuildNumber+'),T1,'+firstHeatSequence(hotendLeft, hotendRight, 0, hotendRightTemperature, bedTemperature, 'Simplify3D')+',G21\t\t;metric values,G90\t\t;absolute positioning,M82\t\t;set extruder to absolute mode,M107\t\t;start with the fan off,G28 X0 Y0\t\t;move X/Y to min endstops,G28 Z0\t\t;move Z to min endstops,G92 E0\t\t;zero the extruded length,G1 Z5 F200\t\t;safety Z axis movement,G1 F'+str(purgeSpeedT1)+' E'+str(startPurgeLengthT1)+'\t;extrude '+str(startPurgeLengthT1)+'mm of feed stock,G92 E0\t\t;zero the extruded length again</startingGcode>')
        postProcessingScript += ',{REPLACE "M104 S'+str(hotendLeftTemperature)+' T0" ""}'
        fff.append('    <postProcessing>'+postProcessingScript+'</postProcessing>')
        fff.append('  </autoConfigureExtruders>')
    if hotendLeft['id'] != 'None' and hotendRight['id'] != 'None':
        fff.append('  <autoConfigureExtruders name="Both Extruders"  allowedToolheads="2">')
        fff.append('    <startingGcode>;Sigma ProGen '+PS.progenVersionNumber+' (Build '+PS.progenBuildNumber+'),,'+firstHeatSequence(hotendLeft, hotendRight, hotendLeftTemperature, hotendRightTemperature, bedTemperature, 'Simplify3D')+',G21\t\t;metric values,G90\t\t;absolute positioning,M108 P1\t\t;enable layer fan for idle extruder,M107\t\t;start with the fan off,G28 X0 Y0\t\t;move X/Y to min endstops,G28 Z0\t\t;move Z to min endstops,T1\t\t;switch to the right extruder,G92 E0\t\t;zero the extruded length,G1 F'+str(purgeSpeedT1)+' E'+str(startPurgeLengthT1)+'\t;extrude '+str(startPurgeLengthT1)+'mm of feed stock,G92 E0\t\t;zero the extruded length again,G1 F200 E-9,T0\t\t;switch to the left extruder,G92 E0\t\t;zero the extruded length,G1 F'+str(purgeSpeedT0)+' E'+str(startPurgeLengthT0)+'\t;extrude '+str(startPurgeLengthT0)+'mm of feed stock,G92 E0\t\t;zero the extruded length again</startingGcode>')
        fff.append('    <layerChangeGcode></layerChangeGcode>')
        fff.append('    <postProcessing>'+postProcessingScript+'</postProcessing>')
        fff.append('  </autoConfigureExtruders>')

    fff.append('</profile>')

    fileName = fileName + '.fff'
    fileContent = '\n'.join(fff)
    return fileName, fileContent

def cura2Profile(machine):
    '''
        Values hierarchy:
            
            quality->material->variant->definition

            We first ask if the top (user) has the setting value. If not, we continue down. So if the quality sets a value (say fan speed) and material sets it as well, the one set by the quality is used.
    '''

    filesList = [] # List containing tuples: (fileName, fileContent)

    for hotend in sorted(PS.profilesData['hotend'], key=lambda k: k['id']):
        cura2PreferredVariant = hotend['id'].replace(' ', '_')
        if machine['defaultHotend'] in hotend['id']:
            cura2PreferredVariant = hotend['id'].replace(' ', '_')
            break

    for quality in sorted(PS.profilesData['quality'], key=lambda k: k['index']):
        cura2PreferredQuality = quality['id'].replace(' ', '_')
        if 'Standard' in quality['id']:
            cura2PreferredQuality = quality['id'].replace(' ', '_')
            break

    for filament in sorted(PS.profilesData['filament'], key=lambda k: k['id']):
        cura2PreferredMaterial = filament['id'].replace(' ', '_')
        if 'Colorfila PLA' in filament['id']:
            cura2PreferredMaterial = filament['id'].replace(' ', '_')
            if 'Pumpkin Orange' in filament['colors']:
                cura2PreferredMaterial += '_Pumpkin_Orange'
            break

    fileName = 'Cura 2/resources/definitions/'+machine['id']+'.def.json'
    definition = []
    definition.append('{')
    definition.append('    "id": "'+machine['id']+'",')
    definition.append('    "version": 2,')
    definition.append('    "name": "'+machine['name']+'",')
    if 'inherits' in machine:
        definition.append('    "inherits": "'+machine['inherits']+'",')
    else:
        definition.append('    "inherits": "fdmprinter",')
    definition.append('    "metadata": {')
    definition.append('        "author": "'+machine['author']+'",')
    definition.append('        "category": "'+machine['category']+'",')
    definition.append('        "manufacturer": "'+machine['manufacturer']+'",')
    definition.append('        "file_formats": "text/x-gcode",')
    definition.append('        "platform": "'+machine['id']+'_bed.stl",')
    # definition.append('        "platform_texture": "'+machine['id']+'backplate.png",')
    definition.append('        "platform_offset": [0, 0, 0],')
    definition.append('        "has_machine_quality": true,')
    definition.append('        "visible": true,')
    if 'variants' in machine:
        definition.append('        "variant_definition": "'+machine['variants']+'",')
    if 'qualities' in machine:
        definition.append('        "quality_definition": "'+machine['qualities']+'",')
    definition.append('        "has_materials": true,')
    definition.append('        "has_machine_materials": true,')
    definition.append('        "has_variant_materials": true,')
    definition.append('        "has_variants": true,')
    definition.append('        "preferred_material": "*'+cura2PreferredMaterial+'*",')
    definition.append('        "preferred_variant": "*'+cura2PreferredVariant+'*",')
    definition.append('        "preferred_quality": "*'+cura2PreferredQuality+'*",')
    definition.append('        "variants_name": "Hotend",')
    definition.append('        "machine_extruder_trains":')
    definition.append('        {')
    definition.append('            "0": "'+machine['id']+'_extruder_left",')
    definition.append('            "1": "'+machine['id']+'_extruder_right"')
    definition.append('        }')
    definition.append('    },')
    definition.append('    "overrides": {')
    definition.append('        "machine_name": { "default_value": "'+machine['name']+'" },')
    if 'inherits' in machine:
        definition.append('        "machine_width": { "default_value": '+str(machine['width'])+' },')
        definition.append('        "print_mode": { "enabled": true },')
        setToValueIfPrintModeIsNotRegular = []
        setToValueIfPrintModeIsNotRegular.append(['wall_extruder_nr', '-1', '-1'])
        setToValueIfPrintModeIsNotRegular.append(['wall_0_extruder_nr', '-1', '-1'])
        setToValueIfPrintModeIsNotRegular.append(['wall_x_extruder_nr', '-1', '-1'])
        setToValueIfPrintModeIsNotRegular.append(['roofing_extruder_nr', '-1', '-1'])
        setToValueIfPrintModeIsNotRegular.append(['top_bottom_extruder_nr', '-1', '-1'])
        setToValueIfPrintModeIsNotRegular.append(['infill_extruder_nr', '-1', '-1'])
        setToValueIfPrintModeIsNotRegular.append(['support_extruder_nr', '0', '0'])
        setToValueIfPrintModeIsNotRegular.append(['support_infill_extruder_nr', '0', "'support_extruder_nr'"])
        setToValueIfPrintModeIsNotRegular.append(['support_extruder_nr_layer_0', '0', "'support_extruder_nr'"])
        setToValueIfPrintModeIsNotRegular.append(['support_interface_extruder_nr', '0', "'support_extruder_nr'"])
        setToValueIfPrintModeIsNotRegular.append(['support_roof_extruder_nr', '0', "'support_extruder_nr'"])
        setToValueIfPrintModeIsNotRegular.append(['support_bottom_extruder_nr', '0', "'support_extruder_nr'"])
        setToValueIfPrintModeIsNotRegular.append(['adhesion_extruder_nr', '0', '0'])
        setToValueIfPrintModeIsNotRegular.append(['prime_tower_enable', 'false', 'false'])
        setToValueIfPrintModeIsNotRegular.append(['ooze_shield_enabled', 'false', 'false'])
        setToValueIfPrintModeIsNotRegular.append(['smart_purge', 'false', 'true'])
        for parameter in setToValueIfPrintModeIsNotRegular:
            definition.append('        "'+parameter[0]+'":')
            definition.append('        {')
            definition.append('            "enabled": "print_mode == '+"'regular'"+'",')
            definition.append('            "value": "'+parameter[1]+' if print_mode != '+"'regular'"+' else '+parameter[2]+'"')
            definition.append('        },')
        definition.append('        "avoid_grinding_filament": { "value": false }')
    else:
        definition.append('        "machine_width": { "default_value": '+str(machine['width'])+' },')
        definition.append('        "machine_depth": { "default_value": '+str(machine['depth'])+' },')
        definition.append('        "machine_height": { "default_value": '+str(machine['height'])+' },')
        definition.append('        "machine_heated_bed": { "default_value": true },')
        definition.append('        "machine_extruder_count": { "default_value": 2 },')
        definition.append('        "machine_center_is_zero": { "default_value": false },')
        definition.append('        "machine_gcode_flavor": { "default_value": "RepRap (Marlin/Sprinter)" },')
        definition.append('        "machine_head_with_fans_polygon":')
        definition.append('        {')
        definition.append('            "default_value":')
        definition.append('            [')
        definition.append('                '+str(machine['extruderHead'][0])+',')
        definition.append('                '+str(machine['extruderHead'][1])+',')
        definition.append('                '+str(machine['extruderHead'][2])+',')
        definition.append('                '+str(machine['extruderHead'][3]))
        definition.append('            ]')
        definition.append('        },')
        definition.append('        "gantry_height": { "default_value": '+str(machine['height'])+' },')
        definition.append('        "extruder_prime_pos_z": { "default_value": 2.0 },') # The Z coordinate of the position where the nozzle primes at the start of printing.
        definition.append('        "extruder_prime_pos_abs": { "default_value": false },') # Make the extruder prime position absolute rather than relative to the last-known location of the head.
        definition.append('        "machine_max_feedrate_x": { "default_value": 200 },')
        definition.append('        "machine_max_feedrate_y": { "default_value": 200 },')
        definition.append('        "machine_max_feedrate_z": { "default_value": 15 },')
        definition.append('        "machine_acceleration": { "default_value": 2000 },')
        definition.append('        "material_flow_dependent_temperature":')
        definition.append('        {')
        definition.append('            "enabled": true,')
        definition.append('            "value": true')
        definition.append('        },')
        # definition.append('        "material_flow_temp_graph": { "enabled": "machine_nozzle_temp_enabled and material_flow_dependent_temperature" },') # Bad visualization
        definition.append('        "print_sequence": { "enabled": true },')
        definition.append('        "start_layers_at_same_position": { "enabled": true },')
        definition.append('        "layer_height": { "maximum_value": "0.75 * min(extruderValues('+"'machine_nozzle_size'"+'))" },')
        definition.append('        "layer_height_0":')
        definition.append('        {')
        definition.append('            "maximum_value": "0.75 * min(extruderValues('+"'machine_nozzle_size'"+'))",')
        definition.append('            "value": "min(extruderValues('+"'machine_nozzle_size'"+')) / 2"')
        definition.append('        },')
        # definition.append('        "support_enable":')
        # definition.append('        {')
        # definition.append('            "default_value": false,')
        # definition.append('            "resolve": "'+"'True' if 'True' in extruderValues('support_enable') else 'False'"+'"') # Not working
        # definition.append('        },')
        definition.append(r'        "machine_start_gcode": { "default_value": "\n;Sigma ProGen '+PS.progenVersionNumber+' (Build '+PS.progenBuildNumber+r')\n\nG21\t\t;metric values\nG90\t\t;absolute positioning\nM82\t\t;set extruder to absolute mode\nM108 P1\t\t;enable layer fan for idle extruder\nM107\t\t;start with the fan off\nG28 X0 Y0\t\t;move X/Y to min endstops\nG28 Z0\t\t;move Z to min endstops\nG1 Z5 F200\t\t;safety Z axis movement\nT1\t\t;switch to the right extruder\nG92 E0\t\t;zero the extruded length\nG1 E20 F50\t\t;extrude 20mm of feed stock\nG92 E0\t\t;zero the extruded length\nG4 P2000\t\t;stabilize hotend'+"'"+r's pressure\nG1 F2400 E-8\t\t;retract\nT0\t\t;switch to the left extruder\nG92 E0\t\t;zero the extruded length\nG1 E20 F50\t\t;extrude 20mm of feed stock\nG92 E0\t\t;zero the extruded length\nG4 P2000\t\t;stabilize hotend'+"'"+r's pressure\nG1 F2400 E-8\t\t;retract\n" },')
        definition.append(r'        "machine_end_gcode": { "default_value": "\nM104 S0 T0\t\t;left extruder heater off\nM104 S0 T1\t\t;right extruder heater off\nM140 S0\t\t;heated bed heater off\nG91\t\t;relative positioning\nG1 Z+0.5 E-5 Y+10 F12000\t;move Z up a bit and retract filament\nG28 X0 Y0\t\t;move X/Y to min endstops so the head is out of the way\nM84\t\t;steppers off\nG90\t\t;absolute positioning\n" },')
        definition.append('        "machine_nozzle_temp_enabled": { "value": true },')
        definition.append('        "material_bed_temp_wait": { "value": true },')
        definition.append('        "material_print_temp_wait": { "value": true },')
        definition.append('        "material_bed_temp_prepend": { "value": false },') # Cura 2.5 ignores it
        definition.append('        "material_print_temp_prepend": { "value": false },') # Cura 2.5 ignores it
        definition.append('        "smart_purge": { "enabled": true },')
        definition.append('        "retract_reduction": { "enabled": true },')
        definition.append('        "avoid_grinding_filament":')
        definition.append('        {')
        definition.append('            "enabled": true,')
        definition.append('            "value": true')
        definition.append('        },')            
        definition.append('        "auto_apply_fixes": { "value": true }')

    definition.append('    }')
    definition.append('}')
    fileContent = '\n'.join(definition)
    filesList.append((fileName, fileContent))

    fileName = 'Cura 2/resources/extruders/'+machine['id']+'_extruder_left.def.json'
    extruder = []
    extruder.append('{')
    extruder.append('    "id": "'+machine['id']+'_extruder_left",')
    extruder.append('    "version": 2,')
    extruder.append('    "name": "Extruder Left",')
    extruder.append('    "inherits": "fdmextruder",')
    extruder.append('    "metadata": {')
    extruder.append('        "machine": "'+machine['id']+'",')
    extruder.append('        "position": "0"')
    extruder.append('    },')
    extruder.append('')
    extruder.append('    "overrides": {')
    extruder.append('        "extruder_nr": {')
    extruder.append('            "default_value": 0,')
    extruder.append('            "maximum_value": "1"')
    extruder.append('        },')
    extruder.append('        "machine_nozzle_offset_x": { "default_value": 0.0 },')
    extruder.append('        "machine_nozzle_offset_y": { "default_value": 0.0 },')
    extruder.append(r'        "machine_extruder_start_code": { "default_value": "G91\nG1 F12000 Z2\nG90\n" },') # Should be set as a quality parameter, but Cura 2.5 doesn't allow it
    extruder.append('        "machine_extruder_start_pos_abs": { "default_value": false },')
    extruder.append('        "machine_extruder_start_pos_x": { "default_value": 0.0 },')
    extruder.append('        "machine_extruder_start_pos_y": { "default_value": 0.0 },')
    extruder.append('        "machine_extruder_end_code": { "default_value": "" },')
    extruder.append('        "machine_extruder_end_pos_abs": { "default_value": false },')
    extruder.append('        "machine_extruder_end_pos_x": { "default_value": 0.0 },')
    extruder.append('        "machine_extruder_end_pos_y": { "default_value": 0.0 },')
    extruder.append('        "extruder_prime_pos_x": { "default_value": 0.0 },')
    extruder.append('        "extruder_prime_pos_y": { "default_value": 0.0 }')
    extruder.append('    }')
    extruder.append('}')
    fileContent = '\n'.join(extruder)
    filesList.append((fileName, fileContent))

    fileName = 'Cura 2/resources/extruders/'+machine['id']+'_extruder_right.def.json'
    extruder = []
    extruder.append('{')
    extruder.append('    "id": "'+machine['id']+'_extruder_right",')
    extruder.append('    "version": 2,')
    extruder.append('    "name": "Extruder Right",')
    extruder.append('    "inherits": "fdmextruder",')
    extruder.append('    "metadata": {')
    extruder.append('        "machine": "'+machine['id']+'",')
    extruder.append('        "position": "1"')
    extruder.append('    },')
    extruder.append('')
    extruder.append('    "overrides": {')
    extruder.append('        "extruder_nr": {')
    extruder.append('            "default_value": 1,')
    extruder.append('            "maximum_value": "1"')
    extruder.append('        },')
    extruder.append('        "machine_nozzle_offset_x": { "default_value": 0.0 },')
    extruder.append('        "machine_nozzle_offset_y": { "default_value": 0.0 },')
    extruder.append(r'        "machine_extruder_start_code": { "default_value": "G91\nG1 F12000 Z2\nG90\n" },') # Should be set as a quality parameter, but Cura 2.5 doesn't allow it
    extruder.append('        "machine_extruder_start_pos_abs": { "default_value": false },')
    extruder.append('        "machine_extruder_start_pos_x": { "default_value": 0.0 },')
    extruder.append('        "machine_extruder_start_pos_y": { "default_value": 0.0 },')
    extruder.append('        "machine_extruder_end_code": { "default_value": "" },')
    extruder.append('        "machine_extruder_end_pos_abs": { "default_value": false },')
    extruder.append('        "machine_extruder_end_pos_x": { "default_value": 0.0 },')
    extruder.append('        "machine_extruder_end_pos_y": { "default_value": 0.0 },')
    extruder.append('        "extruder_prime_pos_x": { "default_value": 0.0 },')
    extruder.append('        "extruder_prime_pos_y": { "default_value": 0.0 }')
    extruder.append('    }')
    extruder.append('}')
    fileContent = '\n'.join(extruder)
    filesList.append((fileName, fileContent))

    for filament in sorted(PS.profilesData['filament'], key=lambda k: k['id']):
        for color in filament['colors']:
            fileName = 'Cura 2/resources/materials/'+machine['manufacturer']+'/'+(filament['brand']+'_'+filament['material']+'_'+color+'.xml.fdm_material').replace(' ', '_')
            if (filament['brand']+'_'+filament['material']+'_'+color+'.xml.fdm_material').replace(' ', '_') not in os.listdir('Cura 2/resources/materials/'+machine['manufacturer']):
                material = []
                material.append('<?xml version="1.0" encoding="UTF-8"?>')
                material.append('<fdmmaterial xmlns="http://www.ultimaker.com/material" version="1.3">')
                material.append('    <metadata>')
                material.append('        <name>')
                material.append('            <brand>'+filament['brand']+'</brand>')
                material.append('            <material>'+filament['material']+'</material>')
                material.append('            <color>'+color+'</color>')
                material.append('        </name>')
                material.append('        <GUID>'+str(uuid.uuid1())+'</GUID>')
                material.append('        <version>1</version>')
                material.append('        <color_code>'+filament['colors'][color]+'</color_code>')
                if filament['brand'] == 'Colorfila':
                    material.append('        <instructions>http://bcn3dtechnologies.com/en/3d-printer-filaments</instructions>')
                    material.append('        <author>')
                    material.append('            <organization>BCN3D Technologies</organization>')
                    material.append('            <contact>BCN3D Support</contact>')
                    material.append('            <email>info@bcn3dtechnologies.com</email>')
                    material.append('            <phone>+34 934 137 088</phone>')
                    material.append('            <address>')
                    material.append('                <street>Esteve Terradas 1</street>')
                    material.append('                <city>Castelldefels</city>')
                    material.append('                <region>Barcelona</region>')
                    material.append('                <zip>08860</zip>')
                    material.append('                <country>Spain</country>')
                    material.append('            </address>')
                    material.append('        </author>')
                    material.append('        <supplier>')
                    material.append('            <organization>BCN3D Technologies</organization>')
                    material.append('            <contact>BCN3D Support</contact>')
                    material.append('            <email>info@bcn3dtechnologies.com</email>')
                    material.append('            <phone>+34 934 137 088</phone>')
                    material.append('            <address>')
                    material.append('                <street>Esteve Terradas 1</street>')
                    material.append('                <city>Castelldefels</city>')
                    material.append('                <region>Barcelona</region>')
                    material.append('                <zip>08860</zip>')
                    material.append('                <country>Spain</country>')
                    material.append('            </address>')
                    material.append('        </supplier>')
                    # material.append('        <EAN>11 22222 33333 4</EAN>')
                    # material.append('        <MSDS>http://...</MSDS>')
                    # material.append('        <TDS>http://...</TDS>')
                material.append('    </metadata>')
                material.append('    <properties>')
                material.append('        <density>'+str(filament['filamentDensity'])+'</density>')
                material.append('        <diameter>'+str(filament['filamentDiameter'])+'</diameter>')
                material.append('    </properties>')
                material.append('    <settings>')
                material.append('        <setting key="print temperature">'+str(defaultMaterialPrintTemperature(filament))+'</setting>') # default_material_print_temperature
                material.append('        <setting key="heated bed temperature">'+str(filament['bedTemperature'])+'</setting>') # material_bed_temperature
                material.append('')
                for m in sorted(PS.profilesData['machine'], key=lambda k: k['id']):
                    material.append('        <machine>')
                    material.append('           <machine_identifier manufacturer="'+m['manufacturer']+'" product="'+m['id']+'" />')
                    for hotend in sorted(PS.profilesData['hotend'], key=lambda k: k['id']):
                        if hotend['id'] != 'None':
                            material.append('           <hotend id="'+hotend['id']+'">')
                            if filament['isAbrasiveMaterial'] and hotend['material'] == "Brass":
                                material.append('                <setting key="hardware compatible">no</setting>')
                            else:
                                material.append('                <setting key="hardware compatible">yes</setting>')
                            material.append('           </hotend>')
                    material.append('        </machine>')
                material.append('')
                material.append('    </settings>')
                material.append('</fdmmaterial>')
                fileContent = '\n'.join(material)
                filesList.append((fileName, fileContent))

    if 'qualities' not in machine:
        globalQualities = []
        for hotend in sorted(PS.profilesData['hotend'], key=lambda k: k['id']):
            if hotend['id'] != 'None':
                for filament in sorted(PS.profilesData['filament'], key=lambda k: k['id']):
                    for color in filament['colors']:
                        for quality in sorted(PS.profilesData['quality'], key=lambda k: k['index']):
                            layerHeight = getLayerHeight(hotend, quality)
                            firstLayerHeight = hotend['nozzleSize']/2.
                            defaultSpeed, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed = speedValues(hotend, hotend, filament, filament, layerHeight, firstLayerHeight, 1, quality, 'MEX Left')
                            hotendLeftTemperature = temperatureAdjustedToFlow(filament, hotend, layerHeight, defaultSpeed)
                            startPurgeLength, toolChangePurgeLength, purgeSpeed, sParameter, eParameter, pParameter = purgeValues(hotend, filament, defaultSpeed, layerHeight)
                            # Create a new global quality for the new layer height
                            if layerHeight not in globalQualities:
                                globalQualities.append(layerHeight)
                                fileName = 'Cura 2/resources/quality/'+machine['id']+'/'+machine['id']+'_global_Layer_'+("%.2f" % layerHeight)+'_mm_Quality.inst.cfg'
                                qualityFile = []
                                qualityFile.append('[general]')
                                qualityFile.append('version = 2')
                                qualityFile.append('name = Global Layer '+("%.2f" % layerHeight)+' mm')
                                qualityFile.append('definition = '+machine['id'])
                                qualityFile.append('')
                                qualityFile.append('[metadata]')
                                qualityFile.append('type = quality')
                                qualityFile.append('quality_type = layer'+("%.2f" % layerHeight)+'mm')
                                qualityFile.append('global_quality = True')
                                qualityFile.append('weight = '+str(len(globalQualities)))
                                qualityFile.append('setting_version = 2')
                                qualityFile.append('')
                                qualityFile.append('[values]')
                                qualityFile.append('layer_height = '+("%.2f" % layerHeight))
                                fileContent = '\n'.join(qualityFile)
                                filesList.append((fileName, fileContent))

                            fileName = 'Cura 2/resources/quality/'+machine['id']+'/'+'_'.join([machine['id'], hotend['id'], filament['brand'], filament['material'], color, quality['id'], 'Quality.inst.cfg']).replace(' ', '_')

                            # keep all default values commented

                            qualityFile = []
                            qualityFile.append('[general]')
                            qualityFile.append('version = 2')
                            qualityFile.append('name = '+quality['id']+' Quality')
                            qualityFile.append('definition = '+machine['id'])
                            qualityFile.append('')
                            qualityFile.append('[metadata]')
                            qualityFile.append('type = quality')
                            qualityFile.append('quality_type = layer'+("%.2f" % layerHeight)+'mm')
                            qualityFile.append('material = '+'_'.join([filament['brand'], filament['material'], color, machine['id'], hotend['id']]).replace(' ', '_'))
                            for index in range(len(globalQualities)):
                                if globalQualities[index] == layerHeight:
                                    qualityFile.append('weight = '+str(index+1))
                                    break
                            qualityFile.append('setting_version = 2')
                            qualityFile.append('')
                            qualityFile.append('[values]')

                            
                            # qualityFile.append(r'machine_extruder_start_code = ="\nM800 F'+str(purgeSpeed)+' S'+str(sParameter)+' E'+str(eParameter)+' P'+str(pParameter)+r'\t;SmartPurge - Needs Firmware v01-1.2.3\nG4 P2000\t\t\t\t;Stabilize Hotend'+"'"+r's pressure\nG92 E0\t\t\t\t;Zero extruder\nG1 F3000 E-4.5\t\t\t\t;Retract\nG1 F12000\t\t\t;End tool switch\nG91\nG1 F12000 Z2\nG90\n"') # Keyword NOT WORKING on Cura 2.5

                            # resolution
                            qualityFile.append('layer_height = '+("%.2f" % layerHeight))
                            qualityFile.append('line_width = =round(machine_nozzle_size * 0.875, 3)')
                            # qualityFile.append('wall_line_width = =line_width')
                            # qualityFile.append('wall_line_width_0 = =wall_line_width')
                            qualityFile.append('wall_line_width_x = =machine_nozzle_size * 0.85')
                            # qualityFile.append('roofing_line_width = =skin_line_width')
                            # qualityFile.append('skin_line_width = =line_width')
                            qualityFile.append('infill_line_width = =machine_nozzle_size * 1.25')
                            # qualityFile.append('skirt_brim_line_width = =line_width')
                            qualityFile.append('support_line_width = =infill_line_width')
                            # qualityFile.append('support_interface_line_width = =line_width')
                            # qualityFile.append('support_roof_line_width = =extruderValue(support_roof_extruder_nr, '+"'support_interface_line_width'"+')
                            # qualityFile.append('support_bottom_line_width = =extruderValue(support_bottom_extruder_nr, '+"'support_interface_line_width'"+'')
                            # qualityFile.append('prime_tower_line_width = =line_width')
                            # qualityFile.append('initial_layer_line_width_factor = 100')

                            #shell
                            # qualityFile.append('wall_extruder_nr = =-1')
                            # qualityFile.append('wall_0_extruder_nr = =wall_extruder_nr')
                            # qualityFile.append('wall_x_extruder_nr = =wall_extruder_nr')
                            qualityFile.append('wall_thickness = =max( 3 * machine_nozzle_size, '+("%.2f" % quality['wallWidth'])+')')     # 3 minimum Perimeters needed
                            qualityFile.append('wall_0_wipe_dist = =12.5 * machine_nozzle_size')
                            # qualityFile.append('roofing_extruder_nr = =-1')
                            # qualityFile.append('roofing_layer_count = =0')
                            # qualityFile.append('roofing_pattern = =skin_angles')
                            # qualityFile.append('roofing_angles = =top_bottom_pattern')
                            # qualityFile.append('top_bottom_extruder_nr = =-1')
                            qualityFile.append('top_bottom_thickness = =max( 5 * layer_height, '+("%.2f" % quality['topBottomWidth'])+')') # 5 minimum layers needed
                            # qualityFile.append('top_thickness = =top_bottom_thickness')
                            # qualityFile.append('bottom_thickness = =top_bottom_thickness')
                            # qualityFile.append('top_bottom_pattern = =lines')
                            # qualityFile.append('top_bottom_pattern_0 = =top_bottom_pattern')
                            # qualityFile.append('skin_angles = =[ ]') # ?? check syntax
                            # qualityFile.append('wall_0_inset = 0')
                            # qualityFile.append('outer_inset_first = False')
                            # qualityFile.append('alternate_extra_perimeter = False')
                            if filament['isFlexibleMaterial']:
                                qualityFile.append('travel_compensate_overlapping_walls_enabled = False')
                            else: 
                                qualityFile.append('travel_compensate_overlapping_walls_enabled = True') 
                            # qualityFile.append('fill_perimeter_gaps = everywhere')
                            # qualityFile.append('fill_outline_gaps = everywhere')
                            # qualityFile.append('xy_offset = 0')
                            qualityFile.append('xy_offset_layer_0 = -0.1')
                            qualityFile.append('z_seam_type = back') 
                            qualityFile.append('z_seam_x = '+str(int(machine['width']/2))) 
                            qualityFile.append('z_seam_y = '+str(machine['depth']))
                            qualityFile.append('z_seam_relative = True')
                            # qualityFile.append('skin_no_small_gaps_heuristic = True') 

                            # infill
                            # qualityFile.append('infill_extruder_nr = =-1')
                            qualityFile.append('infill_sparse_density = ='+str(int(min(100, quality['infillPercentage'] * 1.25)))+" if infill_pattern == 'cubicsubdiv' else "+str(int(quality['infillPercentage']))) # 'if' is not working... # 'if' is not working...
                            qualityFile.append('infill_pattern = grid')
                            # qualityFile.append('infill_angles = []')
                            # qualityFile.append('sub_div_rad_mult = 100')
                            # qualityFile.append('sub_div_rad_add = =wall_line_width_x')
                            # qualityFile.append('infill_overlap = =10 if infill_sparse_density < 95 and infill_pattern != '+"'"+'concentric'+"'"+' else 0')
                            qualityFile.append("skin_overlap = =10 if top_bottom_pattern != 'concentric' else 0")
                            # qualityFile.append('infill_wipe_dist = =wall_line_width_0 / 4 if wall_line_count == 1 else wall_line_width_x / 4')
                            qualityFile.append('infill_sparse_thickness = =layer_height')
                            # qualityFile.append('gradual_infill_steps = 0')
                            # qualityFile.append('gradual_infill_step_height = 5')
                            qualityFile.append('infill_before_walls = False')
                            # qualityFile.append('min_infill_area = 0')
                            # qualityFile.append('max_skin_angle_for_expansion = 20')

                            # material -> default_material_print_temperature, material_bed_temperature,  must be set into material to avoid conflicts
                            qualityFile.append('material_print_temperature = =default_material_print_temperature + '+str(temperatureAdjustedToFlow(filament, hotend, layerHeight, defaultSpeed) - defaultMaterialPrintTemperature(filament)))
                            qualityFile.append('material_print_temperature_layer_0 = =default_material_print_temperature + '+str(int(round((getTemperature(hotend, filament, 'highTemperature')))) - defaultMaterialPrintTemperature(filament)))
                            temperatureInertiaInitialFix = 0
                            qualityFile.append('material_initial_print_temperature = =material_print_temperature + '+str(temperatureInertiaInitialFix))
                            temperatureInertiaFinalFix = -2.5
                            qualityFile.append('material_final_print_temperature = =material_print_temperature + '+str(temperatureInertiaFinalFix))
                            minFlow = 0.3 * 0.05 * 10
                            minTemp = getTemperature(hotend, filament, 'lowTemperature')
                            maxFlow = maxFlowValue(hotend, filament, layerHeight)
                            maxTemp = getTemperature(hotend, filament, 'highTemperature')
                            stdFlow = 0.4 * 0.15 * 60
                            stdTemp = (minTemp + maxTemp) /2.
                            qualityFile.append('material_flow_temp_graph = [['+str(minFlow)+','+str(minTemp)+'], ['+str(stdFlow)+','+str(stdTemp)+'], ['+str(maxFlow)+','+str(maxTemp)+']]')
                            qualityFile.append('material_extrusion_cool_down_speed = 1') # this value depends on extruded flow (not material_flow)
                            qualityFile.append('material_diameter = '+("%.2f" % filament['filamentDiameter']))
                            qualityFile.append('material_flow = '+("%.2f" % (filament['extrusionMultiplier'] * 100)))
                            # qualityFile.append('retraction_enable = True')
                            # qualityFile.append('retract_at_layer_change = False')
                            qualityFile.append('retraction_amount = '+("%.2f" % filament['retractionDistance']))
                            qualityFile.append('retraction_speed = '+("%.2f" % filament['retractionSpeed']))
                            # qualityFile.append('retraction_retract_speed = =retraction_speed')
                            # qualityFile.append('retraction_prime_speed = =retraction_speed')
                            # qualityFile.append('retraction_extra_prime_amount = 0') # Adjust for flex materials
                            qualityFile.append('retraction_min_travel = 1.5')
                            qualityFile.append('retraction_count_max = '+str(int(filament['retractionCount'])))
                            # qualityFile.append('retraction_extrusion_window = =retraction_amount')
                            standbyTemperature = int(getTemperature(hotend, filament, 'standbyTemperature'))
                            qualityFile.append('material_standby_temperature = '+str(standbyTemperature))
                            # qualityFile.append('switch_extruder_retraction_amount = =machine_heat_zone_length')
                            qualityFile.append('switch_extruder_retraction_speed = =retraction_speed')
                            # qualityFile.append('switch_extruder_extra_prime_amount = '+("%.2f" % filament['retractionSpeed'])) # Parameter that should be there to purge on toolchage
                            qualityFile.append('switch_extruder_prime_speed = =retraction_speed')

                            # speed
                            qualityFile.append('speed_print = '+("%.2f" % (defaultSpeed/60.)))
                            # qualityFile.append('speed_infill = =speed_print')
                            qualityFile.append('speed_wall = =round(speed_print - (speed_print - speed_print * '+("%.2f" % outlineUnderspeed)+') / 2, 1)')
                            qualityFile.append('speed_wall_0 = =round(speed_print * '+("%.2f" % outlineUnderspeed)+', 1)')
                            qualityFile.append('speed_wall_x = =speed_wall')
                            # qualityFile.append('speed_roofing = =speed_topbottom')
                            qualityFile.append('speed_topbottom = =speed_wall_0')
                            # qualityFile.append('speed_ironing = =speed_roofing * 20 / 30')
                            qualityFile.append('speed_support = =round(speed_print * '+("%.2f" % supportUnderspeed)+', 1)')
                            # qualityFile.append('speed_support_infill = =speed_support')
                            qualityFile.append('speed_support_interface = =speed_wall')
                            qualityFile.append('speed_travel = =round(speed_print if magic_spiralize else 200)')
                            qualityFile.append('speed_layer_0 = =round(speed_print * '+("%.2f" % firstLayerUnderspeed)+', 1)')
                            # qualityFile.append('speed_print_layer_0 = =speed_layer_0')
                            qualityFile.append('speed_travel_layer_0 = =round(speed_travel / 3, 1)')
                            # qualityFile.append('skirt_brim_speed = =speed_layer_0')
                            # qualityFile.append('speed_slowdown_layers = 2')
                            qualityFile.append('speed_equalize_flow_enabled = True')
                            qualityFile.append('speed_equalize_flow_max = 100')
                            qualityFile.append('acceleration_enabled = True')
                            qualityFile.append('acceleration_print = 2000')
                            # qualityFile.append('acceleration_infill = =acceleration_print')
                            qualityFile.append('acceleration_wall = =round(acceleration_print - (acceleration_print - acceleration_wall_0)/ 2)')
                            qualityFile.append('acceleration_wall_0 = '+str(int(accelerationForPerimeters(hotend['nozzleSize'], layerHeight, int(defaultSpeed/60. * outlineUnderspeed)))))
                            # qualityFile.append('acceleration_wall_x = =acceleration_wall')
                            # qualityFile.append('acceleration_roofing = =acceleration_topbottom')
                            qualityFile.append('acceleration_topbottom = =acceleration_wall_0')
                            # qualityFile.append('acceleration_ironing = =acceleration_roofing')
                            qualityFile.append('acceleration_support = =acceleration_wall')
                            # qualityFile.append('acceleration_support_infill = =acceleration_support')
                            qualityFile.append('acceleration_support_interface = =acceleration_topbottom')
                            qualityFile.append('acceleration_travel = =acceleration_print if magic_spiralize else 2250')
                            qualityFile.append('acceleration_layer_0 = =acceleration_topbottom')
                            # qualityFile.append('acceleration_print_layer_0 = =acceleration_layer_0')
                            # qualityFile.append('acceleration_travel_layer_0 = =acceleration_layer_0 * acceleration_travel / acceleration_print')
                            # qualityFile.append('acceleration_skirt_brim = =acceleration_layer_0')
                            qualityFile.append('jerk_enabled = True')
                            qualityFile.append('jerk_print = =15') # Adjust all jerk
                            # qualityFile.append('jerk_infill = =jerk_print')
                            qualityFile.append('jerk_wall = =jerk_print * 0.75')
                            qualityFile.append('jerk_wall_0 = =jerk_wall * 0.5')
                            # qualityFile.append('jerk_wall_x = =jerk_wall')
                            # qualityFile.append('jerk_roofing = =jerk_topbottom')
                            qualityFile.append('jerk_topbottom = =jerk_print * 0.5')
                            # qualityFile.append('jerk_ironing = =jerk_roofing')
                            qualityFile.append('jerk_support = =jerk_print * 0.75')
                            # qualityFile.append('jerk_support_infill = =jerk_support')
                            qualityFile.append('jerk_support_interface = =jerk_topbottom')
                            qualityFile.append('jerk_prime_tower = =jerk_print * 0.75')
                            qualityFile.append('jerk_travel = =jerk_print if magic_spiralize else 15')
                            qualityFile.append('jerk_layer_0 = =jerk_topbottom')
                            # qualityFile.append('jerk_print_layer_0 = =jerk_layer_0')
                            # qualityFile.append('jerk_travel_layer_0 = =jerk_layer_0 * jerk_travel / jerk_print')
                            # qualityFile.append('jerk_skirt_brim = =jerk_layer_0')

                            # travel
                            if filament['isFlexibleMaterial']:
                                qualityFile.append('retraction_combing = all')
                            else:
                                qualityFile.append('retraction_combing = noskin')
                            # qualityFile.append('travel_retract_before_outer_wall = False')
                            if filament['isSupportMaterial']:
                                qualityFile.append('travel_avoid_other_parts = True')
                            else:
                                qualityFile.append('travel_avoid_other_parts = False')
                            # qualityFile.append('travel_avoid_distance = =machine_nozzle_tip_outer_diameter / 2 * 1.25')
                            qualityFile.append('start_layers_at_same_position = True') # different than z_seam
                            layerStartX, layerStartY = machine['width']/2, machine['depth']
                            qualityFile.append('layer_start_x = '+str(layerStartX)) # different than z_seam
                            qualityFile.append('layer_start_y = '+str(layerStartY)) # different than z_seam
                            qualityFile.append('retraction_hop_enabled = True')
                            qualityFile.append('retraction_hop_only_when_collides = True')
                            qualityFile.append('retraction_hop = =0.5 * layer_height')
                            # qualityFile.append('retraction_hop_after_extruder_switch = True')

                            # cooling
                            if filament['fanPercentage'][1] > 0:
                                qualityFile.append('cool_fan_enabled = True')
                            else:
                                qualityFile.append('cool_fan_enabled = False')
                            qualityFile.append('cool_fan_speed = '+str(int(filament['fanPercentage'][1])))
                            qualityFile.append('cool_fan_speed_min = '+str(int(filament['fanPercentage'][0])))
                            # qualityFile.append('cool_fan_speed_max = =cool_fan_speed')
                            # qualityFile.append('cool_min_layer_time_fan_speed_max = 10')
                            # qualityFile.append('cool_fan_speed_0 = 0')
                            qualityFile.append("cool_fan_full_at_height = =0 if adhesion_type == 'raft' else layer_height_0 + 4 * layer_height") # after 6 layers
                            # qualityFile.append('cool_min_layer_time = 5')
                            # qualityFile.append('cool_min_speed = 10')
                            # qualityFile.append('cool_lift_head = False')

                            # support
                            if filament['isSupportMaterial']:
                                # qualityFile.append('support_enable = True') # Not working
                                qualityFile.append('support_infill_rate = 25')
                                qualityFile.append('support_xy_distance = 0.5')
                                qualityFile.append('support_z_distance = 0')
                                qualityFile.append('support_interface_density = 100')
                                qualityFile.append('support_conical_enabled = False')
                                # qualityFile.append('support_conical_angle = 30')
                            else:
                                # qualityFile.append('support_enable = False')
                                qualityFile.append('support_infill_rate = 15')
                                qualityFile.append('support_xy_distance = 0.7')
                                qualityFile.append('support_z_distance = =layer_height')
                                qualityFile.append('support_interface_density = 75')
                                qualityFile.append('support_conical_enabled = True')
                                # qualityFile.append('support_conical_angle = 30')
                            # qualityFile.append('support_type = everywhere')
                            # qualityFile.append('support_pattern = zigzag')
                            # qualityFile.append('support_connect_zigzags = True')
                            # qualityFile.append('support_skip_some_zags = False')
                            # qualityFile.append('support_zag_skip_count = =6')
                            # qualityFile.append('support_top_distance = =extruderValue(support_extruder_nr, 'support_z_distance')')
                            # qualityFile.append('support_bottom_distance = =extruderValue(support_extruder_nr, 'support_z_distance') if support_type == 'everywhere' else 0')
                            # qualityFile.append('support_xy_overrides_z = z_overrides_xy')
                            # qualityFile.append('support_xy_distance_overhang = =machine_nozzle_size / 2')
                            # qualityFile.append('support_bottom_stair_step_height = 0.3')
                            qualityFile.append('support_join_distance = 10')
                            qualityFile.append('support_offset = 1')
                            # qualityFile.append('support_infill_sparse_thickness = =resolveOrValue('+"'layer_height'"+')')
                            # qualityFile.append('gradual_support_infill_steps = 0')
                            # qualityFile.append('gradual_support_infill_step_height = 1')
                            qualityFile.append('support_interface_enable = True')
                            qualityFile.append('support_interface_height = =5 * layer_height')
                            # qualityFile.append("support_roof_height =extruderValue(support_interface_extruder_nr, 'support_interface_height')")
                            # qualityFile.append("support_bottom_height = =extruderValue(support_interface_extruder_nr, 'support_interface_height')")
                            qualityFile.append('support_interface_skip_height = =layer_height')
                            qualityFile.append('support_interface_pattern = lines')
                            # qualityFile.append('support_use_towers = True')
                            # qualityFile.append('support_tower_diameter = 3.0')
                            qualityFile.append('support_minimal_diameter = 1.0')
                            # qualityFile.append('support_tower_roof_angle = 65')

                            # platform_adhesion
                            # qualityFile.append('extruder_prime_pos_x = 0')
                            # qualityFile.append('extruder_prime_pos_y = 0')
                            qualityFile.append('adhesion_type = skirt')
                            qualityFile.append('skirt_line_count = 2')
                            # qualityFile.append('skirt_gap = 3')
                            qualityFile.append("skirt_brim_minimal_length = =round((material_diameter/2)**2 / (extruderValue(adhesion_extruder_nr, 'machine_nozzle_size')/2)**2 *"+str(startPurgeLength)+', 2)')
                            # qualityFile.append('brim_width = 8')
                            # qualityFile.append('brim_outside_only = True')
                            qualityFile.append('raft_margin = 3')
                            qualityFile.append("raft_airgap = =min(extruderValues('machine_nozzle_size')) * 0.55")
                            # qualityFile.append('layer_0_z_overlap = =raft_airgap / 2')
                            # qualityFile.append('raft_surface_layers = 2')
                            # qualityFile.append('raft_surface_thickness = =layer_height')
                            # qualityFile.append('raft_surface_line_width = =line_width')
                            # qualityFile.append('raft_surface_line_spacing = =raft_surface_line_width')
                            qualityFile.append("raft_interface_thickness = =extruderValue(adhesion_extruder_nr, 'machine_nozzle_size') * 0.7")
                            qualityFile.append('raft_interface_line_width = =line_width * 1.5')
                            # qualityFile.append('raft_interface_line_spacing = =raft_interface_line_width + 0.2')
                            qualityFile.append("raft_base_thickness = =extruderValue(adhesion_extruder_nr, 'machine_nozzle_size') * 0.75")
                            qualityFile.append("raft_base_line_width = =extruderValue(adhesion_extruder_nr, 'machine_nozzle_size') * 2.5")
                            qualityFile.append("raft_base_line_spacing = =extruderValue(adhesion_extruder_nr, 'machine_nozzle_size') * 7.5")
                            # qualityFile.append('raft_speed = =speed_print / 60 * 30')
                            # qualityFile.append('raft_surface_speed = =raft_speed')
                            # qualityFile.append('raft_interface_speed = =raft_speed * 0.75')
                            # qualityFile.append('raft_base_speed = =raft_speed * 0.75')
                            # qualityFile.append('raft_acceleration = =acceleration_print')
                            # qualityFile.append('raft_surface_acceleration = =raft_acceleration')
                            # qualityFile.append('raft_interface_acceleration = =raft_acceleration')
                            # qualityFile.append('raft_base_acceleration = =raft_acceleration')
                            # qualityFile.append('raft_jerk = =jerk_print')
                            # qualityFile.append('raft_surface_jerk = =raft_jerk')
                            # qualityFile.append('raft_interface_jerk = =raft_jerk')
                            # qualityFile.append('raft_base_jerk = =raft_jerk')
                            # qualityFile.append('raft_fan_speed = 0')
                            # qualityFile.append('raft_surface_fan_speed = =raft_fan_speed')
                            # qualityFile.append('raft_interface_fan_speed = =raft_fan_speed')
                            # qualityFile.append('raft_base_fan_speed = =raft_fan_speed')

                            # dual
                            qualityFile.append('prime_tower_enable = False')
                            qualityFile.append('prime_tower_size = =max(15, round(math.sqrt(prime_tower_min_volume/layer_height), 2))')
                            qualityFile.append("prime_tower_min_volume = =round((material_diameter/2)**2 / (extruderValue(adhesion_extruder_nr, 'machine_nozzle_size')/2)**2 *"+str(toolChangePurgeLength)+', 2)')
                            # qualityFile.append("prime_tower_wall_thickness = =round(max(2 * prime_tower_line_width, 0.5 * (prime_tower_size - math.sqrt(max(0, prime_tower_size ** 2 - prime_tower_min_volume / layer_height)))), 3)")
                            # qualityFile.append('prime_tower_position_x = =machine_width - max(extruderValue(adhesion_extruder_nr, 'brim_width') * extruderValue(adhesion_extruder_nr, 'initial_layer_line_width_factor') / 100 if adhesion_type == 'brim' else (extruderValue(adhesion_extruder_nr, 'raft_margin') if adhesion_type == 'raft' else (extruderValue(adhesion_extruder_nr, 'skirt_gap') if adhesion_type == 'skirt' else 0)), max(extruderValues('travel_avoid_distance'))) - max(extruderValues('support_offset')) - sum(extruderValues('skirt_brim_line_width')) * extruderValue(adhesion_extruder_nr, 'initial_layer_line_width_factor') / 100 - 1')
                            # qualityFile.append('prime_tower_position_y = =machine_depth - prime_tower_size - max(extruderValue(adhesion_extruder_nr, 'brim_width') * extruderValue(adhesion_extruder_nr, 'initial_layer_line_width_factor') / 100 if adhesion_type == 'brim' else (extruderValue(adhesion_extruder_nr, 'raft_margin') if adhesion_type == 'raft' else (extruderValue(adhesion_extruder_nr, 'skirt_gap') if adhesion_type == 'skirt' else 0)), max(extruderValues('travel_avoid_distance'))) - max(extruderValues('support_offset')) - sum(extruderValues('skirt_brim_line_width')) * extruderValue(adhesion_extruder_nr, 'initial_layer_line_width_factor') / 100 - 1')
                            # qualityFile.append('prime_tower_flow = 100')
                            qualityFile.append('prime_tower_wipe_enabled = False')
                            qualityFile.append('dual_pre_wipe = False')
                            # qualityFile.append('prime_tower_purge_volume = 0')
                            qualityFile.append('ooze_shield_enabled = False')
                            # qualityFile.append('ooze_shield_angle = 60')
                            # qualityFile.append('ooze_shield_dist = 2')

                            # meshfix
                            # qualityFile.append('meshfix_union_all = True')
                            # qualityFile.append('meshfix_union_all_remove_holes = False')
                            # qualityFile.append('meshfix_extensive_stitching = False')
                            # qualityFile.append('meshfix_keep_open_polygons = False')
                            qualityFile.append("multiple_mesh_overlap = =0.375 * machine_nozzle_size - xy_offset")
                            # qualityFile.append('carve_multiple_volumes = True')
                            # qualityFile.append('alternate_carve_order = True')

                            # blackmagic
                            # qualityFile.append('print_sequence = all_at_once')
                            # qualityFile.append('infill_mesh = False')
                            # qualityFile.append('infill_mesh_order = 0')
                            # qualityFile.append('support_mesh = False')
                            # qualityFile.append('anti_overhang_mesh = False')
                            # qualityFile.append('magic_mesh_surface_mode = normal')
                            # qualityFile.append('magic_spiralize = False')

                            # experimental
                            # qualityFile.append('draft_shield_enabled = False')
                            # qualityFile.append('draft_shield_dist = 10')
                            # qualityFile.append('draft_shield_height_limitation = False')
                            # qualityFile.append('draft_shield_height = 10')
                            # qualityFile.append('conical_overhang_enabled = False')
                            # qualityFile.append('conical_overhang_angle = 50')
                            qualityFile.append('coasting_enable = False')
                            qualityFile.append('coasting_volume = '+str(coastVolume(hotend, filament)))
                            qualityFile.append('coasting_min_volume = =coasting_volume * 2')
                            # qualityFile.append('coasting_speed = 90')
                            # qualityFile.append('skin_outline_count = 0')
                            # qualityFile.append('skin_alternate_rotation = False')
                            qualityFile.append('support_conical_min_width = 10')
                            # qualityFile.append('infill_hollow = False')
                            # qualityFile.append('magic_fuzzy_skin_enabled = False')
                            # qualityFile.append('magic_fuzzy_skin_thickness = 0.3')
                            # qualityFile.append('magic_fuzzy_skin_point_density = 1.25')
                            # qualityFile.append('wireframe_enabled = False')
                            # qualityFile.append('wireframe_height = =machine_nozzle_head_distance')
                            # qualityFile.append('wireframe_roof_inset = =wireframe_height')
                            # qualityFile.append('wireframe_printspeed = 5')
                            # qualityFile.append('wireframe_printspeed_bottom = =wireframe_printspeed')
                            # qualityFile.append('wireframe_printspeed_up = =wireframe_printspeed')
                            # qualityFile.append('wireframe_printspeed_down = =wireframe_printspeed')
                            # qualityFile.append('wireframe_printspeed_flat = =wireframe_printspeed')
                            # qualityFile.append('wireframe_flow = 100')
                            # qualityFile.append('wireframe_flow_connection = =wireframe_flow')
                            # qualityFile.append('wireframe_flow_flat = =wireframe_flow')
                            # qualityFile.append('wireframe_top_delay = 0')
                            # qualityFile.append('wireframe_bottom_delay = 0')
                            # qualityFile.append('wireframe_flat_delay = 0.1')
                            # qualityFile.append('wireframe_up_half_speed = 0.3')
                            # qualityFile.append('wireframe_top_jump = 0.6')
                            # qualityFile.append('wireframe_fall_down = 0.5')
                            # qualityFile.append('wireframe_drag_along = 0.6')
                            # qualityFile.append('wireframe_strategy = compensate')
                            # qualityFile.append('wireframe_straight_before_down = 20')
                            # qualityFile.append('wireframe_roof_fall_down = 2')
                            # qualityFile.append('wireframe_roof_drag_along = 0.8')
                            # qualityFile.append('wireframe_roof_outer_delay = 0.2')
                            # qualityFile.append('wireframe_nozzle_clearance = 1')
                            # qualityFile.append('ironing_enabled = False')
                            # qualityFile.append('ironing_pattern = zigzag')
                            # qualityFile.append('ironing_line_spacing = zigzag')
                            # qualityFile.append('ironing_pattern = zigzag')
                            # qualityFile.append('ironing_line_spacing = =machine_nozzle_tip_outer_diameter/2')
                            # qualityFile.append('ironing_flow = 10')
                            # qualityFile.append('ironing_inset = =wall_line_width_0 / 2')
                            fileContent = '\n'.join(qualityFile)
                            filesList.append((fileName, fileContent))

    if 'variants' not in machine:
        for hotend in sorted(PS.profilesData['hotend'], key=lambda k: k['id']):
            if hotend['id'] != 'None':
                fileName = 'Cura 2/resources/variants/'+machine['id']+'_'+hotend['id'].replace(' ', '_')+'.inst.cfg'
                variant = []
                variant.append('[general]')
                variant.append('name = '+hotend['id'])
                variant.append('version = 2')
                variant.append('definition = '+machine['id'])
                variant.append('')
                variant.append('[metadata]')
                variant.append('author = '+machine['author'])
                variant.append('type = variant')
                variant.append('setting_version = 2') 
                variant.append('')
                variant.append('[values]')
                # machine settings
                variant.append('machine_nozzle_id = '+str(hotend['id']))
                variant.append('machine_nozzle_size = '+str(hotend['nozzleSize']))
                variant.append('machine_nozzle_tip_outer_diameter = '+str(hotend['nozzleTipOuterDiameter']))
                variant.append('machine_nozzle_head_distance = '+str(hotend['nozzleHeadDistance']))
                variant.append('machine_nozzle_expansion_angle = '+str(hotend['nozzleExpansionAngle']))
                variant.append('machine_heat_zone_length = 8')
                variant.append('machine_nozzle_heat_up_speed = '+str(hotend['heatUpSpeed']))
                variant.append('machine_nozzle_cool_down_speed = '+str(hotend['coolDownSpeed']))
                variant.append('machine_min_cool_heat_time_window = '+str(hotend['minimumCoolHeatTimeWindow']))
                fileContent = '\n'.join(variant)
                filesList.append((fileName, fileContent))

    return filesList

def getLayerHeight(hotend, quality):
    rawLayerHeight = hotend['nozzleSize'] * quality['layerHeightMultiplier']
    if rawLayerHeight > 0.1:
        if rawLayerHeight > 0.2:
            base = 0.1
        else:
            base = 0.05
    else:
        base = 0.025
    return round(rawLayerHeight / base) * base

def purgeValues(hotend, filament, speed, layerHeight, minPurgeLength = 20): # purge at least 20mm so the filament weight is enough to stay inside the purge container
    
    '''
    SmartPurge Command:
    M800 F-- S-- E-- P--
        F - Speed
        S - Slope (according to NSize, Flow, Purge@5min)
        E - Maximum distance to purge (according to NSize, Flow)
        P - Minimum distance to purge
    '''

    # nozzleSizeBehavior
    maxPurgeLenghtAtHotendTip = 2.25 * filament['purgeLength'] * filament['extrusionMultiplier']
    minPurgeLenghtAtHotendTip = 0.5  * filament['purgeLength'] * filament['extrusionMultiplier']
    curveGrowth = 1 # Here we assume the growth curve is constant for all materials. Change this value if it's not
    hotendPurgeMultiplier = (maxPurgeLenghtAtHotendTip - (maxPurgeLenghtAtHotendTip-minPurgeLenghtAtHotendTip)*math.exp(-hotend['nozzleSize']/float(curveGrowth)))/float(filament['purgeLength'])

    baseStartLength04 = 7
    startPurgeLength = float("%.2f" % max(10, (hotendPurgeMultiplier * baseStartLength04)))
    
    # this length is a FIXED value. It is not used on SmartPurge, we do not recommend to work with fixed purge lengths
    baseToolChangeLength04 = 1.5 # experimental value that works well for most of the prints
    toolChangePurgeLength = float("%.2f" % (hotendPurgeMultiplier * baseToolChangeLength04))

    # F - Extrusion Speed -> adjusted to improve surplus material storage (maximum purge speed for the hotend's temperature):
    maxPrintSpeed = (max(1, temperatureAdjustedToFlow(filament, hotend, layerHeight, speed) - getTemperature(hotend, filament, 'lowTemperature'))/float(max(1, getTemperature(hotend, filament, 'highTemperature')-getTemperature(hotend, filament, 'lowTemperature')))) * maxFlowValue(hotend, filament, layerHeight) / (hotend['nozzleSize']*layerHeight/60.)
    F = float("%.2f" % (maxPrintSpeed * hotend['nozzleSize'] * layerHeight / (math.pi * (filament['filamentDiameter']/2.)**2)))

    # S - Slope of the SmartPurge function (according to NSize, Flow, PurgeLength)
    distanceAtNozzleTip = hotendPurgeMultiplier * filament['purgeLength'] * filament['extrusionMultiplier']
    slopeCorrection = 0.005 # experimental value
    S = float("%.4f" % ((distanceAtNozzleTip * (hotend['nozzleSize']/2.)**2) / ((filament['filamentDiameter']/2.)**2) * slopeCorrection))

    # E - Maximum distance to purge (according to NSize, Flow)
    if hotend['nozzleSize'] >= 0.8:
        maxPurgeLength = (6 + 16)/2. # max length to purge (highFlow)
    else:
        maxPurgeLength = (6 + 12)/2. # max length to purge (standard)
    E = float("%.2f" % (maxPurgeLength * filament['extrusionMultiplier']))
    
    # P - Minimum distance to purge 
    P = float("%.4f" % ((minPurgeLength*filament['extrusionMultiplier']*(hotend['nozzleSize']/2.)**2) / ((filament['filamentDiameter']/2.)**2)))
    
    # P (testing value)
    P = toolChangePurgeLength

    return (startPurgeLength, toolChangePurgeLength, F, S, E, P)

def retractValues(filament):
    if filament['isFlexibleMaterial']:
        useCoasting = 0
        useWipe = 1
        onlyRetractWhenCrossingOutline = 1
        retractBetweenLayers = 0
        useRetractionMinTravel = 1
        retractWhileWiping = 1
        onlyWipeOutlines = 1
    else:
        useCoasting = 0
        useWipe = 1
        onlyRetractWhenCrossingOutline = 0
        retractBetweenLayers = 0
        useRetractionMinTravel = 1
        retractWhileWiping = 1
        onlyWipeOutlines = 1
    return useCoasting, useWipe, onlyRetractWhenCrossingOutline, retractBetweenLayers, useRetractionMinTravel, retractWhileWiping, onlyWipeOutlines

def coastVolume(hotend, filament):
    return float("%.2f" % ((hotend['nozzleSize'])**3*filament['purgeLength']/16))

def maxFlowValue(hotend, filament, layerHeight):
    if hotend['nozzleSize'] <= 0.6:
        if filament['maxFlow'] == 'None':
            return hotend['nozzleSize']*layerHeight*filament['advisedMaxPrintSpeed']
        else:
            return filament['maxFlow']
    else:
        if filament['maxFlowForHighFlowHotend'] == 'None':
            if filament['maxFlow'] == 'None':
                return hotend['nozzleSize']*layerHeight*filament['advisedMaxPrintSpeed']
            else:
                return filament['maxFlow']
        else:
            return filament['maxFlowForHighFlowHotend']

def getTemperature(hotend, filament, temperatureToAdjust):
    if temperatureToAdjust == "lowTemperature":
        adjustedTemperature = filament['printTemperature'][0] + hotend['temperatureCompensation']
    elif temperatureToAdjust == "highTemperature":
        adjustedTemperature = filament['printTemperature'][1] + hotend['temperatureCompensation']
    elif temperatureToAdjust == "standbyTemperature":
        adjustedTemperature = filament['standbyTemperature'] + hotend['temperatureCompensation']
    return adjustedTemperature

def defaultMaterialPrintTemperature(filament):
    # Exclusive function for Cura 2 to get default_material_print_temperature
    return int(round((filament['printTemperature'][0] + filament['printTemperature'][1])/2.))

def temperatureAdjustedToFlow(filament, hotend, layerHeight, speed, base = 5):
    # adaptative temperature according to flow values. Rounded to base
    flow = hotend['nozzleSize']*layerHeight*float(speed)/60

    # Warning if something is not working properly
    if int(flow) > int(maxFlowValue(hotend, filament, layerHeight)):
        print "\nwarning! you're trying to print at higher flow than allowed:", filament['id']+':', str(int(flow)), str(int(maxFlowValue(hotend, filament, layerHeight)))

    temperature = int(base * round((getTemperature(hotend, filament, 'lowTemperature') + flow/maxFlowValue(hotend, filament, layerHeight) * float(getTemperature(hotend, filament, 'highTemperature')-getTemperature(hotend, filament, 'lowTemperature')))/float(base)))
    return temperature

def fanSpeed(hotend, filament, temperature, layerHeight, base = 5):
    # adaptative fan speed according to temperature values. Rounded to base
    if getTemperature(hotend, filament, 'highTemperature') - getTemperature(hotend, filament, 'lowTemperature') == 0 or filament['fanPercentage'][1] == 0:
        fanSpeed = filament['fanPercentage'][0]
    else:
        fanSpeedForTemperature = int(base * round((filament['fanPercentage'][0] + (temperature-getTemperature(hotend, filament, 'lowTemperature'))/float(getTemperature(hotend, filament, 'highTemperature')-getTemperature(hotend, filament, 'lowTemperature'))*float(filament['fanPercentage'][1]-filament['fanPercentage'][0]))/float(base)))
        LayerHeightAtMaxFanSpeed = 0.025
        LayerHeightAtMinFanSpeed = 0.2
        fanSpeedForLayerHeight = int(base * round((filament['fanPercentage'][0] + (layerHeight - LayerHeightAtMaxFanSpeed)/float(LayerHeightAtMinFanSpeed-LayerHeightAtMaxFanSpeed)*float(filament['fanPercentage'][1]-filament['fanPercentage'][0]))/float(base)))
        fanSpeed = max(fanSpeedForTemperature, fanSpeedForLayerHeight)
    return min(fanSpeed, 100) # Repassar. Aquest 100 no hauria de ser necessari

def timeVsTemperature(element, value, command):

    # bed heating curve parameters
    bedParameterA1 = 51
    bedParameterA2 = 61
    bedParameterA3 = 19
    bedParameterB1 = 1000
    bedParameterB2 = 90
    bedParameterB3 = 47
    bedParameterB4 = 10

    # return needed time (sec) to reach Temperature (ºC)
    if command == 'getTime':
        temperature = value
        if element['id'] == 'bed':
            if temperature <= 60:
                time = bedParameterA1 * math.log(-(bedParameterA2-bedParameterA3)/(float(temperature)-bedParameterA2))
            else:
                time = bedParameterB1 * math.log(-bedParameterB2/(float(temperature)-bedParameterB2-bedParameterB3))+bedParameterB4
        else:
            time = temperature / float(element['heatUpSpeed'])
        return max(0, time)

    # return temperature (ºC) reached after heating during given time (sec)
    elif command == 'getTemperature':
        time = value
        if element['id'] == 'bed':
            if time <= 180:
                temperature = bedParameterA2 - (bedParameterA2 - bedParameterA3) * math.exp(-time/bedParameterA1)
            else:
                temperature = bedParameterB2 + bedParameterB3 - bedParameterB2 * math.exp(-(time - bedParameterB4)/bedParameterB1)
        else:
            temperature = time * element['heatUpSpeed']
        return max(0, temperature)

def firstHeatSequence(hotendLeft, hotendRight, leftHotendTemp, rightHotendTemp, bedTemp, software):
    startSequenceString = '; Start Heating Sequence. If you changed temperatures manually all elements may not heat in sync,'
    bed = dict([('id', 'bed')])
    if software == 'Simplify3D':
        if hotendLeft['id'] != 'None':
            timeLeftHotend  = (timeVsTemperature(hotendLeft, leftHotendTemp, 'getTime'), '', hotendLeft, 'M104 ', 'M109 ', 'S[extruder0_temperature]', ' T0,')
        if hotendRight['id'] != 'None':
            timeRightHotend = (timeVsTemperature(hotendRight, rightHotendTemp, 'getTime'), '', hotendRight, 'M104 ', 'M109 ', 'S[extruder1_temperature]', ' T1,')
        timeBed         = (timeVsTemperature(bed, bedTemp, 'getTime'), '', bed, 'M140 ', 'M190 ', 'S[bed0_temperature]',       ',')
    elif software == 'Cura':
        startSequenceString = '\t;' + startSequenceString[2:-1] + '\n'
        if hotendLeft['id'] != 'None':
            timeLeftHotend  = (timeVsTemperature(hotendLeft, leftHotendTemp, 'getTime'), '\t', hotendLeft, 'M104 ', 'M109 ', 'S{print_temperature}',     ' T0\n')
        if hotendRight['id'] != 'None':
            timeRightHotend = (timeVsTemperature(hotendRight, rightHotendTemp, 'getTime'), '\t', hotendRight, 'M104 ', 'M109 ', 'S{print_temperature2}',    ' T1\n')
        timeBed         = (timeVsTemperature(bed, bedTemp, 'getTime'), '\t', bed, 'M140 ', 'M190 ', 'S{print_bed_temperature}', '\n')
    elif software == 'Cura2':
        # Using Cura 2.5.0 the only labels we know to point to extruder being used are:
        #   adhesion_extruder_nr
        #   support_infill_extruder_nr
        #   support_extruder_nr
        #   support_interface_extruder_nr
        startSequenceString = r'\n;' + startSequenceString[2:-1] + r'\n'
        if hotendLeft['id'] != 'None':
            timeLeftHotend  = (timeVsTemperature(hotendLeft, leftHotendTemp, 'getTime'), '', hotendLeft, 'M104 ', 'M109 ', 'S{material_print_temperature_layer_0}',     r' T0\n')
        if hotendRight['id'] != 'None':
            timeRightHotend = (timeVsTemperature(hotendRight, rightHotendTemp, 'getTime'), '', hotendRight, 'M104 ', 'M109 ', 'S{material_print_temperature_layer_0}',    r' T1\n')
        timeBed         = (timeVsTemperature(bed, bedTemp, 'getTime'), '', bed, 'M140 ', 'M190 ', 'S{material_bed_temperature}', r'\n')

    if hotendLeft['id'] != 'None' and hotendRight['id'] != 'None':
        # IDEX
        startTimes = sorted([timeLeftHotend, timeRightHotend, timeBed])
        startSequenceString += startTimes[-1][-6]+startTimes[-1][-3]+'S'+str(int(timeVsTemperature(startTimes[-1][-5], startTimes[-1][0]-startTimes[-2][0], 'getTemperature')))+startTimes[-1][-1]
        startSequenceString += startTimes[-1][-6]+startTimes[-2][-4]+startTimes[-2][-2]+startTimes[-2][-1]
        startSequenceString += startTimes[-1][-6]+startTimes[-1][-3]+'S'+str(int(timeVsTemperature(startTimes[-1][-5], startTimes[-1][0]-startTimes[-3][0], 'getTemperature')))+startTimes[-1][-1]
        startSequenceString += startTimes[-1][-6]+startTimes[-3][-4]+startTimes[-3][-2]+startTimes[-3][-1]
        startSequenceString += startTimes[-1][-6]+startTimes[-1][-3]+startTimes[-1][-2]+startTimes[-1][-1]
        startSequenceString += startTimes[-1][-6]+startTimes[-2][-3]+startTimes[-2][-2]+startTimes[-2][-1]
        startSequenceString += startTimes[-1][-6]+startTimes[-3][-3]+startTimes[-3][-2]+startTimes[-3][-1]
    else:
        if hotendRight['id'] == 'None':
            # MEX Left
            startTimes = sorted([timeLeftHotend, timeBed])
            startSequenceString += startTimes[-1][-6]+startTimes[-1][-3]+'S'+str(int(timeVsTemperature(startTimes[-1][-5], startTimes[-1][0]-startTimes[-2][0], 'getTemperature')))+startTimes[-1][-1][-1:]
            startSequenceString += startTimes[-1][-6]+startTimes[-2][-4]+startTimes[-2][-2]+startTimes[-2][-1][-1:]
            startSequenceString += startTimes[-1][-6]+startTimes[-1][-3]+startTimes[-1][-2]+startTimes[-1][-1][-1:]
            startSequenceString += startTimes[-1][-6]+startTimes[-2][-3]+startTimes[-2][-2]+startTimes[-2][-1][-1:]
        else:
            # MEX Right
            startTimes = sorted([timeRightHotend, timeBed])
            startSequenceString += startTimes[-1][-6]+startTimes[-1][-3]+'S'+str(int(timeVsTemperature(startTimes[-1][-5], startTimes[-1][0]-startTimes[-2][0], 'getTemperature')))+startTimes[-1][-1][-1:]
            startSequenceString += startTimes[-1][-6]+startTimes[-2][-4]+startTimes[-2][-2]+startTimes[-2][-1][-1:]
            startSequenceString += startTimes[-1][-6]+startTimes[-1][-3]+startTimes[-1][-2]+startTimes[-1][-1][-1:]
            startSequenceString += startTimes[-1][-6]+startTimes[-2][-3]+startTimes[-2][-2]+startTimes[-2][-1][-1:]
    return startSequenceString

def accelerationForPerimeters(nozzleSize, layerHeight, outerWallSpeed, base = 5, multiplier = 30000, defaultAcceleration = 2000):
    return min(defaultAcceleration, int(base * round((nozzleSize * layerHeight * multiplier * 1/(outerWallSpeed**(1/2.)))/float(base))))

def speedMultiplier(hotend, filament):
    if filament['isFlexibleMaterial']:
        return float(filament['defaultPrintSpeed'])/24*hotend['nozzleSize']
        # 24*hotend['nozzleSize'] -> experimental value that works better with flexibles
    else:
        return float(filament['defaultPrintSpeed'])/60
        # 60 -> speed for base material (PLA) at base quality (Standard)

def speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, layerHeight, firstLayerHeight, infillLayerInterval, quality, action):
    if action == 'MEX Left' or action == 'IDEX, Infill with Right' or action == 'IDEX, Supports with Right':
        primaryHotend = hotendLeft
        primaryFilament = filamentLeft
        secondaryHotend = hotendRight
        secondaryFilament = filamentRight
    elif action == 'MEX Right' or action == 'IDEX, Infill with Left' or action == 'IDEX, Supports with Left':
        primaryHotend = hotendRight
        primaryFilament = filamentRight
        secondaryHotend = hotendLeft
        secondaryFilament = filamentLeft

    primaryExtruderDefaultSpeed = quality['defaultSpeed']*speedMultiplier(primaryHotend, primaryFilament)
    primaryExtruderMaxSpeed = maxFlowValue(primaryHotend, primaryFilament, layerHeight)/(primaryHotend['nozzleSize']*layerHeight)
    firstLayerPrimaryExtruderMaxSpeed = maxFlowValue(primaryHotend, primaryFilament, firstLayerHeight)/(primaryHotend['nozzleSize']*firstLayerHeight)

    if 'MEX' in action:
        defaultSpeed = int(str(float(min(primaryExtruderDefaultSpeed, primaryExtruderMaxSpeed, primaryFilament['advisedMaxPrintSpeed']))).split('.')[0])
    else:
        secondaryExtruderMaxSpeed = maxFlowValue(secondaryHotend, secondaryFilament, infillLayerInterval*layerHeight)/(infillLayerInterval*layerHeight*secondaryHotend['nozzleSize'])
        defaultSpeed = int(str(float(min(primaryExtruderDefaultSpeed, primaryExtruderMaxSpeed, secondaryExtruderMaxSpeed, primaryFilament['advisedMaxPrintSpeed'], secondaryFilament['advisedMaxPrintSpeed']))).split('.')[0])

    maxAllowedSpeedMultiplier = primaryExtruderMaxSpeed / float(defaultSpeed)
    firstLayerMaxAllowedSpeedMultiplier = firstLayerPrimaryExtruderMaxSpeed / float(defaultSpeed)

    if primaryFilament['isFlexibleMaterial']:
        outlineUnderspeed = 1.00
    else:
        defaulOulineMultiplier =      primaryExtruderDefaultSpeed*quality['outlineUnderspeed']    /float(defaultSpeed)
        outlineUnderspeed    = float("%.2f" % min(maxAllowedSpeedMultiplier, defaulOulineMultiplier))

    defaultFirstLayerMultiplier = primaryExtruderDefaultSpeed*quality['firstLayerUnderspeed'] /float(defaultSpeed)

    if 'IDEX, Supports with' in action:
        maxAllowedSupportMultiplier = secondaryExtruderMaxSpeed / float(defaultSpeed)
        supportUnderspeed    = float("%.2f" % min(maxAllowedSpeedMultiplier, maxAllowedSupportMultiplier))
        firstLayerSecondaryExtruderMaxSpeed = maxFlowValue(secondaryHotend, secondaryFilament, firstLayerHeight)/(firstLayerHeight*secondaryHotend['nozzleSize'])
        firstLayerSecondaryExtruderMaxAllowedSpeedMultiplier = firstLayerSecondaryExtruderMaxSpeed / float(defaultSpeed)
        firstLayerUnderspeed = float("%.2f" % min(firstLayerMaxAllowedSpeedMultiplier, firstLayerSecondaryExtruderMaxAllowedSpeedMultiplier, defaultFirstLayerMultiplier))
    else:
        supportUnderspeedMultiplier = primaryExtruderDefaultSpeed*0.9 / float(defaultSpeed)
        supportUnderspeed    = float("%.2f" % min(maxAllowedSpeedMultiplier, supportUnderspeedMultiplier))        
        firstLayerUnderspeed = float("%.2f" % min(firstLayerMaxAllowedSpeedMultiplier, defaultFirstLayerMultiplier))

    return defaultSpeed*60, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed