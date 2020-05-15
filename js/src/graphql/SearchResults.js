import gql from 'graphql-tag';

import MatchFragment from "../graphql/MatchFragment.js"

export default gql`
query Search($params: Dict!, $order: [String], $offset: Int!, $limit: Int!) {
  search {
    matches(params: $params, order: $order, offset: $offset, limit: $limit) {
      count
      hits {
        ...MatchFragment
      }
    }
  }
}
${MatchFragment}
`
