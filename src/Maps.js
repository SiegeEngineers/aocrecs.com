import React from 'react'

import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import Grid from '@material-ui/core/Grid'
import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableCell from '@material-ui/core/TableCell'
import TableHead from '@material-ui/core/TableHead'
import TableRow from '@material-ui/core/TableRow'
import Typography from '@material-ui/core/Typography'

import MapIcon from 'mdi-react/EarthIcon'

import AppLink from './util/AppLink'
import CardIconHeader from './util/CardIconHeader'
import DataQuery from './util/DataQuery'
import RelatedMatches from './util/RelatedMatches'

import GetMap from './graphql/Map'
import GetMaps from './graphql/Maps'

const MapTable = ({rows, selected}) => {
  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>Map</TableCell>
          <TableCell>Matches</TableCell>
          <TableCell>Percent</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {rows.map((row, index) =>
          <TableRow key={index} selected={selected === row.map.id}>
            <TableCell><AppLink path={['maps', row.map.id]} text={row.map.name} /></TableCell>
            <TableCell>{row.num_matches}</TableCell>
            <TableCell>{Math.round(row.percent_matches * 1000)/10}%</TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  )
}

const Map = ({id}) => {
  return (
    <RelatedMatches query={GetMap} variables={{id}} field='map'>
      {(data) => (
        <Card>
          <CardIconHeader icon={<MapIcon />} title={data.name} />
          <CardContent>
            <Typography component='span'>
              <ol>
                {data.popular_civs.map((stat) =>
                  <li key={stat.civilization.cid}>
                    {stat.civilization.name} ({Math.round(stat.percent_matches * 1000)/10}%)
                  </li>
                )}
              </ol>
            </Typography>
          </CardContent>
        </Card>
      )}
    </RelatedMatches>
  )
}

const MapsView = ({match}) => {
  return (
    <Grid container spacing={24}>
      <Grid item xs={6}>
        <DataQuery query={GetMaps}>
          {(data) => (
            <MapTable
              rows={data.stats.by_map}
              selected={parseInt(match.params.id)}
             />
          )}
        </DataQuery>
      </Grid>
      {match.params.id && <Grid item xs={6}>
        <Map id={match.params.id} />
      </Grid>}
    </Grid>
  )
}

export default MapsView
