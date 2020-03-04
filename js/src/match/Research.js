import React from 'react'
import Typography from '@material-ui/core/Typography'
import Grid from '@material-ui/core/Grid'

import Timeline from 'react-visjs-timeline'
import '../css/Timeline.css'

import moment from 'moment'
import {flatMap, map} from 'lodash'

import {PLAYER_COLORS} from '../util/Shared'
import DataQuery from '../util/DataQuery'
import PlayerChart from './PlayerChart.js'
import GetResearch from '../graphql/Research'


const ResearchTimeline = ({players, duration_secs}) => {
  const min_resolution = 60 * 1000 * 5
  const start = (Math.min(...players.map(player => player.research[0].started_secs))/1000) * 1000000
  const options = {
    min: 0,
    max: duration_secs * 1000,
    start: start,
    end: start + (min_resolution * 2),
    selectable: false,
    orientation: 'top',
    showMajorLabels: false,
    zoomMin: min_resolution,
    moment: (date) => moment(date).utc(),
    format: {
      minorLabels: {
        second: 'H:mm:ss',
        minute: 'H:mm:ss',
        hour: 'H:mm:ss'
      }
    }
  }

  const items = flatMap(players, player => map(player.research, research => ({
    start: research.started_secs * 1000,
    end: (research.finished_secs !== null ? research.finished_secs : duration_secs) * 1000,
    content: research.name,
    title: `${research.started} - ${research.finished}`,
    group: player.color_id,
    style: `
      background-color: ${PLAYER_COLORS[player.color_id + 1]};
      line-height: 11px;
      border-color: white;
      border-radius: 4px;
    `
  })))

  const groups = players.map(player => ({
    id: player.color_id,
    content: player.name,
    style: 'color: white'
  }))

  return <Timeline options={options} items={items} groups={groups} />
}

const Research = ({match}) => {
  return (
    <DataQuery query={GetResearch} variables={{match_id: match.id}}>
      {(data) => (
      <>
        <Typography variant='h6'>Research Timeline</Typography>
        <ResearchTimeline players={data.match.players} duration_secs={match.duration_secs} />
        <br />
        <Grid container>
          <Grid item xs={6}>
            <PlayerChart players={data.match.players} group='timeseries' field='value_spent_research' title='Cumulative Spending' help='Cumulative total of resources spent on researching technology' skipzero={true} />
          </Grid>
          <Grid item xs={6}>
            <PlayerChart players={data.match.players} group='timeseries' field='roi' title='Return on Investment' help='Value in resources of all units and buildings destroyed by the player, divided by the value of resources spent on researching technologies (after Dark Age)' skipzero={true} />
          </Grid>
        </Grid>
        </>
      )}
    </DataQuery>
  )
}

export default Research
