import React, {useState} from 'react'
import {Link} from 'react-router-dom'
import {makeStyles} from '@material-ui/styles'

import Button from '@material-ui/core/Button'
import TextField from '@material-ui/core/TextField'

import RelatedMatches from './util/RelatedMatches'

import User from './User'

import GetUser from './graphql/User'

const useStyles = makeStyles({
  input: {
    margin: '5px'
  },
  button: {
    margin: '5px'
  },
  link: {
    textDecoration: 'none'
  }
})

const Players = ({match}) => {
  const [string, setString] = useState(null)
  const classes = useStyles()
  return (
    <div>
      <TextField
        type='search'
        onChange={(e) => setString(e.target.value)}
        className={classes.input}
        value={string}
      />
      <Link to={'/players/' + string} className={classes.link}>
        <Button variant='contained' color='primary' className={classes.button}>
          Search
        </Button>
      </Link>
      <br />
      {match.params.id &&
        <RelatedMatches
          query={GetUser}
          variables={{user_id: match.params.id}}
          field='voobly_user'
        >
          {(data) => (
            <User user={data} />
          )}
        </RelatedMatches>
      }
    </div>
  )
}

export default Players
