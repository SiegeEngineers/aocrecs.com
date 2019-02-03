import gql from 'graphql-tag';

import MatchFragment from '../graphql/MatchFragment.js';

export default gql`
query VooblyUser($user_id: String!, $offset: Int!, $limit: Int!) {
  voobly_user(user_id: $user_id) {
    id
    name
    image_small
    image_large
    last_login
    account_created
    matches(offset: $offset, limit: $limit) {
      ...MatchFragment
    }
    match_count
  }
}
${MatchFragment}
`
