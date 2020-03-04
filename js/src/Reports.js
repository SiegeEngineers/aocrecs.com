import React, {useState} from 'react'

import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'

import FormControl from '@material-ui/core/FormControl'
import InputLabel from '@material-ui/core/InputLabel'
import MenuItem from '@material-ui/core/MenuItem'
import Select from '@material-ui/core/Select'
import Grid from '@material-ui/core/Grid'
import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableCell from '@material-ui/core/TableCell'
import TableHead from '@material-ui/core/TableHead'
import TableRow from '@material-ui/core/TableRow'
import Typography from '@material-ui/core/Typography'

import ReactCountryFlag from 'react-country-flag'
import {format, subMonths} from 'date-fns'
import humanizeDuration from 'humanize-duration'

import AppLink from './util/AppLink'
import DataQuery from './util/DataQuery'
import {getMatchTitle, ChangeIndicator} from './util/Shared'

import GetReports from './graphql/Reports.js'
import GetReport from './graphql/Report.js'


const UserName = ({user}) => {
  return (
    <AppLink path={['user', user.platform_id, user.id]} text={user.name} />
  )
}

const PersonName = ({user}) => {
  return (
    <>
    {user.person.country && <ReactCountryFlag countryCode={user.person.country} title={user.person.country.toUpperCase()} svg />} <AppLink path={['players', user.person.id]} text={user.person.name} />
    </>
  )
}

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

const LongestMatchesSection = ({data}) => {
  return (
    <Card>
      <CardContent>
        <Typography variant='h5'>Longest Matches</Typography>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell></TableCell>
              <TableCell>Match</TableCell>
              <TableCell>Map</TableCell>
              <TableCell>Duration</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((match, index) =>
              <TableRow key={match.id}>
                <TableCell>{index + 1}</TableCell>
                <TableCell><AppLink path={['match', match.id]} text={getMatchTitle(match, false)} /></TableCell>
                <TableCell> <AppLink path={['maps', match.map_name]} text={match.map_name} /></TableCell>
                <TableCell>{humanizeDuration(match.duration_secs * 1000)}</TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}

const MostImprovementSection = ({data, title}) => {
  return (
    <Card>
      <CardContent>
        <Typography variant='h5'>Most {title} Improvement</Typography>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell></TableCell>
              <TableCell>Account</TableCell>
              <TableCell align='right'>Lowest</TableCell>
              <TableCell align='right'>Highest</TableCell>
              <TableCell align='right'>Difference</TableCell>
              <TableCell align='right'>Matches</TableCell>
              <TableCell align='right'>Wins</TableCell>
              <TableCell align='right'>Losses</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((row, index) =>
              <TableRow key={row.user.id}>
                <TableCell>{index + 1}</TableCell>
                <TableCell><UserName user={row.user} /></TableCell>
                <TableCell align='right'>{row.min_rate}</TableCell>
                <TableCell align='right'>{row.max_rate}</TableCell>
                <TableCell align='right'>+{row.diff_rate}</TableCell>
                <TableCell align='right'>{row.count}</TableCell>
                <TableCell align='right'>{row.wins}</TableCell>
                <TableCell align='right'>{row.losses}</TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}

const RankingsSection = ({data, title}) => {
  return (
    <Card>
      <CardContent>
        <Typography variant='h5'>{title} Rankings</Typography>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell></TableCell>
              <TableCell></TableCell>
              <TableCell>Account</TableCell>
              <TableCell>Player</TableCell>
              <TableCell align='right'>Rating</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map(row =>
              <TableRow key={row.user_id}>
                <TableCell><ChangeIndicator change={row.change} /></TableCell>
                <TableCell>{row.rank}</TableCell>
                <TableCell><UserName user={row.user} /></TableCell>
                <TableCell>{row.user.person && <PersonName user={row.user} />}</TableCell>
                <TableCell align='right'>{row.rating}</TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}

const PopularMapsSection = ({data}) => {
  return (
    <Card>
      <CardContent>
        <Typography variant='h5'>Popular Maps</Typography>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell></TableCell>
              <TableCell></TableCell>
              <TableCell>Map</TableCell>
              <TableCell align='right'>Matches</TableCell>
              <TableCell align='right'>Percent</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map(row =>
              <TableRow key={row.rank}>
                <TableCell><ChangeIndicator change={row.change} /></TableCell>
                <TableCell>{row.rank}</TableCell>
                <TableCell><AppLink path={['maps', row.map.name]} text={row.map.name} /></TableCell>
                <TableCell align='right'>{row.count.toLocaleString()}</TableCell>
                <TableCell align='right'>{Math.round(row.percent * 1000)/10}%</TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}

const MostMatchesSection = ({data}) => {
  return (
    <Card>
      <CardContent>
        <Typography variant='h5'>Most Matches</Typography>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell></TableCell>
              <TableCell>Account</TableCell>
              <TableCell align='right'>Matches</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((row, index) =>
              <TableRow key={index}>
                <TableCell>{index + 1}</TableCell>
                <TableCell><UserName user={row.user} /></TableCell>
                <TableCell align='right'>{row.count.toLocaleString()}</TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}

const ReportsView = ({match, history}) => {
  const [report_date, setReportDate] = useState(format(subMonths(new Date(), 1), 'yyyy-M'))
  return (
    <div>
      <FormControl>
        <InputLabel htmlFor='platform'>Report</InputLabel>
        <DataQuery query={GetReports}>
          {(data) => (
            <Select value={report_date} onChange={(e, v) => setReportDate(e.target.value)}>
              {data.reports.map((report) =>
                <MenuItem key={report.year + '_' + report.month} value={report.year + '-' + report.month}>
                  {format(new Date(report.year, report.month-1), 'MMMM yyyy')}
                </MenuItem>
              )}
            </Select>
          )}
        </DataQuery>
      </FormControl>
      <br />
      <br />
      <DataQuery query={GetReport} variables={{year: parseInt(report_date.split('-')[0]), month: parseInt(report_date.split('-')[1])}}>
      {(data) => (
        <>
          <Grid container spacing={24}>
            <Grid item><Stat title='Matches' stat={data.report.total_matches.toLocaleString()} /></Grid>
            <Grid item><Stat title='Players' stat={data.report.total_players.toLocaleString()} /></Grid>
          </Grid>
          <Grid container spacing={24}>
            <Grid item>
              <MostMatchesSection data={data.report.most_matches} />
            </Grid>
            <Grid item>
              <PopularMapsSection data={data.report.popular_maps} />
            </Grid>
            <Grid item>
              <RankingsSection data={data.report.rankings_1v1} title={'1v1'} />
            </Grid>
            <Grid item>
              <RankingsSection data={data.report.rankings_tg} title={'Team Game'} />
            </Grid>
            <Grid item>
              <LongestMatchesSection data={data.report.longest_matches} />
            </Grid>
            <Grid item>
              <MostImprovementSection data={data.report.improvement_1v1} title={'1v1'} />
            </Grid>
            <Grid item>
              <MostImprovementSection data={data.report.improvement_tg} title={'Team Game'} />
            </Grid>
          </Grid>
        </>
      )}
      </DataQuery>
    </div>
  )
}

export default ReportsView
