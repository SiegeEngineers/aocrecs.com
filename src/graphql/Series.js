import gql from 'graphql-tag';

import MatchFragment from '../graphql/MatchFragment.js';

export default gql`
query Serie($id: Int!, $offset: Int!, $limit: Int!) {
  serie(id: $id) {
    name
    matches(offset: $offset, limit: $limit) {
      ...MatchFragment
    }
  }
}
${MatchFragment}
`
