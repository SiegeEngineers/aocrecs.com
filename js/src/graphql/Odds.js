import gql from 'graphql-tag';

export default gql`
query Odds($match_id: Int!) {
  match(id: $match_id) {
    odds {
      teams { wins losses percent }
      teams_and_civilizations { wins losses percent }
      civilizations { wins losses percent }
      civilizations_and_map { wins losses percent }
      teams_and_map { wins losses percent }
    }
  }
}
`
