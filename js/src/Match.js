import React, {useState} from 'react'
import {makeStyles} from '@material-ui/styles'

import AppBar from '@material-ui/core/AppBar'
import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import Link from '@material-ui/core/Link'
import Tabs from '@material-ui/core/Tabs'
import Tab from '@material-ui/core/Tab'
import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableCell from '@material-ui/core/TableCell'
import TableHead from '@material-ui/core/TableHead'
import TableRow from '@material-ui/core/TableRow'
import Typography from '@material-ui/core/Typography'

import Timestamp from 'react-timestamp'
import humanizeDuration from 'humanize-duration'
import {upperFirst} from 'lodash'

import MatchIcon from 'mdi-react/SwordCrossIcon'
import MVPIcon from 'mdi-react/StarIcon'
import YesIcon from 'mdi-react/CheckIcon'
import NoIcon from 'mdi-react/CloseIcon'
import UndeterminedIcon from 'mdi-react/MinusIcon'

import AppLink from './util/AppLink'
import DataQuery from './util/DataQuery'
import CardIconHeader from './util/CardIconHeader'
import WinnerMark from './util/WinnerMark'
import {getMatchTitle} from './util/Shared'
import GetOdds from './graphql/Odds'

const shortHumanizeDuration = humanizeDuration.humanizer({
  language: 'shortEn',
  languages: {
    shortEn: {
      y: () => 'y',
      mo: () => 'mo',
      w: () => 'w',
      d: () => 'd',
      h: () => 'h',
      m: () => 'm',
      s: () => 's',
      ms: () => 'ms',
    }
  }
})

const PLAYER_COLORS = {
  1: '#6599d8',
  2: '#f25f5f',
  3: '#00ee00',
  4: '#ffd700',
  5: '#00eeee',
  6: '#ea69e1',
  7: '#808080',
  8: '#ff8c00'
}

const useStyles = makeStyles(theme => ({
  playerColor: {
    borderRadius: '4px',
    borderWidth: '1px',
    borderColor: 'white',
    height: '12px',
    width: '12px',
    display: 'inline-block',
    borderStyle: 'solid',
    marginRight: '4px'
  },
  tabContent: {
    padding: '10px'
  },
  mvpIcon: {
    width: '12px',
    height: '12px'
  },
  teamWinner: {
    width: '16px',
    height: '16px'
  },
  winner: {
    width: '12px',
    height: '12px'
  },
  downloadLink: {
    color: theme.palette.primary.main
  }
}))


const getHasTeams = (size) => {
  return size !== '1v1'
}

const PlayerName = ({player}) => {
  const classes = useStyles()
  return (
    <span>
      <div style={{backgroundColor: PLAYER_COLORS[player.color_id + 1]}} className={classes.playerColor} />
      {player.user
        ? <AppLink path={['player', player.user.platform_id, player.user.id]} text={player.user.name} />
        : player.name
      }
    </span>
  )
}

const TeamRow = ({number, winner, span}) => {
  const classes = useStyles()
  return (
    <TableRow>
      <TableCell colSpan={span}>
        <Typography variant='h6'>
          Team {number} <WinnerMark winner={winner} className={classes.teamWinner} />
        </Typography>
      </TableCell>
    </TableRow>
  )
}

const TeamBody = ({teams, hasTeams, children, span}) => {
  const classes = useStyles()
  return (
    <>
      {teams.map((team, index) => (
        <TableBody key={index}>
          {hasTeams && <TeamRow number={index + 1} winner={team.winner} span={span} />}
          {team.players.map((player, mindex) => (
            <TableRow key={mindex}>
              <TableCell>
                <WinnerMark winner={!hasTeams && player.winner} className={classes.winner} /> <PlayerName player={player} />
              </TableCell>
              {children(player)}
            </TableRow>
          ))}
        </TableBody>
      ))}
    </>
  )
}

const rateString = (player) => {
  let out = player.rate_snapshot
  const diff = player.rate_after - player.rate_before
  if (diff > 0) {
    out += ' ' + String.fromCharCode(8593) + Math.abs(diff)
  } else if (diff < 0) {
    out += ' ' + String.fromCharCode(8595) + Math.abs(diff)
  }
  return out
}

