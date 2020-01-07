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
