import gql from 'graphql-tag';

export default gql`
query Units($match_id: Int!) {
  match(id: $match_id) {
    id
    team_size
    duration_secs
    players {
      name
      color_id
      timeseries {
        timestamp_secs
        kills
        deaths
        razes
        kd_delta
      }
      units_trained {
        timestamp_secs
        name
        count
      }
    }
  }
}
`
