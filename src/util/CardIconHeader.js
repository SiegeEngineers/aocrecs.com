import React from 'react'
import {makeStyles} from '@material-ui/styles'
import Typography from '@material-ui/core/Typography'

const useStyles = makeStyles({
  root: {
    padding: '16px',
    paddingBottom: '0px'
  },
  heading: {
    display: 'inline-flex',
    lineHeight: '1.1'
  },
  icon: {
    paddingRight: '5px'
  }
})

const CardIconHeader = ({icon, title}) => {
  const classes = useStyles()
  return (
    <div className={classes.root}>
      <Typography variant="h5" className={classes.heading}>
        <div className={classes.icon}>{icon}</div>
        <div>{title}</div>
      </Typography>
    </div>
  )
}

export default CardIconHeader
