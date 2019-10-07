import gql from 'graphql-tag';

import MatchFragment from '../graphql/MatchFragment.js';

export default gql`
query Map($name: String!, $offset: Int!, $limit: Int!) {
  map(name: $name) {
    name
    popular_civs {
      percent
      civilization {
        cid
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
