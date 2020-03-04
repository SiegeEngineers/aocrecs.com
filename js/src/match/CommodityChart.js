import React from 'react'
import {useTheme, makeStyles} from '@material-ui/styles'
import Typography from '@material-ui/core/Typography'

import moment from 'moment'

import Chart from '../util/Chart'
import Help from '../util/Help'


const useStyles = makeStyles(theme => ({
  chart: {
    marginBottom: '20px'
  }
}))


const CommodityChart = ({data, fields, title, help, custom}) => {
  const classes = useStyles()
  const theme = useTheme()
  const series = fields.map(field => ({
    name: field.charAt(0).toUpperCase() + field.split('_')[0].slice(1),
    data: data.map(row => [moment.unix(row.timestamp_secs), row[field]])
  }))
  const config = {
    colors: [theme.palette.primary.main, theme.palette.secondary.main],
    stroke: {
      width: 3,
      curve: 'stepline'
    },
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
    ...custom
  }
  return (
    <>
      <Typography variant='h6'>{title} <Help text={help} /></Typography>
      <Chart
        id={title} width='100%' height='200' timeseries={true} className={classes.chart}
        series={series}
        custom={config}
      />
    </>
  )
}

export default CommodityChart
