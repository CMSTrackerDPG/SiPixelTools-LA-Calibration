import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run2_2018_cff import Run2_2018

process = cms.Process("LA", Run2_2018)

process.load('Configuration.StandardSequences.Services_cff')

#process.load("Configuration.StandardSequences.Geometry_cff")
#process.load('Configuration/StandardSequences/GeometryExtended_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')

#process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration/StandardSequences/MagneticField_AutoFromDBCurrent_cff')

# process.load("Configuration.StandardSequences.FakeConditions_cff")

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
# check for the correct tag on https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions
#process.GlobalTag.globaltag = "GR09_PV7::All"
process.GlobalTag.globaltag = "112X_dataRun2_v7"


process.load("RecoTracker.Configuration.RecoTracker_cff")

process.load("RecoVertex.BeamSpotProducer.BeamSpot_cff")
from RecoVertex.BeamSpotProducer.BeamSpot_cff import *
process.offlineBeamSpot = offlineBeamSpot 


#process.load("RecoTracker/TrackProducer/TrackRefitters_cff")

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
process.TrackRefitter.src = 'ALCARECOSiPixelCalSingleMuon'
process.TrackRefitter.TrajectoryInEvent = True


process.MessageLogger = cms.Service("MessageLogger",
    destinations = cms.untracked.vstring('simul', 
        'cout'),
    simul = cms.untracked.PSet(
        threshold = cms.untracked.string('ERROR')
    ),
)

process.lorentzAngle = cms.EDAnalyzer("SiPixelLorentzAngle",
	src = cms.string("TrackRefitter"),
	fileName = cms.string("lorentzangle.root"),
	fileNameFit	= cms.string("lorentzFit.txt"),
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

process.myout = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('LA_CMSSW.root')
)

process.p = cms.Path(process.offlineBeamSpot*
                     process.MeasurementTrackerEvent*
                     process.TrackRefitter*
                     process.lorentzAngle)

# uncomment this if you want to write out the new CMSSW root file (very large)
# process.outpath = cms.EndPath(process.myout)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

process.source = cms.Source("PoolSource",
	#put here the sample you want to use
    fileNames = cms.untracked.vstring('file:/uscms/home/wwei/nobackup/LA/CMSSW_11_2_0_pre10/src/SiPixelCalSingleMuon.root'
    #put your source file here
	  # ' '
	),

#   skipEvents = cms.untracked.uint32(100)
#
)
