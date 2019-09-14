import gql from 'graphql-tag';

export default gql`
query Odds($match_id: Int!) {
  match(match_id: $match_id) {
    odds {
      teams
      teams_and_civilizations
      civilizations
      civilizations_and_map
      teams_and_map
    }
  }
}
`
