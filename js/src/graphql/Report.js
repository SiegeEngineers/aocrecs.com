import gql from 'graphql-tag';

export default gql`
query Report($year: Int!, $month: Int!) {
  report(platform_id: "voobly", year: $year, month: $month) {
    total_matches
    total_players
    most_matches {
      count
      user {
        platform_id
        id
        name
        person {
          name
        }
      }
    }
		popular_maps {
      rank
      map {
        name
      }
      count
      percent
    }
    rankings_1v1: rankings(platform_id: "voobly", ladder_id: 131) {
      rank
      user {
        id
        platform_id
        name
        person {
          name
        }
      }
      rating
      change
    }
    rankings_tg: rankings(platform_id: "voobly", ladder_id: 132) {
      rank
      user {
        id
        name
        platform_id
        person {
          name
        }
      }
      rating
      change
    }
    improvement_1v1: most_improvement(platform_id: "voobly", ladder_id: 131) {
      user {
        id
        platform_id
        name
        person {
          name
        }
      }
      min_rate
      max_rate
      diff_rate
      count
      wins
      losses
    }
    improvement_tg: most_improvement(platform_id: "voobly", ladder_id: 132) {
      user {
        id
        platform_id
        name
        person {
          name
        }
      }
      min_rate
      max_rate
      diff_rate
      count
      wins
      losses
    }
		longest_matches {
      id
      type
      diplomacy_type
      team_size
      map_name
      duration_secs
    }
  }
}
`
