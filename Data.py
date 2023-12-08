XMLRunMonitoringTemplate='''<?xml version="1.0" encoding="utf-8"?>
<!-- ITxPT S02P06 AVMS service - Run Monitoring operation XML Example -->
<RunMonitoringDelivery version="2.2.1">
  <MonitoredRunState>
    <RecordedAtTime>2019-10-24T12:12:12</RecordedAtTime>
    <MonitoredBlockRef>9301</MonitoredBlockRef>
    <CurrentRunInfo>
      <RunState>RunPattern</RunState>
      <PatternRunType>ServiceJourneyPattern</PatternRunType>
      <JourneyPatternRef>9308</JourneyPatternRef>
      <VehicleJourneyRef>930110</VehicleJourneyRef>
    </CurrentRunInfo>
    <RunningPatternState>OnDiversion</RunningPatternState>
    <NextRunInfo>
      <RunState>RunToPattern</RunState>
      <PatternRunType>ServiceJourneyPattern</PatternRunType>
      <JourneyPatternRef>9311</JourneyPatternRef>
      <VehicleJourneyRef>930111</VehicleJourneyRef>
    </NextRunInfo>
    <MonitoredRunStateNote>Note</MonitoredRunStateNote>
  </MonitoredRunState>
</RunMonitoringDelivery>'''

XMLPlannedPatternTemplate= """<?xml version="1.0" encoding="utf-8"?>
<!-- ITxPT S02P06 AVMS service - Planned Pattern operation XML Example -->
<PlannedPatternDelivery version="2.2.1">
  <PlannedPattern>
    <RecordedAtTime>2019-10-24T12:12:12</RecordedAtTime>
    <PatternRef>9308</PatternRef>
    <VehicleJourneyRef>1234</VehicleJourneyRef>
    <OperatingDayDate>2012-12-13</OperatingDayDate>
    <RouteRef>10</RouteRef>
    <LineRef>93</LineRef>
    <PublishedLineLabel>Teor 3</PublishedLineLabel>
    <PublishedTtsLineLabel>Teor 3</PublishedTtsLineLabel>
    <DirectionRef>123</DirectionRef>
    <ExternalLineRef>T3</ExternalLineRef>
    <OriginName>Bizet</OriginName>
    <OriginShortName>Bizet</OriginShortName>
    <OriginLongName>Bizet</OriginLongName>
    <OriginTtsName>BIZÃ©T</OriginTtsName>
    <Via>
      <PlaceRef>11525</PlaceRef>
      <PlaceName language="fre">Eglise St-Jean</PlaceName>
      <PlaceName language="eng">St-Jean church</PlaceName>
    </Via>
    <DestinationPlaceRef>12180</DestinationPlaceRef>
    <DestinationName>Durecu-Lavoisier</DestinationName>
    <DestinationShortName>Durecu-Lavoisier</DestinationShortName>
    <DestinationLongName>Durecu-Lavoisier</DestinationLongName>
    <DestinationTtsName>DURÃ©CU-LAVOISIER</DestinationTtsName>
    <PatternStops>
      <PatternStop>
        <StopPointRef>10164</StopPointRef>
        <Order>1</Order>
        <StopPointName>Bizet</StopPointName>
        <StopPointShortName>Bizet</StopPointShortName>
        <StopPointLongName>Bizet</StopPointLongName>
        <StopPointTtsName>BIZÃ©T</StopPointTtsName>
      </PatternStop>
      <PatternStop>
        <StopPointRef>11524</StopPointRef>
        <Order>2</Order>
        <StopPointName language="fre">Eglise St-Jean</StopPointName>
        <StopPointName language="eng">St-Jean church</StopPointName>
        <StopPointShortName>Eglise St-Jean</StopPointShortName>
        <StopPointLongName>Eglise St-Jean</StopPointLongName>
        <StopPointTtsName>EGLISE SAINT-JEAN</StopPointTtsName>
      </PatternStop>
<!-- […] -->
      <PatternStop>
        <StopPointRef>12180</StopPointRef>
        <Order>2</Order>
        <StopPointName>Durecu-Lavoisier</StopPointName>
        <StopPointShortName>Durecu-Lavoisier</StopPointShortName>
        <StopPointLongName>Durecu-Lavoisier</StopPointLongName>
        <StopPointTtsName>DURÃ©CU-LAVOISIER</StopPointTtsName>
      </PatternStop>
    </PatternStops>
    <PlannedPatternNote>Note</PlannedPatternNote>
  </PlannedPattern>
</PlannedPatternDelivery>
"""

XMLVehicleMonitoringTemplate= """<?xml version="1.0" encoding="utf-8"?>
<!-- ITxPT S02P06 AVMS service - Vehicle Monitoring operation XML Example -->
<VehicleMonitoringDelivery version="2.2.1">
  <VehicleActivity>
    <RecordedAtTime>2019-10-24T12:12:12</RecordedAtTime>
    <ItemIdentifier>9</ItemIdentifier>
    <JourneyPatternRef>9311</JourneyPatternRef>
    <VehicleJourneyRef>1234</VehicleJourneyRef>
    <ProgressBetweenStops>
      <PreviousCallRef>
        <StopPointRef>12159</StopPointRef>
        <Order>7</Order>
      </PreviousCallRef>
      <MonitoredCallRef>
        <StopPointRef>11759</StopPointRef>
        <Order>8</Order>
        <VehicleAtStop>true</VehicleAtStop>
      </MonitoredCallRef>
      <LinkDistance>123.45</LinkDistance>
      <Percentage>98.12</Percentage>
    </ProgressBetweenStops>
    <VehicleActivityNote>Note</VehicleActivityNote>
  </VehicleActivity>
  <VehicleActivityCancellation>
    <RecordedAtTime>2019-10-24T12:12:12</RecordedAtTime>
    <ItemIdentifier>9310</ItemIdentifier>
    <PatternRef>123</PatternRef>
    <Reason>Reason</Reason>
  </VehicleActivityCancellation> 
</VehicleMonitoringDelivery>
"""

