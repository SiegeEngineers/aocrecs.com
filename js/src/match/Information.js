import React from 'react'

import Link from '@material-ui/core/Link'
import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableCell from '@material-ui/core/TableCell'
import TableRow from '@material-ui/core/TableRow'

import Timestamp from 'react-timestamp'
import {upperFirst} from 'lodash'

import AppLink from '../util/AppLink'
import {getHasTeams} from '../util/Shared'


const Information = ({match}) => {
  const hasTeams = getHasTeams(match.team_size)
  return (
    <Table>
      <TableBody>
      <TableRow>
        <TableCell>Duration</TableCell><TableCell>{match.duration}</TableCell>
      </TableRow>
      {match.played && <TableRow>
        <TableCell>Played</TableCell><TableCell><Timestamp time={match.played} format='full' /></TableCell>
      </TableRow>}
      {match.rated && match.ladder && <TableRow>
        <TableCell>Ladder</TableCell>
        <TableCell>
          <AppLink path={['ladders', match.ladder.platform_id, match.ladder.lid]} text={match.ladder.name} />
        </TableCell>
      </TableRow>}
      <TableRow>
        <TableCell>Rated</TableCell><TableCell>{match.rated ? 'Yes' : 'No'}</TableCell>
      </TableRow>
      {match.series && match.tournament && match.event && <TableRow>
        <TableCell>Event</TableCell><TableCell><AppLink path={['events', match.event.id]} text={match.event.name} /></TableCell>
      </TableRow>}
      {match.series && match.tournament && <TableRow>
        <TableCell>Tournament</TableCell><TableCell><AppLink path={['events', match.event.id, match.tournament.id]} text={match.tournament.name} /></TableCell>
      </TableRow>}
      {match.series && <TableRow>
        <TableCell>Series</TableCell><TableCell><AppLink path={['events', match.event.id, match.tournament.id, match.series.id]} text={match.series.name} /></TableCell>
      </TableRow>}
      {!hasTeams && <TableRow>
        <TableCell>Mirror</TableCell><TableCell>{match.mirror ? 'Yes' : 'No'}</TableCell>
      </TableRow>}
      <TableRow>
        <TableCell>Map</TableCell>
        <TableCell>
          <AppLink path={['maps', match.map_name]} text={match.map_name} /> ({match.map_size})
        </TableCell>
      </TableRow>
      {match.map_events && <TableRow>
        <TableCell>Map Event</TableCell>
        <TableCell>
          {match.map_events.map((event, i) => [
            i > 0 && ', ',
            <AppLink key={event.id} path={['events', event.id]} text={event.name} />
          ])}
        </TableCell>
      </TableRow>}
      <TableRow>
        <TableCell>Cheats</TableCell><TableCell>{match.cheats ? 'On' : 'Off'}</TableCell>
      </TableRow>
      <TableRow>
        <TableCell>Reveal Map</TableCell><TableCell>{match.map_reveal_choice}</TableCell>
      </TableRow>
      <TableRow>
        <TableCell>Population Limit</TableCell><TableCell>{match.population_limit}</TableCell>
      </TableRow>
      <TableRow>
        <TableCell>Speed</TableCell><TableCell>{match.speed}</TableCell>
      </TableRow>
      <TableRow>
        <TableCell>Lock Teams</TableCell><TableCell>{match.lock_teams ? 'On' : 'Off'}</TableCell>
      </TableRow>
      <TableRow>
        <TableCell>Difficulty</TableCell><TableCell>{match.difficulty}</TableCell>
      </TableRow>
      {match.dataset && <TableRow>
        <TableCell>Dataset</TableCell><TableCell>{match.dataset.name} {match.dataset_version}</TableCell>
      </TableRow>}
      <TableRow>
        <TableCell>Version</TableCell><TableCell>{upperFirst(match.version)}</TableCell>
      </TableRow>
      {match.platform && match.platform.url === '' && <TableRow>
        <TableCell>Platform</TableCell>
        <TableCell>
          {match.platform.name}
        </TableCell>
      </TableRow>}
      {match.platform && match.platform.url !== '' && <TableRow>
        <TableCell>Platform</TableCell>
        <TableCell>
          <Link href={match.platform.url} underline='always' target='_blank'>{match.platform.name}</Link>
        </TableCell>
      </TableRow>}
      {match.platform_match_id && <TableRow>
        <TableCell>Match Link</TableCell>
        <TableCell>
          <Link href={match.platform.match_url + match.platform_match_id} underline='always' target='_blank'>{match.platform_match_id}</Link>
        </TableCell>
      </TableRow>}
    </TableBody>
    </Table>
  )
}

export default Information
