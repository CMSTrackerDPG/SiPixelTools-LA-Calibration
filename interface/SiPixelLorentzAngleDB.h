#ifndef CalibTracker_SiPixelLorentzAngleDB_SiPixelLorentzAngleDB_h
#define CalibTracker_SiPixelLorentzAngleDB_SiPixelLorentzAngleDB_h

#include <map>

#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "Geometry/TrackerGeometryBuilder/interface/TrackerGeometry.h"
#include "Geometry/Records/interface/TrackerDigiGeometryRecord.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/DetId/interface/DetId.h"

// Magnetic field
#include "MagneticField/Engine/interface/MagneticField.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"

// #include "CalibTracker/SiStripLorentzAngle/interface/SiStripLorentzAngleAlgorithm.h"

class SiPixelLorentzAngleDB : public edm::one::EDAnalyzer<>
{
 public:
  
  explicit SiPixelLorentzAngleDB(const edm::ParameterSet& conf);
  
  virtual ~SiPixelLorentzAngleDB();
  
  //  virtual void beginJob(const edm::EventSetup& c);

  virtual void beginJob();
  
  virtual void endJob(); 
  
  virtual void analyze(const edm::Event& e, const edm::EventSetup& c);
  
  
 private:

  std::vector< std::pair<uint32_t, float> > detid_la;
  edm::ParameterSet conf_;
  double magneticField_;
  std::string recordName_;
  float bPixLorentzAnglePerTesla_;
  float fPixLorentzAnglePerTesla_;
  std::string fileName_;
  bool useFile_;
  const edm::ESGetToken<TrackerGeometry, TrackerDigiGeometryRecord> tkGeomToken_;
};


#endif
