import React, { useState } from 'react'
import { Bar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

function Harvest() {
  const [selectedRegion, setSelectedRegion] = useState('All')
  const [selectedCrop, setSelectedCrop] = useState('All')

  const regions = ['All', 'Southern', 'Central', 'Northern']
  const crops = ['All', 'Maize', 'Groundnuts', 'Soybean', 'Tobacco', 'Cassava', 'Beans', 'Rice']

  // Sample data - crop-specific yield data per region
  // In production, this would come from your API
  const cropData = {
    'Maize': {
      Southern: { yield: 4.5, farmers: 30, avg_rainfall: 850 },
      Central: { yield: 3.8, farmers: 45, avg_rainfall: 780 },
      Northern: { yield: 3.2, farmers: 20, avg_rainfall: 720 }
    },
    'Groundnuts': {
      Southern: { yield: 2.2, farmers: 18, avg_rainfall: 820 },
      Central: { yield: 1.8, farmers: 25, avg_rainfall: 760 },
      Northern: { yield: 1.5, farmers: 12, avg_rainfall: 700 }
    },
    'Soybean': {
      Southern: { yield: 2.8, farmers: 15, avg_rainfall: 830 },
      Central: { yield: 2.3, farmers: 22, avg_rainfall: 770 },
      Northern: { yield: 2.0, farmers: 10, avg_rainfall: 710 }
    },
    'Tobacco': {
      Southern: { yield: 2.0, farmers: 12, avg_rainfall: 800 },
      Central: { yield: 2.5, farmers: 20, avg_rainfall: 750 },
      Northern: { yield: 2.2, farmers: 8, avg_rainfall: 690 }
    },
    'Cassava': {
      Southern: { yield: 8.5, farmers: 10, avg_rainfall: 850 },
      Central: { yield: 7.2, farmers: 15, avg_rainfall: 790 },
      Northern: { yield: 6.5, farmers: 6, avg_rainfall: 730 }
    },
    'Beans': {
      Southern: { yield: 1.6, farmers: 20, avg_rainfall: 810 },
      Central: { yield: 1.4, farmers: 28, avg_rainfall: 750 },
      Northern: { yield: 1.2, farmers: 14, avg_rainfall: 700 }
    },
    'Rice': {
      Southern: { yield: 3.2, farmers: 8, avg_rainfall: 900 },
      Central: { yield: 2.8, farmers: 12, avg_rainfall: 840 },
      Northern: { yield: 2.5, farmers: 5, avg_rainfall: 800 }
    }
  }

  // Get the data based on selected crop and region
  const getFilteredData = () => {
    let filtered = {}

    // If specific crop selected
    if (selectedCrop !== 'All') {
      const crop = cropData[selectedCrop]
      if (selectedRegion !== 'All') {
        filtered = { [selectedRegion]: crop?.[selectedRegion] || null }
      } else {
        filtered = crop || {}
      }
    } else {
      // 'All' crops - average across all crops
      const allCrops = Object.keys(cropData)
      const regions = ['Southern', 'Central', 'Northern']
      regions.forEach(region => {
        let totalYield = 0, totalFarmers = 0, count = 0
        allCrops.forEach(crop => {
          if (cropData[crop]?.[region]) {
            totalYield += cropData[crop][region].yield
            totalFarmers += cropData[crop][region].farmers
            count++
          }
        })
        if (count > 0) {
          filtered[region] = {
            yield: parseFloat((totalYield / count).toFixed(1)),
            farmers: totalFarmers,
            avg_rainfall: parseFloat(((cropData['Maize']?.[region]?.avg_rainfall || 0) + 
                                     (cropData['Groundnuts']?.[region]?.avg_rainfall || 0) + 
                                     (cropData['Soybean']?.[region]?.avg_rainfall || 0) + 
                                     (cropData['Tobacco']?.[region]?.avg_rainfall || 0)) / 4).toFixed(0)
          }
        }
      })
    }

    // Apply region filter if specific region selected
    if (selectedRegion !== 'All' && selectedCrop !== 'All') {
      return filtered
    }

    return filtered
  }

  const filteredData = getFilteredData()
  const regionKeys = Object.keys(filteredData)

  // Prepare chart data
  const chartData = {
    labels: regionKeys,
    datasets: [
      {
        label: `${selectedCrop === 'All' ? 'All Crops' : selectedCrop} - Average Yield (t/ha)`,
        data: regionKeys.map(r => filteredData[r]?.yield || 0),
        backgroundColor: ['#1F9E8C', '#A8481C', '#D4A63A', '#2b6a5a', '#8a6a3a'],
        borderRadius: 4
      }
    ]
  }

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: { boxWidth: 12, font: { size: 12 } }
      },
      title: {
        display: true,
        text: `${selectedCrop === 'All' ? 'All Crops' : selectedCrop} - Regional Performance`,
        font: { size: 16, weight: 'bold' }
      }
    },
    scales: {
      y: {
        title: { display: true, text: 'Yield (tons per hectare)' },
        min: 0,
        max: 6
      }
    }
  }

  // Get the title for the stats section
  const getStatsTitle = () => {
    if (selectedCrop === 'All' && selectedRegion === 'All') {
      return 'All Crops - National Summary'
    } else if (selectedCrop !== 'All' && selectedRegion === 'All') {
      return `${selectedCrop} - All Regions`
    } else if (selectedCrop === 'All' && selectedRegion !== 'All') {
      return `All Crops - ${selectedRegion} Region`
    } else {
      return `${selectedCrop} - ${selectedRegion} Region`
    }
  }

  return (
    <div className="wrap">
      <h2 style={{ marginBottom: 8 }}>Harvest Trends</h2>
      <p style={{ color: 'var(--ink-soft)', marginBottom: 24 }}>
        Regional agricultural performance by crop type
      </p>

      {/* Filters */}
      <div style={{
        display: 'flex',
        gap: 16,
        marginBottom: 24,
        flexWrap: 'wrap',
        alignItems: 'center'
      }}>
        <div>
          <label style={{ fontSize: 13, fontWeight: 600, marginRight: 8 }}>Region:</label>
          <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
            {regions.map((region) => (
              <button
                key={region}
                onClick={() => setSelectedRegion(region)}
                style={{
                  padding: '6px 14px',
                  borderRadius: '20px',
                  border: selectedRegion === region ? '2px solid var(--twin)' : '1px solid var(--line)',
                  background: selectedRegion === region ? 'rgba(31,158,140,0.1)' : 'transparent',
                  color: selectedRegion === region ? 'var(--twin)' : 'var(--ink)',
                  cursor: 'pointer',
                  fontSize: 12,
                  fontWeight: selectedRegion === region ? 600 : 400
                }}
              >
                {region}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label style={{ fontSize: 13, fontWeight: 600, marginRight: 8 }}>Crop:</label>
          <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
            {crops.map((crop) => (
              <button
                key={crop}
                onClick={() => setSelectedCrop(crop)}
                style={{
                  padding: '6px 14px',
                  borderRadius: '20px',
                  border: selectedCrop === crop ? '2px solid var(--soil)' : '1px solid var(--line)',
                  background: selectedCrop === crop ? 'rgba(168,72,28,0.1)' : 'transparent',
                  color: selectedCrop === crop ? 'var(--soil)' : 'var(--ink)',
                  cursor: 'pointer',
                  fontSize: 12,
                  fontWeight: selectedCrop === crop ? 600 : 400
                }}
              >
                {crop}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      {regionKeys.length > 0 ? (
        <>
          <h4 style={{ marginBottom: 12 }}>{getStatsTitle()}</h4>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: 16,
            marginBottom: 24
          }}>
            {regionKeys.map((region) => (
              <div key={region} className="card">
                <h4 style={{ fontSize: 14, color: 'var(--ink-soft)', marginBottom: 8 }}>{region}</h4>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <div>
                    <div style={{ fontSize: 24, fontWeight: 700, color: 'var(--twin)' }}>
                      {filteredData[region]?.yield || 0} t/ha
                    </div>
                    <div style={{ fontSize: 12, color: 'var(--ink-soft)' }}>Avg Yield</div>
                  </div>
                  <div>
                    <div style={{ fontSize: 24, fontWeight: 700, color: 'var(--soil)' }}>
                      {filteredData[region]?.farmers || 0}
                    </div>
                    <div style={{ fontSize: 12, color: 'var(--ink-soft)' }}>Farmers</div>
                  </div>
                  <div>
                    <div style={{ fontSize: 24, fontWeight: 700, color: 'var(--gold)' }}>
                      {filteredData[region]?.avg_rainfall || 0} mm
                    </div>
                    <div style={{ fontSize: 12, color: 'var(--ink-soft)' }}>Rainfall</div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Chart */}
          <div className="card" style={{ height: '350px' }}>
            <Bar data={chartData} options={chartOptions} />
          </div>
        </>
      ) : (
        <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
          <p style={{ color: 'var(--ink-soft)' }}>No data available for the selected filters.</p>
          <p style={{ fontSize: 13, color: 'var(--ink-soft)' }}>
            Try selecting a different crop or region.
          </p>
        </div>
      )}

      {/* Farmer Distribution by Region */}
      <div className="card" style={{ marginTop: 16 }}>
        <h4 style={{ fontSize: 14, marginBottom: 12 }}>
          Farmer Distribution by Region {selectedCrop !== 'All' ? `(${selectedCrop})` : '(All Crops)'}
        </h4>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: 16
        }}>
          {regionKeys.map((region) => {
            const maxFarmers = Math.max(...regionKeys.map(r => filteredData[r]?.farmers || 0))
            return (
              <div key={region}>
                <div style={{ fontSize: 13, fontWeight: 600 }}>{region}</div>
                <div style={{
                  width: '100%',
                  height: 8,
                  background: 'var(--line)',
                  borderRadius: 4,
                  marginTop: 4,
                  overflow: 'hidden'
                }}>
                  <div style={{
                    width: maxFarmers > 0 ? `${(filteredData[region]?.farmers / maxFarmers) * 100}%` : '0%',
                    height: '100%',
                    background: 'var(--twin)',
                    borderRadius: 4
                  }}></div>
                </div>
                <div style={{ fontSize: 12, color: 'var(--ink-soft)', marginTop: 2 }}>
                  {filteredData[region]?.farmers || 0} farmers
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

export default Harvest