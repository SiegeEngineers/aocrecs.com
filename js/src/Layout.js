import React from 'react'
import {Switch, Redirect, Route, NavLink} from 'react-router-dom'
import {makeStyles} from '@material-ui/styles'

import Drawer from '@material-ui/core/Drawer'
import AppBar from '@material-ui/core/AppBar'
import CssBaseline from '@material-ui/core/CssBaseline'
import Toolbar from '@material-ui/core/Toolbar'
import List from '@material-ui/core/List'
import Typography from '@material-ui/core/Typography'
import ListItem from '@material-ui/core/ListItem'
import ListItemIcon from '@material-ui/core/ListItemIcon'
import ListItemText from '@material-ui/core/ListItemText'

import EventIcon from 'mdi-react/CalendarRangeIcon'
import HomeIcon from 'mdi-react/HomeIcon'
import SearchIcon from 'mdi-react/SearchIcon'
import CivIcon from 'mdi-react/ChessRookIcon'
import MapIcon from 'mdi-react/EarthIcon'
import PlayerIcon from 'mdi-react/AccountIcon'
import LadderIcon from 'mdi-react/FormatListNumberedIcon'
import ReportIcon from 'mdi-react/TableIcon'
import AboutIcon from 'mdi-react/InformationIcon'
import UploadIcon from 'mdi-react/FileUploadIcon'
import WatchingIcon from 'mdi-react/EyeOutlineIcon'
import ApiIcon from 'mdi-react/JsonIcon'

import Main from './Main'
import Search from './Search'
import Events from './Events'
import Ladders from './Ladders'
import Civilizations from './Civilizations'
import Maps from './Maps'
import Match from './MatchView'
import User from './UserView'
import Players from './Players'
import Reports from './Reports'
import Upload from './Upload'
import Latest from './Latest'
import Watching from './Watching'
import About from './About'

const drawerWidth = 180

const useStyles = makeStyles(theme => ({
  root: {
    display: 'flex',
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
  },
  drawerPaper: {
    width: drawerWidth,
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing(1),
  },
  toolbar: theme.mixins.toolbar,
  logo: {
    width: '40px',
    marginRight: '10px'
  },
  title: {
    fontFamily: 'Times New Roman',
  },
  link: {
    textDecoration: 'none',
    color: 'white'
  }
}))

const TITLE = 'Siege Engineers Recorded Game Database'
const LOGO = 'https://github.com/SiegeEngineers/SiegeEngineers-CD/raw/master/SiegeEngineers.png'
const LOGO_ALT = 'SE'
const MENU = [
  {
    link: '/',
    title: 'Main',
    icon: HomeIcon
  },
  {
    link: '/search',
    title: 'Search',
    icon: SearchIcon
  },
  {
    link: '/events',
    title: 'Events',
    icon: EventIcon
  },
  {
    link: '/ladders',
    title: 'Ladders',
    icon: LadderIcon
  },
  {
    link: '/civilizations',
    title: 'Civilizations',
    icon: CivIcon
  },
  {
    link: '/maps',
    title: 'Maps',
    icon: MapIcon
  },
  {
    link: '/players',
    title: 'Players',
    icon: PlayerIcon
  },
  {
    link: '/reports',
    title: 'Reports',
    icon: ReportIcon
  },
  {
    link: '/upload',
    title: 'Upload',
    icon: UploadIcon
  },
  {
    link: '/watching',
    title: 'Watching',
    icon: WatchingIcon
  },
  {
    link: '/api',
    title: 'API',
    icon: ApiIcon
  },
  {
    link: '/about',
    title: 'About',
    icon: AboutIcon
  }
]


const Layout = () => {
  const classes = useStyles()
  return (
    <div className={classes.root}>
      <CssBaseline />
      <AppBar position='fixed' className={classes.appBar}>
        <Toolbar>
          <img alt={LOGO_ALT} src={LOGO} className={classes.logo} />
          <Typography variant='h5' color='inherit' noWrap>
            <span className={classes.title}>{TITLE}</span>
          </Typography>
        </Toolbar>
      </AppBar>
      <Drawer
        className={classes.drawer}
        variant='permanent'
        classes={{
          paper: classes.drawerPaper,
        }}
      >
        <div className={classes.toolbar} />
        <List>
          {MENU.map((link, index) => {
            const Icon = link.icon
            return link.link !== '/api' ? (
              <NavLink key={index} to={link.link} className={classes.link}>
                <ListItem button key={link.title}>
                  <ListItemIcon><Icon /></ListItemIcon>
                  <ListItemText primary={link.title} />
                </ListItem>
              </NavLink>
            ) : (
              <a key={index} href={link.link} className={classes.link}>
                <ListItem button key={link.title}>
                  <ListItemIcon><Icon /></ListItemIcon>
                  <ListItemText primary={link.title} />
                </ListItem>
              </a>
            )
          })}
        </List>
      </Drawer>
      <main className={classes.content}>
        <div className={classes.toolbar} />
        <Switch>
          <Route exact path='/' component={Main} />
          <Route path='/search' component={Search} />
          <Route path='/events/:eid?/:tid?/:sid?' component={Events} />
          <Route path='/ladders/:pid?/:id?/:vid?' component={Ladders} />
          <Route path='/civilizations/:did?/:id?' component={Civilizations} />
          <Route path='/maps/:id?' component={Maps} />
          <Route path='/players/:id?' component={Players} />
          <Route path='/match/:id?/:section?/:subsection?' component={Match} />
          <Route path='/user/:pid?/:id?' component={User} />
          <Route path='/reports/:y?/:m?' component={Reports} />
          <Route path='/upload' component={Upload} />
          <Route path='/latest/:id' component={Latest} />
          <Route path='/watching' component={Watching} />
          <Route path='/about' component={About} />
          <Redirect to='/' />
        </Switch>
        <br />
        <Typography style={{fontSize: 13}}>aocrecs.com isn't endorsed by Microsoft Corporation and doesn't reflect the views or opinions of Microsoft Corporation or anyone officially involved in producing or managing Age of Empires II. Age of Empires II is a trademark or registered trademark of Microsoft Corporation in the U.S. and other countries.</Typography>
      </main>
    </div>
  )
}

export default Layout
