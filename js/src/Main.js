import React from 'react'

import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import Grid from '@material-ui/core/Grid'
import Typography from '@material-ui/core/Typography'

import Odometer from 'react-odometerjs'
import {reverse} from 'lodash'
import {useSubscription} from '@apollo/react-hooks'

import AppLink from './util/AppLink'
import Chart from './util/Chart'
import DataQuery from './util/DataQuery'

import GetStats from './graphql/Stats'
import GetSubscription from './graphql/Subscriptions'

import 'odometer/themes/odometer-theme-default.css'

const Stat = ({title, stat}) => {
  return (
    <Card>
      <CardContent>
        <Typography component='p'>{title}</Typography>
        <Typography variant='h3'><Odometer value={stat} format="(,ddd)" /></Typography>
      </CardContent>
    </Card>
  )
}


const Cell = ({children}) => {
  return (
    <Grid item>
    <Card>
      <CardContent>
        <Typography component='p'>{children}</Typography>
      </CardContent>
    </Card>
  </Grid>
  )
}


const Main = () => {
  const sub = useSubscription(GetSubscription)
  return (
    <DataQuery query={GetStats}>
      {(data) => (
        <div>
          <Grid container spacing={24}>
            <Grid item><Stat title='Matches' stat={sub.data ? sub.data.stats.match_count : data.stats.match_count } /></Grid>
            <Grid item><Stat title='Series' stat={data.stats.series_count} /></Grid>
            <Grid item><Stat title='Players' stat={data.stats.player_count} /></Grid>
            <Grid item><Stat title='Maps' stat={data.stats.map_count} /></Grid>
          </Grid>
          <Grid container spacing={24}>
            <Cell>
              Recorded Games for Latest Versions:
            </Cell>
            {reverse(data.latest_summary.map((latest, i) => (
              <Cell>
                <AppLink path={['latest', latest.dataset.id]} text={latest.dataset.name + ' ' + latest.version}/>&nbsp;
                (<Odometer value={sub.data ? sub.data.stats.latest_summary[i].count : latest.count} format="(,ddd)" />)
              </Cell>
            )))}
          </Grid>
          <Grid container>
            <Grid item xs={4}>
              <Card>
                <CardContent>
                  <Typography variant='h5'>Match Additions</Typography>
                  <Chart id="additions" height='280' timeseries={true} series={[{data: data.stats.by_day.map(d => [d.date, d.count])}]} y_min={0} />
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={4}>
              <Card>
                <CardContent>
                  <Typography variant='h5'>Languages</Typography>
                  <Chart id="languages" height='280' type='bar' series={[{data: data.stats.languages.map(i => ({x: i.name, y: i.count}))}]} />
                </CardContent>
              </Card>
            </Grid>
          <Grid item xs={4}>
              <Card>
                <CardContent>
                  <Typography variant='h5'>Datasets</Typography>
                  <Chart id="datasets" height='280' type='bar' series={[{data: data.stats.datasets.map(i => ({x: i.name, y: i.count}))}]} />
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={4}>
              <Card>
                <CardContent>
                  <Typography variant='h5'>Platforms</Typography>
                  <Chart id="platforms" height='280' type='bar' series={[{data: data.stats.platforms.map(i => ({x: i.name, y: i.count}))}]} />
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={4}>
              <Card>
                <CardContent>
                  <Typography variant='h5'>Diplomacy</Typography>
                  <Chart id="diplomacy" height='280' type='bar' series={[{data: data.stats.diplomacy.map(i => ({x: i.name, y: i.count}))}]} />
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={4}>
              <Card>
                <CardContent>
                  <Typography variant='h5'>Match Types</Typography>
                  <Chart id="types" height='280' type='bar' series={[{data: data.stats.types.map(i => ({x: i.name, y: i.count}))}]} />
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
