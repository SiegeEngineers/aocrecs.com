import React from 'react'
import {makeStyles} from '@material-ui/styles'

import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import Grid from '@material-ui/core/Grid'
import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableCell from '@material-ui/core/TableCell'
import TableHead from '@material-ui/core/TableHead'
import TableRow from '@material-ui/core/TableRow'
import Typography from '@material-ui/core/Typography'

import ReactCountryFlag from 'react-country-flag'

import AppLink from './util/AppLink'
import CardIconHeader from './util/CardIconHeader'
import DataQuery from './util/DataQuery'
import RelatedMatches from './util/RelatedMatches'

import GetPerson from './graphql/Person'
import GetPeople from './graphql/People'


const useStyles = makeStyles({
  narrowTable: {
    width: 'unset'
  }
})


const PeopleTable = ({rows, selected}) => {
  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell align='right'></TableCell>
          <TableCell>Name</TableCell>
          <TableCell>Activity</TableCell>
          <TableCell align='right'>Matches</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {rows.map((row, index) =>
          <TableRow key={index} selected={selected === row.id}>
            <TableCell align='right'>{row.country && <ReactCountryFlag countryCode={row.country} title={row.country.toUpperCase()} svg />}</TableCell>
            <TableCell><AppLink path={['players', row.id]} text={row.name} /></TableCell>
            <TableCell>{row.first_year} - {row.last_year}</TableCell>
            <TableCell align='right'>{row.match_count.toLocaleString()}</TableCell>

          </TableRow>
        )}
      </TableBody>
    </Table>
  )
}


const Person = ({id}) => {
  const classes = useStyles()
  return (
    <RelatedMatches query={GetPerson} variables={{id}} field='person'>
      {(data) => (
        <Card>
          <CardIconHeader icon={data.country && <ReactCountryFlag countryCode={data.country} title={data.country.toUpperCase()} svg />} title={data.name} />
          <CardContent>
            <Typography variant='h6'>Aliases</Typography>
            <Typography>{data.aliases.join(', ')}</Typography>
            <br />
            <Typography variant='h6'>Accounts</Typography>
            <Table className={classes.narrowTable}>
              <TableHead>
                <TableRow>
                  <TableCell>Name</TableCell>
                  <TableCell>Platform</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {data.accounts.map((row, index) =>
                  <TableRow key={index}>
                    <TableCell><AppLink path={['user', row.platform.id, row.id]} text={row.name} /></TableCell>
                    <TableCell>{row.platform.name}</TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
            <br />
            <Typography variant='h6'>Event Participation</Typography>
            <Table className={classes.narrowTable}>
              <TableHead>
                <TableRow>
                  <TableCell>Event</TableCell>
                  <TableCell>Year</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {data.events.map((row, index) =>
                  <TableRow key={index}>
                    <TableCell><AppLink path={['events', row.id]} text={row.name} /></TableCell>
                    <TableCell>{row.year}</TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>

          </CardContent>
        </Card>
      )}
    </RelatedMatches>
  )
}


const PlayersView = ({match}) => {
  return (
    <div>
      <Typography variant='h5'>Known Players</Typography>
      <Typography>This list can grow as known players and associated accounts are added to the database.</Typography>
      <br />
      <Grid container spacing={24}>
        <Grid item xs={3}>
          <DataQuery query={GetPeople}>
            {(data) => (
              <PeopleTable
                rows={data.people}
                selected={parseInt(match.params.id)}
               />
            )}
          </DataQuery>
        </Grid>
        {match.params.id && <Grid item xs={9}>
          <Person id={parseInt(match.params.id)} />
        </Grid>}
      </Grid>
    </div>
  )
}

export default PlayersView

