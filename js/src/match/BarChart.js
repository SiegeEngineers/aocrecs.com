import React, {useState} from 'react'
import {makeStyles} from '@material-ui/styles'

import Slider from '@material-ui/core/Slider'
import ApexChart from 'react-apexcharts'

import moment from 'moment'
import {flatMap, map, uniqBy, sortBy, groupBy, reduce, cloneDeep} from 'lodash'

import {PLAYER_COLORS} from '../util/Shared'


const useStyles = makeStyles(theme => ({
  chart: {
    paddingTop: '40px',
  }
}))


const BarChart = ({match, dataKey, customFilter, lockSelection, defaultInterval}) => {
  const classes = useStyles()
  const data = flatMap(match.players.map(player => player[dataKey]))
  const first = sortBy(data.filter(customFilter), 'timestamp_secs')[0].timestamp_secs / 60
  const [interval, setInterval] = useState([first, first + defaultInterval])
  const filterRow = (row) => {
    return row.timestamp_secs >= interval[0] * 60 && row.timestamp_secs < interval[1] * 60 && customFilter(row)
  }
  const template = sortBy(uniqBy(data.filter(filterRow).map(t => ({x: t.name, y: 0})), 'x'), 'x')
  const series = map(match.players, player => ({
    name: player.name,
    data: cloneDeep(template).map(x => (
      Object.assign(
        x,
        map(groupBy(player[dataKey].filter(filterRow), 'name'), (k, v) => ({
          x: v,
          y: reduce(map(k, s => s.count), (x, y) => x + y, 0)
        })).find(y => y.x === x.x))
    ))
  }))
  const categories = template.map(unit => unit.x)
  const colors = match.players.map(player => PLAYER_COLORS[player.color_id + 1])
  const setter = lockSelection ? (e, n) => {
    if(n === interval) {
      return
    }
    if(n[0] !== interval[0]) {
      setInterval([n[0], n[0] + defaultInterval])
    }
    if(n[1] !== interval[1]) {
      setInterval([n[1] - defaultInterval, n[1]])
    }
  }
  : (e, n) => setInterval(n)

  return (
    <div className={classes.chart}>
      <Slider
        className={classes.slider}
        value={interval}
        valueLabelDisplay="on"
        valueLabelFormat={(n) => moment.unix(n * 60).utc().format('HH:mm')}
        onChange={setter}
        step={5}
        marks
        min={0}
        max={((match.duration_secs-(match.duration_secs % 300)) / 60) + 5}
      />
      <ApexChart type="bar" width="1000" height={90 + (categories.length * 25)} series={series}
        options={{
          colors: colors,
          xaxis: {
            type: 'category',
            labels: {
              style: {
                fontSize: '13px'
              }
            },
            categories: categories
          },
          yaxis: {
            labels: {
              style: {
                fontSize: '13px'
              }
            }
          },
          plotOptions: {
            bar: {
              horizontal: true,
            }
          },
          tooltip: {
            theme: 'dark',
            enabled: true
          },
          chart: {
            foreColor: 'white',
            type: 'bar',
            stacked: true,
            toolbar: {
              show: false,
              tools: {
                download: true,
                selection: false,
                zoom: true,
                zoomin: false,
                zoomout: false,
                pan: false,
                reset: true
              }
            },
            fontFamily: 'Roboto'
          },
          legend: {
            fontSize: '13px',
            position: 'top',
            horizontalAlign: 'right',
          }
        }
      } />
    </div>
  )
}

export default BarChart