XMLJourneyMonitoringTemplate = """<JourneyMonitoringDelivery version="2.2.1">
  <!-- ITxPT S02P06 AVMS service - Journey Monitoring operation XML Example -->
  <MonitoredJourney>
    <RecordedAtTime>2019-10-24T12:12:12</RecordedAtTime>
    <ItemIdentifier>2</ItemIdentifier>
    <PatternRef>9311</PatternRef>
    <JourneyRef>9</JourneyRef>
    <VehicleJourneyRef>9310</VehicleJourneyRef>
    <JourneyNote>Note</JourneyNote>
    <HeadwayService>true</HeadwayService>
    <OriginPlannedDepartureTime>2019-10-24T12:10:00</OriginPlannedDepartureTime>
    <DestinationPlannedArrivalTime>2019-10-24T12:20:12</DestinationPlannedArrivalTime>
    <InCongestion>true</InCongestion>
    <InPanic>true</InPanic>
    <ProgressRate>slowProgress</ProgressRate>
    <Occupancy>full</Occupancy>
    <Delay>340</Delay>
    <ProgressStatus>str1234</ProgressStatus>
    <ProductCategoryRef>str1234</ProductCategoryRef>
    <ServiceFeatureRef>str1234</ServiceFeatureRef>
    <VehicleFeatureRef>str1234</VehicleFeatureRef>
    <PreviousCalls>
      <PreviousCall>
        <StopPointRef>12180</StopPointRef>
        <Order>1</Order>
        <ActualArrivalTime>2019-10-24T12:10:12</ActualArrivalTime>
        <ActualDepartureTime>2019-10-24T12:12:12</ActualDepartureTime>
      </PreviousCall>
    </PreviousCalls>
    <MonitoredCall>
      <StopPointRef>12157</StopPointRef>
      <Order>9</Order>
      <VehicleAtStop>false</VehicleAtStop>
      <PlannedArrivalTime>2019-10-24T12:25:00</PlannedArrivalTime>
      <ExpectedArrivalTime>2019-10-24T12:30:00</ExpectedArrivalTime>
      <PlannedDepartureTime>2019-10-24T12:51:12</PlannedDepartureTime>
      <ExpectedDepartureTime>2019-10-24T12:12:12</ExpectedDepartureTime>
    </MonitoredCall>
    <OnwardCalls>
      <OnwardCall>
        <StopPointRef>12157</StopPointRef>
        <Order>10</Order>
        <PlannedArrivalTime>2019-10-24T12:25:00</PlannedArrivalTime>
        <ExpectedArrivalTime>2019-10-24T12:30:00</ExpectedArrivalTime>
        <PlannedDepartureTime>2019-10-24T12:51:12</PlannedDepartureTime>
        <ExpectedDepartureTime>2019-10-24T12:12:12</ExpectedDepartureTime>
      </OnwardCall>
      <!-- […] -->
      <OnwardCall>
        <StopPointRef>10164</StopPointRef>
        <Order>31</Order>
        <PlannedArrivalTime>2019-10-24T12:25:00</PlannedArrivalTime>
        <ExpectedArrivalTime>2019-10-24T12:30:00</ExpectedArrivalTime>
        <PlannedDepartureTime>2019-10-24T12:51:12</PlannedDepartureTime>
        <ExpectedDepartureTime>2019-10-24T12:12:12</ExpectedDepartureTime>
      </OnwardCall>
    </OnwardCalls>
  </MonitoredJourney>
  <MonitoredJourneyCancellation>
    <RecordedAtTime>2019-10-24T12:12:12</RecordedAtTime>
    <ItemIdentifier>1</ItemIdentifier>
    <PatternRef>9309</PatternRef>
    <JourneyRef>9</JourneyRef> 
    <Reason>Reason</Reason>
  </MonitoredJourneyCancellation>
</JourneyMonitoringDelivery>"""

GNSSLocationDeliveryTemplate = """<?xml version="1.0" encoding="utf-8"?>

<!-- ITxPT S02P03 GNSSLocation service - GNSSLocation Delivery XML Example -->

<GNSSLocationDelivery version="2.2.1">
  <GNSSLocation>
    <Data>$GPRMC,080530.526,A,4852.655,N,00220.337,E,,,241019,000.0,W*70</Data>  
    <Latitude>
      <Degree>48.877583</Degree>
      <Direction>N</Direction>
    </Latitude>
    <Longitude>
      <Degree>2.338950</Degree>
      <Direction>E</Direction>
    </Longitude>
    <Altitude>12</Altitude>
    <Time>08:05:30</Time>
    <Date>2019-10-24</Date>
    <SpeedOverGround>11.52356</SpeedOverGround>
    <SignalQuality>aGPS</SignalQuality>
    <Fix>3D</Fix>
    <NumberOfSatellites>7</NumberOfSatellites>
    <HorizontalDilutionOfPrecision>10.01</HorizontalDilutionOfPrecision>
    <VerticalDilutionOfPrecision>21.3</VerticalDilutionOfPrecision>
    <TrackDegreeTrue>91.2</TrackDegreeTrue>
    <TrackDegreeMagnetic>91.0</TrackDegreeMagnetic>
    <GNSSType>GPS</GNSSType>
    <GNSSCoordinateSystem>WGS84</GNSSCoordinateSystem>
  </GNSSLocation>
  <Extensions />
</GNSSLocationDelivery>"""