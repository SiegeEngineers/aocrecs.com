import gql from 'graphql-tag';

export default gql`
query ChartsTG($match_id: Int!) {
  match(id: $match_id) {
    id
    players {
      name
      color_id
      timeseries {
        timestamp_secs
        population
        military
        percent_explored
        value_objects_destroyed
        value_current_units
      }
    }
  }
}
`
