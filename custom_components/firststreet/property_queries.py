# property_queries.py

PROPERTY_BY_FSID_QUERY = """
query PropertyByFSID($fsid: Int64!, $buildingId: [Int!]) {
  property(fsid: $fsid) {
    flood {
      floodType
      link
      exclusion {
        description
      }
      floodFactor
      riskDirection
      probability {
        cumulative(depths: [5, 15, 30, 61, 91, 122, 152, 183, 213, 244, 274, 305, 335, 366, 396, 427, 457, 488, 518, 549, 579, 610]) {
          threshold
          relativeYear
          mid
          yAxisHeightMid
        }
        depth {
          returnPeriod
          relativeYear
          low
          mid
          high
        }
        depthMean: depth(filter: {depthFlavor: MEAN}) {
          returnPeriod
          relativeYear
          low
          mid
          high
        }
      }
      insuranceRequirement
      insuranceQuotes {
        rates {
          providers
          minPrice
          maxPrice
          link
        }
      }
      historic {
        eventId
        name
        affectedProperties
        depth
        month
        year
      }
      stats {
        floodfactorRankInCity
      }
      adaptationConnection {
        totalCount
      }
      insights {
        name
        details {
          name
          value
        }
      }
    }
    fire {
      exclusion {
        description
      }
      riskDirection
      fireFactor
      defensibleSpace
      usfsRelativeRisk
      prescribedBurns: historicConnection(filter: {type: [PRESCRIBED_FIRE]}) {
        totalCount
      }
      probability {
        burn {
          emberZone
          relativeYear
          percent
          year
          flameMax
          flameMean
          flameBin
        }
        cumulative {
          year
          relativeYear
          point
          yAxisHeight
        }
      }
      historicConnection(first: 100) {
        totalCount
        edges {
          node {
            ... on PropertyFireHistoric {
              eventId
              name
              distance
              month
              year
              area
              eventAffectedProperties
            }
          }
        }
      }
      insuranceHippo {
        rates {
          providers
          minPrice
          maxPrice
          link
        }
      }
      insights {
        name
        details {
          name
          value
        }
      }
    }
    heat {
      exclusion {
        description
      }
      heatFactor
      hotTemperature
      anomalyTemperature
      temperatureAverageHigh {
        relativeYear
        mmt
      }
      cooling {
        coolingTemp
        cost
        costPerKwh
        energy
        relativeYear
      }
      heatWaves {
        hotHeatWave {
          length
          relativeYear
          probability
        }
      }
      days {
        distribution {
          relativeYear
          binLower
          days
        }
        hotDays {
          relativeYear
          days
          yAxisHeight
        }
        anomalyDays {
          relativeYear
          days
        }
        coolingDays {
          relativeYear
          days
        }
        dangerousDays {
          relativeYear
          days
        }
        healthCautionDays {
          relativeYear
          days
        }
      }
      insights {
        name
        details {
          name
          value
        }
      }
    }
    wind {
      windFactor
      factorScale
      riskDirection
      hasTornadoRisk
      hasThunderstormRisk
      hasCycloneRisk
      greatestWindRisk
      missileEnvironment
      primaryWindDirection
      probability {
        speed {
          ssp
          year
          relativeYear
          returnPeriod
          maxSpeed
          maxGust
          category {
            windCategoryId
            name
            minWindSpeed
            maxWindSpeed
          }
        }
        direction {
          ssp
          direction
          percent
        }
        cumulative(
          input: {thresholds: [50, 75, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240]}
        ) {
          ssp
          year
          relativeYear
          threshold
          probability
          yMax
          category {
            windCategoryId
            name
            minWindSpeed
            maxWindSpeed
          }
        }
      }
      historicConnection(
        first: 100
        filter: {mappedEventsOnly: true}
        sort: PROPERTIES_AFFECTED_DESC
      ) {
        pageInfo {
          hasNextPage
          endCursor
        }
        totalCount
        edges {
          node {
            ... on PropertyWindHistoricEventThunderstorm {
              eventId
              eventType
              date
              year
              damages
              injuries
              fatalities
              maxWind
            }
            ... on PropertyWindHistoricEventTornado {
              eventId
              eventType
              date
              damages
              year
              fatalities
              injuries
              geometry {
                bbox {
                  coordinates
                  type
                }
              }
              category {
                tornadoCategoryId
                rating
                isEnhanced
                name
                minWindSpeed
                maxWindSpeed
                description
              }
            }
            ... on PropertyWindHistoricEventCyclone {
              localWindSpeed
              eventId
              eventType
              windSpeed
              name
              date
              year
              geometry {
                bbox {
                  coordinates
                  type
                }
              }
              categoryAtLandfall {
                windCategoryId
                name
                minWindSpeed
                maxWindSpeed
              }
              categoryMax {
                windCategoryId
                name
                minWindSpeed
                maxWindSpeed
              }
              categoryLocality {
                windCategoryId
                name
                minWindSpeed
                maxWindSpeed
              }
              affectedProperties
              affectedPropertiesNationwide
              hasDetails
            }
          }
        }
      }
      exclusion {
        description
      }
    }
    air {
      exclusion {
        description
      }
      airFactor
      factorScale
      riskDirection
      days {
        outdoorDays {
          year
          relativeYear
          color {
            color
          }
          ozoneDays
          ozoneDaysYAxisHeight
          anthroPM25Days
          anthroPM25DaysYAxisHeight
          smokeMaxDays
          smokeMaxDaysYAxisHeight
          smokeAvgDays
          smokeAvgDaysYAxisHeight
          totalDays
          totalDaysYAxisHeight
        }
      }
      greatestRisk {
        criteriaPollutantId
        name
        description
      }
      triNearby
      triFacilityConnection {
        totalCount
        edges {
          node {
            triFacilityId
            name
            industry {
              industrySectorId
              name
            }
          }
        }
      }
      historic {
        aqi {
          year
          aqiAvg
          aqiMax
          worstDate
          criteriaPollutant {
            criteriaPollutantId
            name
            description
          }
        }
        days(filter: {colorID: 3}) {
          year
          totalDays
        }
      }
      insights {
        name
        details {
          name
          value
        }
      }
      percentile {
        national
        state
      }
    }
    buildingConnectionTotalCount: buildingConnection {
      totalCount
    }
    exclusion {
      description
    }
    fsid
    isResidential
    state {
      name
      air {
        days {
          outdoorDays {
            year
            relativeYear
            color {
              color
            }
            totalDays
          }
        }
        stats {
          worstCities {
            name
            fsid
            state {
              name
            }
            slug
          }
          bestCities {
            name
            fsid
            slug
            state {
              name
            }
          }
        }
      }
      heat {
        emissions {
          co2PerMWh
        }
      }
    }
    address {
      formattedAddress
    }
    alternativeAddresses {
      formattedAddress
    }
    femaZone
    floorElevation
    footprint
    parcelAcres
    landuseCodeId
    building {
      buildingId
      hasBasement
      units
      stories
      construction {
        combustibility
        material
      }
      roof {
        combustibility
        material
      }
      yearBuilt
      sqft
      replacementCostPerSqft
      buildingOrientation
      windDesignStandard
      airFilterId
    }
    geometry {
      center {
        coordinates
        type
      }
      polygon {
        coordinates
        type
      }
      bbox {
        coordinates
        type
      }
    }
    city {
      fsid
      name
      fire {
        communityRisk {
          riskPercentile
          score
          facilitiesCount
          facilitiesCategory {
            facilityCategoryId
            facilitiesCount
            score
            risks {
              year
              relativeYear
              facilitiesFireRisk
            }
          }
        }
      }
      flood {
        adaptationConnection {
          totalCount
        }
        communityRisk {
          riskPercentile
          score
          facilitiesCount
          facilitiesCategory {
            facilityCategoryId
            facilitiesCount
            score
            risks {
              facilitiesOperationalRisk
              facilitiesWaterRisk
              relativeYear
              year
            }
          }
        }
        historic {
          name
          eventId
          affectedProperties
          month
          year
        }
      }
      air {
        days {
          outdoorDays {
            year
            relativeYear
            color {
              color
            }
            totalDays
          }
        }
      }
    }
    county {
      fsid
      name
      isCoastal
      geometry {
        center {
          coordinates
          type
        }
        polygon {
          coordinates
          type
        }
        bbox {
          coordinates
          type
        }
      }
      air {
        days {
          outdoorDays {
            year
            relativeYear
            color {
              color
            }
            totalDays
          }
        }
        nonAttainments {
          classification
          part
          criteriaPollutant {
            criteriaPollutantId
            name
            description
          }
        }
      }
      flood {
        historic {
          eventId
          month
          year
          name
          affectedProperties
          data {
            count
            bin
          }
        }
        SoVI {
          percentile
        }
        adaptationConnection {
          totalCount
        }
        floodAdaptationConnection(first: 100, filter: {types: [6, 19, 20, 30, 32]}) {
          totalCount
          edges {
            node {
              adaptationId
              scenario
              name
              type
              serving {
                property
              }
            }
          }
        }
        communityRisk {
          riskPercentile
          score
          facilitiesCount
          facilitiesCategory {
            facilityCategoryId
            facilitiesCount
            score
            risks {
              facilitiesOperationalRisk
              facilitiesWaterRisk
              relativeYear
              year
            }
          }
        }
      }
      fire {
        prescribedBurns: historicConnection(filter: {type: [PRESCRIBED_FIRE]}) {
          totalCount
        }
        communityRisk {
          riskPercentile
          score
          facilitiesCount
          facilitiesCategory {
            facilityCategoryId
            facilitiesCount
            score
            risks {
              year
              relativeYear
              facilitiesFireRisk
            }
          }
        }
      }
      wind {
        riskLevel
        atRisk {
          propertyCount
          level
        }
      }
    }
    neighborhood {
      name
      air {
        days {
          outdoorDays {
            relativeYear
            color {
              color
            }
            totalDays
          }
        }
      }
      fire {
        communityRisk {
          riskPercentile
          score
          facilitiesCount
          facilitiesCategory {
            facilityCategoryId
            facilitiesCount
            score
            risks {
              year
              relativeYear
              facilitiesFireRisk
            }
          }
        }
      }
      flood {
        adaptationConnection {
          totalCount
        }
        communityRisk {
          riskPercentile
          score
          facilitiesCount
          facilitiesCategory {
            facilityCategoryId
            facilitiesCount
            score
            risks {
              facilitiesOperationalRisk
              facilitiesWaterRisk
              relativeYear
              year
            }
          }
        }
      }
    }
    zcta {
      name
      air {
        days {
          outdoorDays {
            relativeYear
            color {
              color
            }
            totalDays
          }
        }
      }
      fire {
        communityRisk {
          riskPercentile
          score
          facilitiesCount
          facilitiesCategory {
            facilityCategoryId
            facilitiesCount
            score
            risks {
              year
              relativeYear
              facilitiesFireRisk
            }
          }
        }
        AAL {
          annualLossByYear {
            relativeYear
            avgDestroyed
            damages
            percent
          }
        }
      }
      flood {
        adaptationConnection {
          totalCount
        }
        communityRisk {
          riskPercentile
          score
          facilitiesCount
          facilitiesCategory {
            facilityCategoryId
            facilitiesCount
            score
            risks {
              facilitiesOperationalRisk
              facilitiesWaterRisk
              relativeYear
              year
            }
          }
        }
        insurance {
          premiumMin
          premiumMax
          provider {
            name
            logo
          }
          purchaseLink
          disclaimer
        }
      }
      wind {
        insurance {
          policyExclusion
          hudWindZone
        }
      }
    }
    buildingConnection(filter: { buildingId: $buildingId }) {
      totalCount
      edges {
        node {
          fsid
          buildingId
          hasBasement
          units
          stories
          yearBuilt
          sqft
          replacementCostPerSqft
          buildingOrientation
          windDesignStandard
          airFilterId
          riskfactorLink
          floorElevation
          landuseCodeId
          isResidential
          construction {
            material
            combustibility
          }
          roof {
            material
            combustibility
          }
          exclusion {
            description
          }
          geometry {
            center {
              coordinates
              type
            }
            polygon {
              coordinates
              type
            }
            bbox {
              coordinates
              type
            }
          }
          flood {
            floodType
            link
            exclusion {
              description
            }
            floodFactor
            riskDirection
            probability {
             cumulative(
                depths: [5, 15, 30, 61, 91, 122, 152, 183, 213, 244, 274, 305, 335, 366, 396, 427, 457, 488, 518, 549, 579, 610]
              ) {
                threshold
                relativeYear
                mid
                yAxisHeightMid
              }
              depth {
                returnPeriod
                relativeYear
                low
                mid
                high
              }
              depthMean: depth(filter: {depthFlavor: MEAN}) {
                returnPeriod
                relativeYear
                low
                mid
                high
              }
            }
            consequences {
              annualized {
                days
                damages
                relativeYear
                percentile
                ssp
              }
            }
            historic {
              eventId
              name
              affectedProperties
              depth
              month
              year
            }
            insights {
              name
              details {
                name
                value
              }
            }
          }
          fire {
            exclusion {
              description
            }
            riskDirection
            fireFactor
            defensibleSpace
            usfsRelativeRisk
            probability {
              damage {
                conditional {
                  flameLossConditional
                  relativeYear
                }
              }
              cumulative {
                year
                relativeYear
                yAxisHeight
                point
              }
              burn {
                emberZone
                relativeYear
                percent
                emberPercent
                flamePercent
                year
                flameMax
                flameMean
                flameBin
              }
            }
            insights {
              name
              details {
                name
                value
              }
            }
          }
          heat {
            exclusion {
              description
            }
            heatFactor
            insights {
              name
              details {
                name
                value
              }
            }
          }
          wind {
            windFactor
            factorScale
            riskDirection
            hasTornadoRisk
            hasThunderstormRisk
            hasCycloneRisk
            greatestWindRisk
            missileEnvironment
            primaryWindDirection
            probability {
              speed {
                ssp
                year
                relativeYear
                returnPeriod
                maxSpeed
                maxGust
                category {
                  windCategoryId
                  name
                  minWindSpeed
                  maxWindSpeed
                }
              }
              cumulative(
                input: {thresholds: [50, 75, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240]}
              ) {
                ssp
                year
                relativeYear
                threshold
                probability
                yMax
                category {
                  windCategoryId
                  name
                  minWindSpeed
                  maxWindSpeed
                }
              }
            }
            exclusion {
              description
            }
          }
          air {
            exclusion {
              description
            }
            airFactor
            factorScale
            riskDirection
            insights {
              name
              details {
                name
                value
              }
            }
          }
          property {
            flood {
              floodType
              link
              exclusion {
                description
              }
              floodFactor
              riskDirection
              probability {
                cumulative(depths: [5, 15, 30, 61, 91, 122, 152, 183, 213, 244, 274, 305, 335, 366, 396, 427, 457, 488, 518, 549, 579, 610]) {
                  threshold
                  relativeYear
                  mid
                  yAxisHeightMid
                }
                depth {
                  returnPeriod
                  relativeYear
                  low
                  mid
                  high
                }
                depthMean: depth(filter: {depthFlavor: MEAN}) {
                  returnPeriod
                  relativeYear
                  low
                  mid
                  high
                }
              }
              insuranceRequirement
              insuranceQuotes {
                rates {
                  providers
                  minPrice
                  maxPrice
                  link
                }
              }
              historic {
                eventId
                name
                affectedProperties
                depth
                month
                year
              }
              stats {
                floodfactorRankInCity
              }
              adaptationConnection {
                totalCount
              }
              insights {
                name
                details {
                  name
                  value
                }
              }
              insuranceQuotes {
                provider {
                  name
                }
                rates {
                  link
                  minPrice
                  maxPrice
                }
              }
            }
            fire {
              exclusion {
                description
              }
              riskDirection
              fireFactor
              defensibleSpace
              usfsRelativeRisk
              prescribedBurns: historicConnection(filter: {type: [PRESCRIBED_FIRE]}) {
                totalCount
              }
              probability {
                burn {
                  emberZone
                  relativeYear
                  percent
                  year
                  flameMax
                  flameMean
                  flameBin
                }
                cumulative {
                  year
                  relativeYear
                  point
                  yAxisHeight
                }
              }
              historicConnection(first: 100) {
                totalCount
                edges {
                  node {
                    ... on PropertyFireHistoric {
                      eventId
                      name
                      distance
                      month
                      year
                      area
                      eventAffectedProperties
                    }
                  }
                }
              }
              insuranceHippo {
                rates {
                  providers
                  minPrice
                  maxPrice
                  link
                }
              }
              insights {
                name
                details {
                  name
                  value
                }
              }
            }
            heat {
              exclusion {
                description
              }
              heatFactor
              hotTemperature
              anomalyTemperature
              temperatureAverageHigh {
                relativeYear
                mmt
              }
              cooling {
                coolingTemp
                cost
                costPerKwh
                energy
                relativeYear
              }
              heatWaves {
                hotHeatWave {
                  length
                  relativeYear
                  probability
                }
              }
              days {
                distribution {
                  relativeYear
                  binLower
                  days
                }
                hotDays {
                  relativeYear
                  days
                  yAxisHeight
                }
                anomalyDays {
                  relativeYear
                  days
                }
                coolingDays {
                  relativeYear
                  days
                }
                dangerousDays {
                  relativeYear
                  days
                }
                healthCautionDays {
                  relativeYear
                  days
                }
              }
              insights {
                name
                details {
                  name
                  value
                }
              }
            }
            wind {
              windFactor
              factorScale
              riskDirection
              hasTornadoRisk
              hasThunderstormRisk
              hasCycloneRisk
              greatestWindRisk
              missileEnvironment
              primaryWindDirection
              probability {
                speed {
                  ssp
                  year
                  relativeYear
                  returnPeriod
                  maxSpeed
                  maxGust
                  category {
                    windCategoryId
                    name
                    minWindSpeed
                    maxWindSpeed
                  }
                }
                direction {
                  ssp
                  direction
                  percent
                }
                cumulative(
                  input: {thresholds: [50, 75, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240]}
                ) {
                  ssp
                  year
                  relativeYear
                  threshold
                  probability
                  yMax
                  category {
                    windCategoryId
                    name
                    minWindSpeed
                    maxWindSpeed
                  }
                }
              }
              historicConnection(
                first: 100
                filter: {mappedEventsOnly: true}
                sort: PROPERTIES_AFFECTED_DESC
              ) {
                pageInfo {
                  hasNextPage
                  endCursor
                }
                totalCount
                edges {
                  node {
                    ... on PropertyWindHistoricEventThunderstorm {
                      eventId
                      eventType
                      date
                      year
                      damages
                      injuries
                      fatalities
                      maxWind
                    }
                    ... on PropertyWindHistoricEventTornado {
                      eventId
                      eventType
                      date
                      damages
                      year
                      fatalities
                      injuries
                      geometry {
                        bbox {
                          coordinates
                          type
                        }
                      }
                      category {
                        tornadoCategoryId
                        rating
                        isEnhanced
                        name
                        minWindSpeed
                        maxWindSpeed
                        description
                      }
                    }
                    ... on PropertyWindHistoricEventCyclone {
                      localWindSpeed
                      eventId
                      eventType
                      windSpeed
                      name
                      date
                      year
                      geometry {
                        bbox {
                          coordinates
                          type
                        }
                      }
                      categoryAtLandfall {
                        windCategoryId
                        name
                        minWindSpeed
                        maxWindSpeed
                      }
                      categoryMax {
                        windCategoryId
                        name
                        minWindSpeed
                        maxWindSpeed
                      }
                      categoryLocality {
                        windCategoryId
                        name
                        minWindSpeed
                        maxWindSpeed
                      }
                      affectedProperties
                      affectedPropertiesNationwide
                      hasDetails
                    }
                  }
                }
              }
              exclusion {
                description
              }
            }
            air {
              exclusion {
                description
              }
              airFactor
              factorScale
              riskDirection
              days {
                outdoorDays {
                  year
                  relativeYear
                  color {
                    color
                  }
                  ozoneDays
                  ozoneDaysYAxisHeight
                  anthroPM25Days
                  anthroPM25DaysYAxisHeight
                  smokeMaxDays
                  smokeMaxDaysYAxisHeight
                  smokeAvgDays
                  smokeAvgDaysYAxisHeight
                  totalDays
                  totalDaysYAxisHeight
                }
              }
              greatestRisk {
                criteriaPollutantId
                name
                description
              }
              triNearby
              triFacilityConnection {
                totalCount
                edges {
                  node {
                    triFacilityId
                    name
                    industry {
                      industrySectorId
                      name
                    }
                  }
                }
              }
              historic {
                aqi {
                  year
                  aqiAvg
                  aqiMax
                  worstDate
                  criteriaPollutant {
                    criteriaPollutantId
                    name
                    description
                  }
                }
                days(filter: {colorID: 3}) {
                  year
                  totalDays
                }
              }
              insights {
                name
                details {
                  name
                  value
                }
              }
              percentile {
                national
                state
              }
            }
          }
        }
      }
    }
  }
}

"""

# You can add more queries here in the future if needed