const Teams = ({size, teams, rated, postgame}) => {
  const hasTeams = getHasTeams(size)
  const classes = useStyles()
  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>Player</TableCell>
          <TableCell>Civilization</TableCell>
          {hasTeams && <TableCell>MVP</TableCell>}
          {rated && <TableCell align='right'>Rating</TableCell>}
          {postgame && <TableCell align='right'>Score</TableCell>}
        </TableRow>
      </TableHead>
      <TeamBody teams={teams} hasTeams={hasTeams} span={5}>
        {(player) => (
          <>
            <TableCell>
              <AppLink path={['civilizations', player.civilization.dataset_id, player.civilization.id]} text={player.civilization.name} />
            </TableCell>
            {hasTeams && <TableCell>
              {player.mvp && <MVPIcon className={classes.mvpIcon} />}
            </TableCell>}
            {rated && <TableCell align='right'>{rateString(player)}</TableCell>}
            {postgame && <TableCell align='right'>{player.score && player.score.toLocaleString()}</TableCell>}
          </>
        )}
      </TeamBody>
    </Table>
  )
}

const Information = ({match}) => {
  const hasTeams = getHasTeams(match.team_size)
  return (
    <Table>
      <TableBody>
      <TableRow>
        <TableCell>Duration</TableCell><TableCell>{humanizeDuration(match.duration_secs * 1000)}</TableCell>
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
        <TableCell>Event</TableCell><TableCell>{match.event.name}</TableCell>
      </TableRow>}
      {match.series && match.tournament && <TableRow>
        <TableCell>Tournament</TableCell><TableCell><AppLink path={['events', match.tournament.id]} text={match.tournament.name} /></TableCell>
      </TableRow>}
      {match.series && <TableRow>
        <TableCell>Series</TableCell><TableCell><AppLink path={['events', match.tournament.id, match.series.id]} text={match.series.name} /></TableCell>
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
            <AppLink path={['events', event.id]} text={event.name} />
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
      {match.platform && <TableRow>
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

const Achievements = ({size, teams}) => {
  const hasTeams = getHasTeams(size)
  return (
    <div>
      <Typography variant='h6'>Score</Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Player</TableCell>
            <TableCell align='right'>Military</TableCell>
            <TableCell align='right'>Economy</TableCell>
            <TableCell align='right'>Technology</TableCell>
            <TableCell align='right'>Society</TableCell>
            <TableCell align='right'>Total</TableCell>
          </TableRow>
        </TableHead>
        <TeamBody teams={teams} hasTeams={hasTeams} span={6}>
          {(player) => (
            <>
              <TableCell align='right'>{player.military_score}</TableCell>
              <TableCell align='right'>{player.economy_score}</TableCell>
              <TableCell align='right'>{player.technology_score}</TableCell>
              <TableCell align='right'>{player.society_score}</TableCell>
              <TableCell align='right'>{player.score}</TableCell>
            </>
          )}
        </TeamBody>
      </Table>
      <br />
      <Typography variant='h6'>Military</Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Player</TableCell>
            <TableCell align='right'>Units Killed</TableCell>
            <TableCell align='right'>Buildings Razed</TableCell>
            <TableCell align='right'>Units Lost</TableCell>
            <TableCell align='right'>Buildings Lost</TableCell>
            <TableCell align='right'>Units Converted</TableCell>
          </TableRow>
        </TableHead>
        <TeamBody teams={teams} hasTeams={hasTeams} span={6}>
          {(player) => (
            <>
              <TableCell align='right'>{player.units_killed}</TableCell>
              <TableCell align='right'>{player.buildings_razed}</TableCell>
              <TableCell align='right'>{player.units_lost}</TableCell>
              <TableCell align='right'>{player.buildings_lost}</TableCell>
              <TableCell align='right'>{player.units_converted}</TableCell>
            </>
          )}
        </TeamBody>
      </Table>
      <br />
      <Typography variant='h6'>Economy</Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Player</TableCell>
            <TableCell align='right'>Food</TableCell>
            <TableCell align='right'>Wood</TableCell>
            <TableCell align='right'>Stone</TableCell>
            <TableCell align='right'>Gold</TableCell>
            <TableCell align='right'>Sent</TableCell>
            <TableCell align='right'>Received</TableCell>
            <TableCell align='right'>Trade</TableCell>
            <TableCell align='right'>Relic</TableCell>
          </TableRow>
        </TableHead>
        <TeamBody teams={teams} hasTeams={hasTeams} span={9}>
          {(player) => (
            <>
              <TableCell align='right'>{player.food_collected}</TableCell>
              <TableCell align='right'>{player.wood_collected}</TableCell>
              <TableCell align='right'>{player.stone_collected}</TableCell>
              <TableCell align='right'>{player.gold_collected}</TableCell>
              <TableCell align='right'>{player.tribute_sent}</TableCell>
              <TableCell align='right'>{player.tribute_received}</TableCell>
              <TableCell align='right'>{player.trade_gold}</TableCell>
              <TableCell align='right'>{player.relic_gold}</TableCell>
            </>
          )}
        </TeamBody>
      </Table>
      <br />
      <Typography variant='h6'>Technology</Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Player</TableCell>
            <TableCell align='right'>Feudal</TableCell>
            <TableCell align='right'>Castle</TableCell>
            <TableCell align='right'>Imperial</TableCell>
            <TableCell align='right'>Explored</TableCell>
            <TableCell align='right'>Researches</TableCell>
          </TableRow>
        </TableHead>
        <TeamBody teams={teams} hasTeams={hasTeams} span={6}>
          {(player) => (
            <>
              <TableCell align='right'>{shortHumanizeDuration(player.feudal_time_secs * 1000)}</TableCell>
              <TableCell align='right'>{shortHumanizeDuration(player.castle_time_secs * 1000)}</TableCell>
              <TableCell align='right'>{shortHumanizeDuration(player.imperial_time_secs * 1000)}</TableCell>
              <TableCell align='right'>{player.explored_percent}</TableCell>
              <TableCell align='right'>{player.research_count}</TableCell>
            </>
          )}
        </TeamBody>
      </Table>
      <br />
      <Typography variant='h6'>Society</Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Player</TableCell>
            <TableCell align='right'>Wonders</TableCell>
            <TableCell align='right'>Castles</TableCell>
            <TableCell align='right'>Relics</TableCell>
            <TableCell align='right'>Villager High</TableCell>
          </TableRow>
        </TableHead>
        <TeamBody teams={teams} hasTeams={hasTeams} span={5}>
          {(player) => (
            <>
              <TableCell align='right'>{player.total_wonders}</TableCell>
              <TableCell align='right'>{player.total_castles}</TableCell>
              <TableCell align='right'>{player.total_relics}</TableCell>
              <TableCell align='right'>{player.villager_high}</TableCell>
            </>
          )}
        </TeamBody>
      </Table>

    </div>
  )
}

const Files = ({files}) => {
  const classes = useStyles()
  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>File</TableCell>
          <TableCell>Owner</TableCell>
          <TableCell align='right'>Size</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {files.map(file => (
          <TableRow key={file.id}>
            <TableCell><a className={classes.downloadLink} href={process.env.REACT_APP_API + '/download/' + file.id}>{file.original_filename}</a></TableCell>
            <TableCell>{file.owner.name}</TableCell>
            <TableCell align='right'>{file.size}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}

const Map = ({match}) => {
  return (
    <img src={process.env.REACT_APP_API + "/map/" + match.id} width="100%" />
  )
}

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

const Match = ({match}) => {
  const [tab, setTab] = useState(0)
  const classes = useStyles()
  const title = getMatchTitle(match, true)
  return (
    <Card>
      <CardIconHeader icon={<AppLink path={['match', match.id]} text={<MatchIcon />} />} title={title}/>
      <CardContent>
        <AppBar position='static'>
          <Tabs value={tab} onChange={(e, value) => setTab(value)} variant="fullWidth">
            <Tab label='Players' />
            <Tab label='Information' />
            <Tab label='Map' />
            <Tab label='Odds' />
            <Tab label='Files' />
            {match.postgame && <Tab label='Achievements' />}}
          </Tabs>
        </AppBar>
        <Typography component='div' className={classes.tabContent}>
          {tab === 0 && <Teams size={match.team_size} teams={match.teams} rated={match.rated} postgame={match.postgame} />}
          {tab === 1 && <Information match={match} />}
          {tab === 2 && <Map match={match} />}
          {tab === 3 && <Odds match={match} />}
          {tab === 4 && <Files files={match.files} />}
          {tab === 5 && <Achievements size={match.team_size} teams={match.teams} />}
        </Typography>
      </CardContent>
    </Card>
  )
}

export default Match
