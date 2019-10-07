import React, {useState} from 'react'
import {makeStyles} from '@material-ui/styles'

import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import Grid from '@material-ui/core/Grid'
import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableCell from '@material-ui/core/TableCell'
import TableHead from '@material-ui/core/TableHead'
import TableRow from '@material-ui/core/TableRow'
import TextField from '@material-ui/core/TextField'
import Typography from '@material-ui/core/Typography'

import MapIcon from 'mdi-react/EarthIcon'

import Pagination from 'material-ui-flat-pagination'

import AppLink from './util/AppLink'
import CardIconHeader from './util/CardIconHeader'
import DataQuery from './util/DataQuery'
import RelatedMatches from './util/RelatedMatches'
import StandardIcon from 'mdi-react/StarIcon'

import GetMap from './graphql/Map'
import GetMaps from './graphql/Maps'


const useStyles = makeStyles({
  standardIcon: {
    width: '12px',
    height: '12px'
  }
})


const MapTable = ({rows, selected}) => {
  const classes = useStyles()
  const [offset, setOffset] = useState(0)
  const [filter, setFilter] = useState(null)
  const limit = 25
  const filterName = (rows) => {
    return rows.filter((row) => filter !== null ? row.name.includes(filter) : true)
  }
  let total = filterName(rows).length
  return (
    <>
      <TextField
        label='Map'
        value={filter}
        onChange={(event) => setFilter(event.target.value)}
      />
      {total > limit && <Pagination
        limit={limit}
        offset={offset}
        total={total}
        onClick={(e, offset) => setOffset(offset)}
      />}
      <Table>
        <TableHead>
          <TableRow>
            <TableCell></TableCell>
            <TableCell></TableCell>
            <TableCell>Map</TableCell>
            <TableCell>Events</TableCell>
            <TableCell align='right'>Matches</TableCell>
            <TableCell align='right'>Percent</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {filterName(rows).slice(offset, offset + limit).map((row, index) =>
            <TableRow key={index} selected={selected === row.name}>
              <TableCell align='center'>{row.builtin && <StandardIcon className={classes.standardIcon} />}</TableCell>
              <TableCell>{offset + index + 1}</TableCell>
              <TableCell><AppLink path={['maps', row.name]} text={row.name} /></TableCell>
              <TableCell>
                {row.event_maps.map((map, i) => [
                  i > 0 && ', ',
                  <AppLink path={['events', map.event.id]} text={map.event.name} key={map.event.id} />
                ])}
              </TableCell>
              <TableCell align='right'>{row.count.toLocaleString()}</TableCell>
              <TableCell align='right'>{Math.round(row.percent * 1000)/10}%</TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
      {total > limit && <Pagination
        limit={limit}
        offset={offset}
        total={total}
        onClick={(e, offset) => setOffset(offset)}
      />}
    </>
  )
}

const Map = ({name}) => {
  return (
    <RelatedMatches query={GetMap} variables={{name}} field='map'>
      {(data) => (
        <Card>
          <CardIconHeader icon={<MapIcon />} title={data.name} />
          <CardContent>
            {data.popular_civs.length > 0 && <div>
              <Typography variant='h6'>Popular 1v1 Civilizations</Typography>
              <Typography component='span'>
                <ol>
                  {data.popular_civs.map((stat) =>
                    <li key={stat.civilization.cid}>
                      {stat.civilization.name} ({Math.round(stat.percent * 1000)/10}%)
                    </li>
                  )}
                </ol>
              </Typography>
            </div>}
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
        <Map name={match.params.id} />
      </Grid>}
    </Grid>
  )
}

export default MapsView
