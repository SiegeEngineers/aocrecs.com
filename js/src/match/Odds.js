import React from 'react'

import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableCell from '@material-ui/core/TableCell'
import TableHead from '@material-ui/core/TableHead'
import TableRow from '@material-ui/core/TableRow'

import YesIcon from 'mdi-react/CheckIcon'
import NoIcon from 'mdi-react/CloseIcon'
import UndeterminedIcon from 'mdi-react/MinusIcon'

import {getHasTeams} from '../util/Shared'
import DataQuery from '../util/DataQuery'
import GetOdds from '../graphql/Odds'

import PlayerName from './PlayerName'

const Scenario = ({title, scenario, match}) => {
  return (
    <TableRow>
      <TableCell>{title}</TableCell>
      {scenario ? scenario.map((team, index) => (
        <TableCell key={index} align='right'>{Math.round(team.percent*1000)/10}% ({team.wins}/{team.losses})</TableCell>
      )): <TableCell align='center' colSpan={match.teams.length + 1}>{match.mirror ? 'Not applicable' : 'Not enough data'}</TableCell>}
      {scenario && <TableCell align='center'>{scenario[match.winning_team_id].percent > 0.5 ? <YesIcon /> : (scenario[match.winning_team_id].percent === 0.5 ? <UndeterminedIcon /> : <NoIcon />)}</TableCell>}
    </TableRow>
  )
}

const Odds = ({match}) => {
  const hasTeams = getHasTeams(match.team_size)
  return (
    <DataQuery query={GetOdds} variables={{match_id: match.id}}>
      {(data) => (
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Scenario</TableCell>
            {match.teams.map((team, index) => (
              <TableCell key={index} align='right'>{hasTeams ? <span>Team {index+1}</span> : <PlayerName player={team.players[0]} />}</TableCell>
            ))}
            <TableCell align='center'>Expected Outcome</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          <Scenario title='Players' scenario={data.match.odds.teams} match={match} />
          <Scenario title='Players on Map' scenario={data.match.odds.teams_and_map} match={match} />
          <Scenario title='Players with Civilizations' scenario={data.match.odds.teams_and_civilization} match={match} />
          <Scenario title='Civilizations' scenario={data.match.odds.civilizations} match={match} />
          <Scenario title='Civilizations on Map' scenario={data.match.odds.civilizations_and_map} match={match} />
        </TableBody>
      </Table>
      )}
    </DataQuery>
  )
}

export default Odds
