import React from 'react'
import {makeStyles} from '@material-ui/styles'
import Tooltip from '@material-ui/core/Tooltip'
import HelpIcon from 'mdi-react/HelpCircleOutlineIcon'

const tooltipStyle = makeStyles(theme => ({
    arrow: {
      color: theme.palette.common.black,
    },
    tooltip: {
      backgroundColor: theme.palette.common.black,
      fontSize: '14px',
      opacity: 0.5
  }
}))

const useStyles = makeStyles(theme => ({
  helpIconLarge: {
    width: '18px',
    height: '18px'
  },
  helpIconSmall: {
    width: '14px',
    height: '14px'
  }
}))


const Help = ({text, small}) => {
  const classes = useStyles()
  return (
    <>
      {text &&
        <Tooltip title={text} classes={tooltipStyle()} placement="right" arrow TransitionProps={{ timeout: 0 }}>
          <span><HelpIcon className={small ? classes.helpIconSmall : classes.helpIconLarge} /></span>
        </Tooltip>
      }
    </>
  )
}

export default Help
