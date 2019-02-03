import React from 'react'
import {makeStyles} from '@material-ui/styles'

import Grid from '@material-ui/core/Grid'

import Match from './Match.js'

const useStyles = makeStyles({
  root: {
    marginTop: '10px'
  }
})

const Matches = ({matches}) => {
  const classes = useStyles()
  return (
    <div className={classes.root}>
      <Grid container spacing={24}>
        {matches.map(match => (
          <Grid item key={match.id}>
            <Match match={match} />
          </Grid>
        ))}
      </Grid>
    </div>
  )
}

export default Matches
