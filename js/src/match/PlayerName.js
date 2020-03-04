import React from 'react'

import AppLink from '../util/AppLink'
import {PLAYER_COLORS} from '../util/Shared'

const PlayerName = ({player}) => {
  return (
    <span>
      <div style={{
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
      />
      {player.user
        ? <AppLink path={['user', player.user.platform_id, player.user.id]} text={player.user.name} />
        : player.name
      }
    </span>
  )
}

export default PlayerName
