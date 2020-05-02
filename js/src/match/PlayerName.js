import React from 'react'

import ReactCountryFlag from 'react-country-flag'

import AppLink from '../util/AppLink'
import {PLAYER_COLORS} from '../util/Shared'

const PlayerName = ({player}) => {
  return (
    <span>
      {player.color_id >= 0 && <div style={{
        backgroundColor: PLAYER_COLORS[player.color_id + 1],
        borderRadius: '4px',
        borderWidth: '1px',
        borderColor: 'white',
        height: '12px',
        width: '12px',
        display: 'inline-block',
        borderStyle: 'solid',
        marginRight: '4px'
      }}
      />}
      {player.user
          ? (player.user.person
            ? <span>{player.user.person.country && <ReactCountryFlag countryCode={player.user.person.country} title={player.user.person.country.toUpperCase()} svg />} <AppLink path={['players', player.user.person.id]} text={player.user.person.name} /> ({player.name})</span>
            : <AppLink path={['user', player.user.platform_id, player.user.id]} text={player.user.name} />)
        : player.name
      }
    </span>
  )
}

export default PlayerName
