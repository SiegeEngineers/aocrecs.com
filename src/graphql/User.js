import gql from 'graphql-tag';

import MatchFragment from '../graphql/MatchFragment.js';

export default gql`
query User($user_id: String!, $platform_id: String!, $offset: Int!, $limit: Int!) {
  user(user_id: $user_id, platform_id: $platform_id) {
    id
    name
    image_small
    image_large
    last_login
    account_created
    meta_ranks {
      rank
      ladder {
        id
        name
      }
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
