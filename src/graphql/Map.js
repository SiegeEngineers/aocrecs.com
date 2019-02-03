import gql from 'graphql-tag';

import MatchFragment from '../graphql/MatchFragment.js';

export default gql`
query Map($id: Int!, $offset: Int!, $limit: Int!) {
  map(id: $id) {
    name
    popular_civs {
      percent_matches
      civilization {
        cid
        name
      }
    }
    match_count
    matches(offset: $offset, limit: $limit) {
      ...MatchFragment
    }
  }
}
${MatchFragment}
`
