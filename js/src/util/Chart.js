import React from 'react'
import ApexChart from 'react-apexcharts'
import {useTheme} from '@material-ui/styles'
import {merge} from 'lodash'


const Chart = ({id, type, timeseries, series, width, height, y_min, custom}) => {
  const theme = useTheme()
  const options = {
    colors: [theme.palette.primary.main],
    dataLabels: {
      enabled: false
    },
    xaxis: {
      labels: {
        style: {
          fontSize: '13px'
        }
      }
    },
    yaxis: {
      min: y_min,
      tickAmount: height / 50,
      forceNiceScale: true,
      labels: {
        style: {
          fontSize: '13px'
        }
      }
    },
    chart: {
      id: id,
      foreColor: 'white',
      toolbar: {
        show: false,
        tools: {
          download: true,
          selection: false,
          zoom: false,
          zoomin: false,
          zoomout: false,
          pan: false,
          reset: true
        }
      },
      fontFamily: 'Roboto',
      animations: {
        enabled: false
      }
    },
    tooltip: {
      theme: 'dark',
      enabled: false
    },
    legend: {
      position: 'top',
      horizontalAlign: 'right',
      floating: true,
      show: true
    }
  }
  if (timeseries === true) {
    merge(options, {
      xaxis: {
        type: "datetime",
        labels: {
          format: "MM/dd"
        }
      },
      yaxis: {
        labels: {
          formatter: (value) => Math.floor(value).toLocaleString()
        }
      }
    })
  }
  if (type === 'bar') {
    merge(options, {
      plotOptions: {
        bar: {
            horizontal: true,
        }
      },
      xaxis: {
        labels: {
          trim: false,
          formatter: (value) => value === 0 ? 0 : (value >= 1000000 ? (value/1000000) + 'm' : (value/1000) + 'k')
        }
      },
      yaxis: {
        labels: {
          maxWidth: 500,
        }
      },
      grid: {
        xaxis: {
          lines: {
            show: true
          }
        },
        yaxis: {
          lines: {
            show: false
          }
        }
      }
    })
  }
  merge(options, custom)
  return <ApexChart type={type} width={width} height={height} series={series} options={options} />
}

export default Chart
