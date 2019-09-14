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
            <Grid item><Stat title='Matches' stat={data.stats.matches.toLocaleString()} /></Grid>
            <Grid item><Stat title='Series' stat={data.stats.series.toLocaleString()} /></Grid>
            <Grid item><Stat title='Players' stat={data.stats.users.toLocaleString()} /></Grid>
            <Grid item><Stat title='Maps' stat={data.stats.map_count.toLocaleString()} /></Grid>
          </Grid>
          <Grid container spacing={24}>
            <Grid item>
              <Card>
                <CardContent>
                  <Typography variant='h5'>Match Additions</Typography>
                  <Chart id="additions" width='500' height='280' timeseries={true} series={[{data: data.stats.by_day.map(d => [d.date, d.matches])}]} />
                </CardContent>
              </Card>
            </Grid>
            <Grid item>
              <Card>
                <CardContent>
                  <Typography variant='h5'>Languages</Typography>
                  <Chart id="languages" width='500' height='280' type='bar' series={[{data: data.stats.languages.map(i => ({x: i.label, y: i.count}))}]} />
                </CardContent>
              </Card>
            </Grid>
          <Grid item>
              <Card>
                <CardContent>
                  <Typography variant='h5'>Datasets</Typography>
                  <Chart id="datasets" width='500' height='280' type='bar' series={[{data: data.stats.datasets.map(i => ({x: i.label.split(': ')[1], y: i.count}))}]} />
                </CardContent>
              </Card>
            </Grid>
            <Grid item>
              <Card>
                <CardContent>
                  <Typography variant='h5'>Platforms</Typography>
                  <Chart id="platforms" width='500' height='280' type='bar' series={[{data: data.stats.platforms.map(i => ({x: i.label, y: i.count}))}]} />
                </CardContent>
              </Card>
            </Grid>
            <Grid item>
              <Card>
                <CardContent>
                  <Typography variant='h5'>Diplomacy</Typography>
                  <Chart id="diplomacy" width='500' height='280' type='bar' series={[{data: data.stats.diplomacy_types.map(i => ({x: i.label, y: i.count}))}]} />
                </CardContent>
              </Card>
            </Grid>
            <Grid item>
              <Card>
                <CardContent>
                  <Typography variant='h5'>Match Types</Typography>
                  <Chart id="types" width='500' height='280' type='bar' series={[{data: data.stats.game_types.map(i => ({x: i.label, y: i.count}))}]} />
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
