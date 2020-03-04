import gql from 'graphql-tag';

export default gql`
query Research($match_id: Int!) {
  match(id: $match_id) {
    id
    team_size
    duration_secs
    players {
      name
      color_id
      research {
        name
        started
        finished
        started_secs
        finished_secs
      }
      timeseries {
        timestamp_secs
        roi
        value_spent_research
      }
    }
  }
}
`
