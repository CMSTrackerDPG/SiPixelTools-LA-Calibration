# cmsRun test.py outName=testrun.root outNameFit=testrun.txt maxEvents=10 inputFiles=/store/data/Run2018C/SingleMuon/ALCARECO/SiPixelCalSingleMuon-ForPixelALCARECO_UL2018-v1/00000/698BAF88-2250-894B-A47B-88749735A6CC.root

import FWCore.ParameterSet.Config as cms
import sys
import os

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')
options.register( "outName", "lorentzangle.root", VarParsing.multiplicity.singleton, VarParsing.varType.string, "name and path of the output files (without extension)" )
options.register( "outNameFit", "lorentzFit.txt", VarParsing.multiplicity.singleton, VarParsing.varType.string, "name and path of the output files (without extension)" )
#options.register( "maxEvents", -1, VarParsing.multiplicity.singleton, VarParsing.varType.int, "maximum events" )
options.parseArguments()

#if options.maxEvents is -1: # maxEvents is set in VarParsing class by default to -1
#    options.maxEvents = 100

from Configuration.Eras.Era_Run2_2018_cff import Run2_2018

process = cms.Process("LA", Run2_2018)
process.load('Configuration.StandardSequences.Services_cff')
#process.load("Configuration.StandardSequences.Geometry_cff")
#process.load('Configuration/StandardSequences/GeometryExtended_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
#process.load('Configuration/StandardSequences/MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
# process.load("Configuration.StandardSequences.FakeConditions_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
# check for the correct tag on https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions
#process.GlobalTag.globaltag = "GR09_PV7::All"
process.GlobalTag.globaltag = "112X_dataRun2_v7"


process.load("RecoTracker.Configuration.RecoTracker_cff")
process.load("RecoVertex.BeamSpotProducer.BeamSpot_cff")
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideFindingBeamSpot
from RecoVertex.BeamSpotProducer.BeamSpot_cff import *
process.offlineBeamSpot = offlineBeamSpot

process.load("RecoTracker.TrackProducer.TrackRefitters_cff")
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.load("RecoTracker.MeasurementDet.MeasurementTrackerEventProducer_cfi")

process.MeasurementTrackerEvent.pixelClusterProducer = 'ALCARECOSiPixelCalSingleMuon'
process.MeasurementTrackerEvent.stripClusterProducer = 'ALCARECOSiPixelCalSingleMuon'
process.MeasurementTrackerEvent.inactivePixelDetectorLabels = cms.VInputTag()
process.MeasurementTrackerEvent.inactiveStripDetectorLabels = cms.VInputTag()


process.load("RecoTracker.TransientTrackingRecHit.TransientTrackingRecHitBuilderWithoutRefit_cfi")
# put here the tag of the tracks you want to use
# alcareco samples have special names for the tracks, in normal reco samples generalTracks can be used
#process.TrackRefitter.src = "generalTracks"
#process.TrackRefitter.src = "ALCARECOTkAlZMuMu"

# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideTrackRecoSequences#RefTr
# Some use-cases require performing a new Final Fit over already reconstructed Tracks. For examples, for alignment studies, you can refit Tracks after having modified the geometry of detectors. Refitting tracks is also useful if you need access to their Trajectory.
# We use the same geometry, so we just want ot access the trajectory
# The TrackRefitter class is responsible for this task: it takes as input a collection of reco::Tracks, and puts into the event a new TrackCollection containing refitted Tracks.

# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideTransientTracks
# A TransientTracks has a pointer to the magnetic field, and can be given a pointer to the geometry as well.

process.TrackRefitter.src = 'ALCARECOSiPixelCalSingleMuon'
process.TrackRefitter.TrajectoryInEvent = True

process.MessageLogger = cms.Service("MessageLogger",
    destinations = cms.untracked.vstring('simul', 
        'cout'),
    simul = cms.untracked.PSet(
        threshold = cms.untracked.string('ERROR')
    ),
)
#SiPixelLorentzAngle

#from SiPixelTools.LA-Calibration.SiPixelLorentzAngle_cfi import *
process.lorentzAngle = cms.EDAnalyzer("SiPixelLorentzAngle",
	src = cms.string("TrackRefitter"),
	fileName = cms.string(options.outName),
#    fileName = cms.string("lorentzangle.root"),
	fileNameFit	= cms.string(options.outNameFit),
#    fileNameFit    = cms.string("lorentzFit.txt"),
	binsDepth	= cms.int32(50),
	binsDrift =	cms.int32(200),
	ptMin = cms.double(3),
	#in case of MC set this to true to save the simhits (does not work currently, Mixing Module needs to be included correctly)
	simData = cms.bool(False),
  	normChi2Max = cms.double(2),
	clustSizeYMin = cms.int32(4),
	residualMax = cms.double(0.005),
	clustChargeMax = cms.double(120000)
)

#process.myout = cms.OutputModule("PoolOutputModule",
#    fileName = cms.untracked.string('LA_CMSSW.root')
#)

process.p = cms.Path(process.offlineBeamSpot*
                     process.MeasurementTrackerEvent*
                     process.TrackRefitter*
                     process.lorentzAngle)
                     
#process.p = cms.EndPath(process.myout)

# uncomment this if you want to write out the new CMSSW root file (very large)
# process.outpath = cms.EndPath(process.myout)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(int(options.maxEvents))
)

process.options.numberOfThreads=cms.untracked.uint32(8)

#process.options.numberOfThreads=cms.untracked.uint32(2)

process.source = cms.Source("PoolSource",
	#put here the sample you want to use
#    fileNames = cms.untracked.vstring('file:/uscms/home/wwei/nobackup/LA/CMSSW_11_2_0_pre10/src/trial2/SiPixelCalSingleMuon_1.root'),
    fileNames = cms.untracked.vstring(options.inputFiles),
#   skipEvents = cms.untracked.uint32(100)
#
)
