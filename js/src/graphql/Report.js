import gql from 'graphql-tag';

export default gql`
query Report($year: Int!, $month: Int!) {
  report(year: $year, month: $month) {
    total_matches
    total_players
    most_matches(platform_id: "voobly") {
      platform_id
      count
      user {
        id
        name
        canonical_name
      }
    }
		popular_maps {
      rank
      name
      count
      percent
      change
    }
    rankings_1v1: rankings(platform_id: "voobly", ladder_id: 131) {
      rank
      user_id
      user {
        name
        canonical_name
      }
      platform_id
      rating
      change
    }
    rankings_tg: rankings(platform_id: "voobly", ladder_id: 132) {
      rank
      user_id
      user_name
      user {
        name
        canonical_name
      }
      platform_id
      rating
      change
    }
    improvement_1v1: most_improvement(platform_id: "voobly", ladder_id: 131) {
      user {
        id
        name
        canonical_name
      }
      platform_id
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
        name
        canonical_name
      }
      platform_id
      min_rate
      max_rate
      diff_rate
      count
      wins
      losses
    }
		longest_matches {
      id
      type {
        name
      }
      diplomacy_type
      team_size
      map_name
      duration_secs
    }
  }
}
`
