import React from 'react'
import {makeStyles} from '@material-ui/styles'
import Typography from '@material-ui/core/Typography'

import moment from 'moment'

import {PLAYER_COLORS} from '../util/Shared'
import Chart from '../util/Chart'
import Help from '../util/Help'


const useStyles = makeStyles(theme => ({
  chart: {
    marginBottom: '20px'
  }
}))


const PlayerChart = ({players, group, field, title, help, skipzero, custom}) => {
  const classes = useStyles()
  const firstNonZero = moment.unix(Math.min(...players.map(player => {
    const f = player[group] && player[group].find(row => row[field] !== 0)
    return f !== undefined && f !== null ? f.timestamp_secs : -1
  }).filter(ts => ts >= 0)))
  const series =  players.map(player => ({
    name: player.name,
    data: player[group].map(row => (
      [moment.unix(row.timestamp_secs), row[field]]
    )).filter(row => skipzero ? row[0] >= firstNonZero : true)
  }))
  const config = {
    colors: players.map(player => (
      PLAYER_COLORS[player.color_id + 1]
    )),
    xaxis: {
      type: "datetime",
      labels: {
        format: 'H:mm:ss'
      }
    },
    tooltip: {
      x: {
        format: 'H:mm:ss'
      },
      enabled: true,
    },
    stroke: {
       width: 3
    },
    ...custom
  }
  return (
    <>
      <Typography variant='h6'>{title} <Help text={help} /></Typography>
      <Chart
        id={field} width='100%' height='200' timeseries={true} className={classes.chart}
        series={series}
        custom={config}
      />
    </>
  )
}

export default PlayerChart
