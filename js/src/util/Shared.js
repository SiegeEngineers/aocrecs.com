import React from 'react'

export const PLAYER_COLORS = {
  1: '#6599d8',
  2: '#f25f5f',
  3: '#00ee00',
  4: '#ffd700',
  5: '#00eeee',
  6: '#ea69e1',
  7: '#808080',
  8: '#ff8c00'
}

export const getMatchTitle = (match, show_map) => {
  let title = match.type + ' ' + match.diplomacy_type
  if (match.diplomacy_type === 'TG') {
    title += ' ' + match.team_size
  }
  if (show_map) {
    title += ' on ' + match.map_name
  }
  return title
}

export const ChangeIndicator = ({change}) => {
  let out = ''
  let color = ''
  if (change > 0) {
    out = ' ' + String.fromCharCode(8593) + Math.abs(change)
    color = '#00ee00'
  } else if (change < 0) {
    out = ' ' + String.fromCharCode(8595) + Math.abs(change)
    color = '#f25f5f'
  }
  return (
    <span style={{color: color}}>{out}</span>
  )
}

export const getHasTeams = (size) => {
  return size !== '1v1'
}

export const getIsNomad = (map_name) => {
  return map_name.toLowerCase().includes('nomad')
}
