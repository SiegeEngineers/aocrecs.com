import gql from 'graphql-tag';

import MatchFragment from "../graphql/MatchFragment.js"

export default gql`
query Search($params: GenericScalar!, $offset: Int!, $limit: Int!) {
  search(params: $params) {
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
