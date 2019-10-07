import gql from 'graphql-tag';

import MatchFragment from '../graphql/MatchFragment.js';

export default gql`
query User($user_id: String!, $platform_id: String!, $offset: Int!, $limit: Int!) {
  user(user_id: $user_id, platform_id: $platform_id) {
    id
    name
    canonical_name
    aliases
    meta_ranks {
      rating
      rank
      streak
      ladder {
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
      cid
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
