import React from 'react'
import {makeStyles} from '@material-ui/styles'
import {NavLink} from 'react-router-dom'

import Box from '@material-ui/core/Box'
import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import List from '@material-ui/core/List'
import Typography from '@material-ui/core/Typography'
import ListItem from '@material-ui/core/ListItem'
import ListItemIcon from '@material-ui/core/ListItemIcon'
import ListItemText from '@material-ui/core/ListItemText'

import MapIcon from 'mdi-react/EarthIcon'
import PlayersIcon from 'mdi-react/AccountMultipleIcon'
import InformationIcon from 'mdi-react/InformationIcon'
import AchievementsIcon from 'mdi-react/TrophyIcon'
import ChatIcon from 'mdi-react/ChatIcon'
import FilesIcon from 'mdi-react/FileDownloadIcon'
import OddsIcon from 'mdi-react/ScaleBalanceIcon'
import GraphIcon from 'mdi-react/GraphIcon'
import ResearchIcon from 'mdi-react/SchoolIcon'
import MilitaryIcon from 'mdi-react/SwordIcon'
import ChartsIcon from 'mdi-react/ChartLineIcon'
import MarketIcon from 'mdi-react/SwapHorizontalBoldIcon'
import EconomyIcon from 'mdi-react/HomeGroupIcon'
import EventsIcon from 'mdi-react/FlagIcon'

import Research from './match/Research'
import Graph from './match/Graph'
import Flags from './match/Flags'
import Military from './match/Military'
import Market from './match/Market'
import Charts from './match/Charts'
import Economy from './match/Economy'
import Chat from './match/Chat'
import Information from './match/Information'
import Achievements from './match/Achievements'
import Files from './match/Files'
import Odds from './match/Odds'
import Map from './match/Map'
import {Teams} from './match/Teams'

import {getMatchTitle} from './util/Shared'
import DataQuery from './util/DataQuery'
import GetMatch from './graphql/Match'


const useStyles = makeStyles(theme => ({
  link: {
    textDecoration: 'none',
    color: 'white'
  }
}))


const MatchLink = ({id, route, label, icon, selected}) => {
  const classes = useStyles()
  return (
    <NavLink key={route} to={`/match/${id}/${route}`} className={classes.link}>
      <ListItem button selected={selected === route}>
        <ListItemIcon>{icon}</ListItemIcon>
        <ListItemText primary={label} />
      </ListItem>
    </NavLink>
  )
}


const Match = ({match, selected, subselected}) => {
  const title = getMatchTitle(match, true)
  const shouldGrow = (selected) => {
    const grow = ['research']
    return grow.includes(selected) ? 1 : 0
  }
  return (
    <div>
      <Typography variant='h5'>{title}</Typography>
      <Box display='flex'>
        <Box>
          <List>
            <MatchLink id={match.id} selected={selected} route='players' label='Players' icon={<PlayersIcon />} />
            <MatchLink id={match.id} selected={selected} route='information' label='Information' icon={<InformationIcon />} />
            <MatchLink id={match.id} selected={selected} route='map' label='Map' icon={<MapIcon />} />
            <MatchLink id={match.id} selected={selected} route='achievements' label='Achievements' icon={<AchievementsIcon />} />
            <MatchLink id={match.id} selected={selected} route='chat' label='Chat' icon={<ChatIcon />} />
            <MatchLink id={match.id} selected={selected} route='files' label='Files' icon={<FilesIcon />} />
            <MatchLink id={match.id} selected={selected} route='odds' label='Odds' icon={<OddsIcon />} />
            {match.has_playback && <>
              <MatchLink id={match.id} selected={selected} route='charts' label='Charts' icon={<ChartsIcon />} />
              <MatchLink id={match.id} selected={selected} route='research' label='Research' icon={<ResearchIcon />} />
              <MatchLink id={match.id} selected={selected} route='military' label='Military' icon={<MilitaryIcon />} />
              <MatchLink id={match.id} selected={selected} route='economy' label='Economy' icon={<EconomyIcon />} />
              <MatchLink id={match.id} selected={selected} route='market' label='Market' icon={<MarketIcon />} />
              <MatchLink id={match.id} selected={selected} route='events' label='Events' icon={<EventsIcon />} />
              <MatchLink id={match.id} selected={selected} route='graph' label='Graph' icon={<GraphIcon />} />
            </>}
          </List>
        </Box>
        <Box flexGrow={shouldGrow(selected)}>
          <Card>
            <CardContent>
              {(selected === 'players' || selected === undefined) && <Teams size={match.team_size} teams={match.teams} rated={match.rated} postgame={match.postgame} />}
              {selected === 'information' && <Information match={match} />}
              {selected === 'map' && <div style={{width: '800px'}}><Map match={match} /></div>}
              {selected === 'achievements' && <Achievements size={match.team_size} teams={match.teams} />}
              {selected === 'files' && <Files files={match.files} />}
              {selected === 'chat' && <Chat match={match} />}
              {selected === 'odds' && <Odds match={match} />}
              {match.has_playback && <>
                {selected === 'charts' && <Charts match={match} />}
                {selected === 'research' && <Research match={match} />}
                {selected === 'military' && <Military match={match} />}
                {selected === 'economy' && <Economy match={match} size={match.team_size} />}
                {selected === 'market' && <Market match={match} size={match.team_size} />}
                {selected === 'events' && <Flags match={match} selected={subselected} />}
                {selected === 'graph' && <Graph match={match} />}
              </>}
            </CardContent>
          </Card>
        </Box>
      </Box>
    </div>
  )
}


const MatchView = ({match}) => {
  const match_id = parseInt(match.params.id)
  return (
    <DataQuery query={GetMatch} variables={{match_id}}>
      {(data) => (
        <Match match={data.match} selected={match.params.section} subselected={match.params.subsection} />
      )}
    </DataQuery>
  )
}

export default MatchView
