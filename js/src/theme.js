import {createMuiTheme} from '@material-ui/core/styles'

const theme = createMuiTheme({
  palette: {
    primary: {
      light: '#ffcc00',
      main: '#ff9900',
      dark: '#ff6600'
    },
    secondary: {
      main: '#3300ff',
    },
    type: 'dark',
  },
  typography: {
    useNextVariants: true,
  },
  overrides: {
    MuiTableCell: {
      root: {
        padding: '1px',
        paddingLeft: '3px',
        paddingRight: '3px'
      }
    },
    MuiTableRow: {
      root: {
        height: '26px'
      },
      head: {
        height: '26px'
      }
    },
    MuiCard: {
      root: {
        margin: '6px'
      }
    },
    MuiCardContent: {
      root: {
        '&:last-child': {
          paddingBottom: '16px'
        }
      }
    },
    MuiTab: {
      root: {
        minWidth: 0,
        '@media (min-width: 0px)': {
          minWidth: 0
        }
      }
    }
  }
})

export default theme
