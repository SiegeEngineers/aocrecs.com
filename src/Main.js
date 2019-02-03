import React from 'react'

import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import Grid from '@material-ui/core/Grid'
import Typography from '@material-ui/core/Typography'

import Chart from './util/Chart'
import DataQuery from './util/DataQuery'

import GetStats from './graphql/Stats'

const Stat = ({title, stat}) => {
  return (
    <Card>
      <CardContent>
        <Typography component='p'>{title}</Typography>
        <Typography variant='h3'>{stat}</Typography>
      </CardContent>
    </Card>
  )
}

const Main = () => {
  return (
    <DataQuery query={GetStats}>
      {(data) => (
        <div>
          <Grid container spacing={24}>
            <Grid item><Stat title='Files' stat={data.stats.files} /></Grid>
            <Grid item><Stat title='Matches' stat={data.stats.matches} /></Grid>
            <Grid item><Stat title='Series' stat={data.stats.series} /></Grid>
            <Grid item><Stat title='Players' stat={data.stats.voobly_users} /></Grid>
          </Grid>
          <Grid container spacing={24}>
            <Grid item>
              <Card>
                <CardContent>
                  <Typography variant='h5'>Match Additions</Typography>
                  <Chart width='500' series={[{data: data.stats.by_day.map(d => [d.date, d.matches])}]} />
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </div>
      )}
    </DataQuery>
  )
}

export default Main
