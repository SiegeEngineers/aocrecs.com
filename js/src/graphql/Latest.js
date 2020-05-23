import gql from 'graphql-tag';

import MatchFragment from "../graphql/MatchFragment.js"

export default gql`
query Latest($dataset_id: Int!, $order: [String], $offset: Int!, $limit: Int!) {
  latest {
    matches(dataset_id: $dataset_id, order: $order, offset: $offset, limit: $limit) {
      count
      hits {
        ...MatchFragment
      }
    }
  }
}
${MatchFragment}
`
