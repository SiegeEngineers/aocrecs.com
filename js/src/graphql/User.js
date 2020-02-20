import gql from 'graphql-tag';

import MatchFragment from '../graphql/MatchFragment.js';

export default gql`
query User($user_id: String!, $platform_id: String!, $offset: Int!, $limit: Int!) {
  user(id: $user_id, platform_id: $platform_id) {
    id
    name
    person {
      id
      name
      country
    }
    meta_ranks(ladder_ids: [131, 132]) {
      rating
      rank
      streak
      ladder {
        platform_id
        id
        name
      }
      rate_by_day {
        date
        count
      }
    }
    top_map {
      name
    }
    top_civilization {
      id
      dataset_id
      name
    }
    top_dataset {
      name
    }
    matches(offset: $offset, limit: $limit) {
      count
      hits {
        ...MatchFragment
      }
    }
  }
}
${MatchFragment}
`
