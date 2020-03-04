import gql from 'graphql-tag';

export default gql`
query Economy($match_id: Int!) {
  match(id: $match_id) {
    id
    duration_secs
    teams {
      winner
      players {
        color_id
        winner
        name
        user {
          id
          platform_id
          name
        }
        metrics {
          dark_age_tc_idle
          total_tcs
          average_floating_resources
          seconds_housed
          seconds_villagers_idle
          seconds_popcapped
        }
      }
    }
    players {
      color_id
      name
      timeseries {
        timestamp_secs
        relic_gold
        total_food
        total_wood
        total_stone
        total_gold
      }
      villagers {
        timestamp_secs
        count
      }
      villager_allocation {
        timestamp_secs
        name
        count
      }
    }
  }
}
`
