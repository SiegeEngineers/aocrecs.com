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
import Typography from '@material-ui/core/Typography'
import FormControl from '@material-ui/core/FormControl'
import InputLabel from '@material-ui/core/InputLabel'
import MenuItem from '@material-ui/core/MenuItem'
import Select from '@material-ui/core/Select'
import Box from '@material-ui/core/Box'
import Link from '@material-ui/core/Link'
import Avatar from '@material-ui/core/Avatar'

import {sortBy, uniqBy} from 'lodash'
import {getName} from 'country-list'

import ReactCountryFlag from 'react-country-flag'

import PaginatedTable from './util/PaginatedTable'
import AppLink from './util/AppLink'
import CardIconHeader from './util/CardIconHeader'
import DataQuery from './util/DataQuery'
import RelatedMatches from './util/RelatedMatches'

import GetPerson from './graphql/Person'
import GetPeople from './graphql/People'


const useStyles = makeStyles({
  narrowTable: {
    width: 'unset',
    margin: '5px'
  },
  portrait: {
    width: '150px',
    height: '150px'
  },
})


const PeopleTable = ({rows, selected}) => {
  return (
    <PaginatedTable limit={25} rows={rows}>
    {(rows) => (
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
    )}
    </PaginatedTable>
  )
}


const format_name = (data) => {
  if(data.first_name !== null && data.last_name !== null) {
    return data.name + ' (' + data.first_name + ' ' + data.last_name + ')'
  }
  return data.name
}

const formatter = new Intl.NumberFormat(undefined, {
  style: 'currency',
  currency: 'USD',
})

const Person = ({id}) => {
  const classes = useStyles()
  return (
    <RelatedMatches query={GetPerson} variables={{id}} field='person'>
      {(data) => (
        <Card>
          <CardIconHeader icon={data.country && <ReactCountryFlag countryCode={data.country} title={data.country.toUpperCase()} svg />} title={format_name(data)} />
          <CardContent>
            <Box display='flex'>
              <Box>
                {data.portrait_link && <Avatar alt={data.name} src={data.portrait_link} className={classes.portrait} />}
              </Box>
              <Box>
            <Table className={classes.narrowTable}>
              <TableBody>
                {data.country && <TableRow>
                  <TableCell><Box fontWeight="fontWeightMedium">Country</Box></TableCell>
                  <TableCell align="right">{getName(data.country)}</TableCell>
                </TableRow>}
                {data.earnings && <TableRow>
                  <TableCell><Box fontWeight="fontWeightMedium">Pro Earnings</Box></TableCell>
                  <TableCell align="right"><Link target="_blank" href={"https://www.esportsearnings.com/players/" + data.esportsearnings_id}>{formatter.format(data.earnings)}</Link></TableCell>
                </TableRow>}
                {data.aoeelo_rank && <TableRow>
                  <TableCell><Box fontWeight="fontWeightMedium">Tournament Elo</Box></TableCell>
                  <TableCell align="right"><Link target="_blank" href={"https://aoe-elo.com/player/" + data.aoeelo_id + "/"}>{data.aoeelo_rate} (#{data.aoeelo_rank})</Link></TableCell>
                </TableRow>}
              </TableBody>
            </Table>
          </Box>
        </Box>
            <br />
            <Typography variant='h6'>Aliases</Typography>
            <Typography>{data.aliases.join(', ')}</Typography>
            <br />
            <Box display='flex'>
              <Box>
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
          </Box>
          <Box>
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
          </Box>
        </Box>

          </CardContent>
        </Card>
      )}
    </RelatedMatches>
  )
}


const PlayersView = ({match}) => {
  const [country, setCountry] = useState('all')
  return (
    <div>
      <Typography variant='h5'>Known Players</Typography>
      <Typography>This list can grow as known players and associated accounts are added to the database.</Typography>
      <br />
      <Grid container spacing={24}>
        <Grid item xs={3}>
          <DataQuery query={GetPeople}>
            {(data) => (
              <>
              <FormControl>
                <InputLabel htmlFor='country'>Country</InputLabel>
                <Select value={country} onChange={(e, v) => setCountry(e.target.value)}>
                  <MenuItem key={0} value={'all'}>All</MenuItem>
                  {sortBy(uniqBy(data.people, 'country'), 'country').filter(row => row.country !== null).map((person, i) =>
                    <MenuItem key={i+1} value={person.country}>
                      <ReactCountryFlag countryCode={person.country} title={person.country.toUpperCase()} svg />&nbsp;{person.country.toUpperCase()}
                    </MenuItem>
                  )}
                </Select>
              </FormControl>
              <PeopleTable
                rows={data.people.filter(row => country !== 'all' ? row.country === country : true)}
                selected={parseInt(match.params.id)}
              />
              </>
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

