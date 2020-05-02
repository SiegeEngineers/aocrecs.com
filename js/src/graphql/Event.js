import gql from 'graphql-tag';

export default gql`
query Event($id: String!) {
  event(id: $id) {
    id
    year
    name
    tournaments {
      id
      event_id
      name
      series {
        id
        name
        participants {
          name
          score
          winner
        }
      }
    }
    maps {
      map {
        name
      }
      match_count
      most_played_civilization {
        name
      }
      played_percent
      average_duration
    }
    players {
      match_count
      win_percent
      average_duration
      most_played_map
      most_played_civilization {
        id
        dataset_id
        name
      }
      player {
        name
        user {
          id
          platform_id
          name
          person {
            id
            name
            country
          }
        }
      }
    }
  }
}
`;
