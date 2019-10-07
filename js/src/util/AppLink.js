import React from 'react'
import {makeStyles} from '@material-ui/styles'
import {Link} from 'react-router-dom'

const useStyles = makeStyles(theme => ({
  root: {
    color: theme.palette.primary.main
  }
}))

const AppLink = ({path, text}) => {
  const classes = useStyles()
  return (
    <Link to={'/' + path.join('/')} className={classes.root}>
      {text}
    </Link>
  )
}

export default AppLink
